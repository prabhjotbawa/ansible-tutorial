### Vision
The purpose of the project is to create a template for ansible plugins. This is a work in progress and will evolve over
time however my vision is to have the below covered and I will follow an iterative approach to achieve it.
- Inventory plugin
  - Calls netbox api to query clusters and add set set host vars, group vars to use in playbooks
  - Queries a host file to construct the host and group vars
- Create a docker image of the project
- Lookup plugin
- Module and/or action plugin
- Unit Tests to test the plugins
- Create documentation
- **Stretch Goal**: Molecule framework to test playbook functionality

Additional documentation related to sample playbooks can be found [here](./docs/helper.md)

I will also add a developer doc at a later date.

## What's completed
- Inventory plugin
  - Calls netbox api to query clusters and sets host vars, group vars to use in playbooks