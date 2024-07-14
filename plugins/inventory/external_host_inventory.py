"""Ansible plugin for parsing inventory data from an external system
Here, I have used netbox as an example however it can be any system that
exposes its data via API. Netbox has its own python package. I am calling the cluster
api instead to show the use case.
"""
from __future__ import (absolute_import, division, print_function)

import os
from datetime import datetime
from datetime import timedelta

import requests
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

DOCUMENTATION = r'''
    inventory: external_host_inventory
    plugin_type: inventory
    short_description: Loads hosts from the host database into the inventory.
    description: Returns Ansible inventory from database
    options:
      plugin:
        description: Name of the plugin
        required: true
        choices: ['collectionlib.core.external_host_inventory']
      service_endpoint:
        description: api endpoint of the hosted service
        required: true

'''

EXAMPLES = '''
    plugin: collectionlib.core.external_host_inventory
    service_endpoint: http://localhost:8000
'''


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    """Custom inventory definition based on an external inventory system"""
    NAME = 'collectionlib.core.external_host_inventory'

    def verify_file(self, path):
        """Verifies that the file is a yaml file"""

        if not super().verify_file(path):
            return False

        # Only load the main hosts file
        if not path.endswith('.yml'):
            return False

        with open(path, encoding="utf-8") as hostfile:
            data = hostfile.read().splitlines()

        # Only process YAML files that are defined as si_yaml_inventory
        if 'plugin: ' + self.NAME in data:
            return True

        return False

    def get_clusters(self, url, token):
        """

        :param url: Netbox base url
        :param token: A token to query or post data
        :return: Clusters
        """
        headers = {
            "accept": "application/json",
            "authorization": "Token {}".format(self._token)
        }

        data = requests.get(url=f"{self.service_endpoint}/api/virtualization/clusters/", headers=headers)
        data.raise_for_status()
        return data.json()

    def parse(self, inventory, loader, path, cache=True):
        """ parses the inventory file """
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
        self.use_cache = cache
        self.service_endpoint = self.get_option("service_endpoint")
        self._token = os.getenv("token")

        self.verify_file(path)

        # Get all clusters
        clusters = self.get_clusters(url=self.service_endpoint, token=self._token)['results']

        # Set host_vars, group_vars
        for cluster in clusters:
            cluster_name = cluster.get('name')
            host_name = cluster_name
            # Add a host to the inventory
            inventory.add_host(host_name)

            # Create host_vars
            cluster_type = cluster.get('type').get('name')
            cluster_group = cluster.get('group').get('name', 'not defined')
            cluster_status = cluster.get('status').get('label', 'not defined')

            # Add variables about the hosts
            inventory.set_variable(host_name, 'inventory_cluster_name', cluster_name)
            inventory.set_variable(host_name, 'inventory_cluster_type', cluster_type)
            inventory.set_variable(host_name, 'inventory_cluster_group', cluster_group)
            inventory.set_variable(host_name, 'inventory_cluster_status', cluster_status)

            # Add host groups to target certain hosts
            groups = [
                cluster_type,
                cluster_status,
                cluster_group
            ]

            # Link host with groups
            for group in groups:
                inventory.add_group(group)
                inventory.add_host(host_name, group)
