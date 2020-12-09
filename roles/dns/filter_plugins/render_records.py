#!/usr/bin/python
# this filter renders a list of records for the Named service
#
# example:
# zones:
#   - name: test.local
#     records:
#       - name: server
#         type: A
#         value: 192.168.1.1
#       - name: service
#         proto: tcp
#         ttl: 86400
#         priority: 1
#         weight: 1
#         port: 1234
#         target: target.domain.com
#         type: SRV
#
# output:
#   192.168.1.1 IN  A   server.test.local.
#   _service._tcp.test.local.   86400 IN SRV 1 1 1234 target.domain.com.
#

from string import Template

# main filter class
class FilterModule(object):
    def filters(self):
        # return methods for use in ansible templates
        return {'render_records': self.render_records}

    # list flatten method
    def render_records(self, zone_records, domain=None):
        if domain is None:
            raise RuntimeException("render_records: domain cannot be None")

        # supported record types
        record_template = Template("$hostname.$domain_name. IN $record_type $ipaddress")
        ptr_template = Template("$ipaddress IN $record_type $hostname.$domain_name.")
        srv_record_template = Template("_$servicename._$proto.$domain_name. $ttl IN SRV $priority $weight $port $target.")
        rendered_records = []
        # gather info
        for record in zone_records:
            if record.get('type') == "SRV":
                rendered_records.append(srv_record_template.substitute(servicename=record.get('name'),
                    proto=record.get('proto'),
                    domain_name=domain,
                    ttl=record.get('ttl'),
                    priority=record.get('priority'),
                    weight=record.get('weight'),
                    port=record.get('port'),
                    target=record.get('target'))
                )
            elif record.get('type') == 'PTR':
                rendered_records.append(ptr_template.substitute(ipaddress=record.get('value'),
                    record_type=record.get('type'),
                    hostname=record.get('name'),
                    domain_name=domain)
                )
            else:
                rendered_records.append(record_template.substitute(ipaddress=record.get('value'),
                    record_type=record.get('type'),
                    hostname=record.get('name'),
                    domain_name=domain)
                )

        # return rendered list as a string
        return "\n".join(rendered_records)
