### Inventory plugin
Checking the host and group vars were set properly
Run 
```commandline
ansible-inventory -i inventory/build.yml --list
```
Output
```yaml
    "all": {
        "children": [
            "ungrouped",
            "DigitalOcean",
            "Active",
            "EMEA",
            "Asia Pacific",
            "North America",
            "Google Cloud",
            "South America"
        ]
    }
```

I could use a group var to target specific hosts, For instance, all clusters in EMEA can be targeted at once.
Execute sample playbook
```commandline
 ansible-playbook playbooks/sample_inventory_playbook.yml -l EMEA
```
Output
```
DO-AMS3                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
DO-FRA1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
DO-LON1                    : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-north1           : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-west1            : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-west2            : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-west3            : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-west4            : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
gc-europe-west6            : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
Above output shows the playbook was run against all the clusters in EMEA.