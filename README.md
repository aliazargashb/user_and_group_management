# Ansible Project Structure
This project is structured to manage network infrastructure using Ansible, organized with inventories, group variables, host-specific configurations, and playbooks to configure different sets of devices such as leafs, spines, and superspines.

## Project Structure
```bash
├── ansible.cfg
├── inventories
│   ├── group_vars
│   │   ├── all.yaml
│   │   ├── bmi_leafs.yaml
│   │   ├── bmi_spines.yaml
│   │   ├── bmi.yaml
│   │   ├── border_leafs.yaml
│   │   ├── leafs.yaml
│   │   ├── sic_leafs.yaml
│   │   ├── sic_spines.yaml
│   │   ├── sic.yaml
│   │   ├── spines.yaml
│   │   └── superspines.yaml
│   ├── hosts
│   └── host_vars
│       ├── bmi_BL.yaml
│       ├── bmi_leaf1.yaml
│       ├── bmi_spine1.yaml
│       ├── bmi_spine2.yaml
│       ├── bmi_superspine.yaml
│       ├── sic_BL.yaml
│       ├── sic_leaf1.yaml
│       ├── sic_leaf2.yaml
│       ├── sic_spine1.yaml
│       ├── sic_spine2.yaml
│       └── sic_superspine.yaml
└── playbooks
    ├── leafs.yaml
    ├── spine.yaml
    └── superspine.yaml
```
