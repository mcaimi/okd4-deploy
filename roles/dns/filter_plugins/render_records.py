#!/usr/bin/python
# this filter renders a list of records for the Named service
#
from string import Template
import ipaddress

# main filter class
class FilterModule(object):
    def filters(self):
        # return methods for use in ansible templates
        return {
                'octet': self.octet,
                'reverse_zone': self.reverse_zone
                }

    def reverse_zone(self, cidr_subnet):
        network = ipaddress.ip_network(cidr_subnet)
        return network.reverse_pointer[5:]

    def octet(self, server_address, index=1):
        address = ipaddress.ip_address(server_address)
        return str(address).split(".")[index]
