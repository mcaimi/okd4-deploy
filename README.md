# OKD4 Install Helper

This repository aims to provide an easy way to deploy OKD 4.x on platform not directly supported by the automated installer.
The main goal is to easily build small clusters or lab deployments on bare-metal servers or libvirt nodes for example.

The installer is composed a set of Ansible Playbooks that handle all configuration/prerequisites tasks that are needed in order to successfully deploy OKD.

As a side-note, this is still an ongoing effort and there **will** be issues and bugs. Also, this project is not officially supported by RedHat.

## HW/SW Requirements

Both virtual environments and physical servers are supported, however for lab/dev deployments virtual machines are the go-to solution.
A minimal list of which machines are needed is shown below:

Server | Purpose | OS
------ | -------- | ----
Bastion Host | Server from where the playbooks are run. Also has access to deployed OKD Cluster | Any Linux but CentOS Stream is preferred
Services Host | Infrastructure Services Provider (DNS, DHCP, PXE, Load Balancer) | CentOS Stream 8
OKD Masters | Openshift Master Nodes (Control Plane) | Fedora CoreOS
OKD Workers | Openshift Worker Nodes (Application Nodes) | Fedora CoreOS
_(Optional)_ OKD Infra | Openshift Infrastructure Nodes (Infra Nodes dedicated for example to Prometheus or Ingress Controllers) | Fedora CoreOS

A single VM can be used as both the Bastion and the Services Hosts: while this is convenient for demos or very small deployments, this configuration can cause issues.
Also, the bastion host ideally can be as small as a laptop or a RaspberryPI. This node also may run any linux distribution or anything that can run ansible really.

## Playbooks

The installation process is split in three stages and every stage is handled by a playbook:

Stage | Playbook | Tasks
----- | -------- | -----
Infra Setup | `okd_deploy_services.yaml` | Sets up the services host, sets up the DNS and Load Balancer
Ignition Setup | `okd_ignition_config.yaml` | Renders configuration files for Ingition, installs OKD toolchain and CLI, sets up HTTPD
DHCP and PXE Configuration | `okd_setup_pxe_dhcp.yaml` | Configures the DHCP and PXE services

## Installation

### Variables file

All major configuration is done by modifiying the `vars/okd_cluster` variables file.

There are a few options that need to be customized:

Option | Value
------ | -----
`cluster_name` | the name given to the OKD cluster.
`base_domain` | DNS domain name of the OKD cluster. This will be combined with the `cluster_name` to form the full cluster domain
`ssh_key` | The public key that gets injected into CoreOS nodes
`machines.bootstrap.ipaddress` | The IP address of the bootstrap node
`machines.bootstrap.mac_address` | The MAC address of the bootstrap node
`machines.masters[].ipaddress` | The IP address of master nodes
`machines.masters[].mac_address` | The MAC address of master nodes
`machines.workers[].ipaddress` | The IP address of master nodes
`machines.workers[].mac_address` | The MAC address of master nodes
`services` | The IP address of the host that serves infrastructure components (DHCP, DNS, etc)

### Run Playbooks

Playbooks need to be run in this order:

1. `okd_deploy_services.yaml`
2. `okd_ignition_config.yaml`
3. `okd_setup_pxe_dhcp.yaml`

### Start OCP nodes

After the services are up and running, start all OCP nodes and monitor the boot process (Nodes should boot from PXE)

# TODO

- [ ] Finish this README

