#!/usr/bin/python
# this filter takes a list in input and returns a flattened string
# a separator can also be specified
#
# example:
# list_of_things:
#   - first
#   - second
#
# output: "first;second"
#
# optional left and right pads can be specified in jinja template
# final string will be rendered as template:
#
#   <optional left pad char><string text><optional right pad char><separator>
#

from string import Template

# main filter class
class FilterModule(object):
    def filters(self):
        # return methods for use in ansible templates
        return {'list_to_string': self.list_to_string}

    # list flatten method
    def list_to_string(self, input_list, separator=";", rpad=False, lpad=False, pad_char=" "):
        nothing = ''
        PADS_TABLE = {
                (True, True): (pad_char, pad_char),
                (True, False): (pad_char, nothing),
                (False, True): (nothing, pad_char),
                (False, False): (nothing, nothing)
            }

        if type(input_list) is not list:
            raise TypeError("input_list must be a python-compatible list")

        # apply padding if needed
        lp, rp = PADS_TABLE.get((lpad, rpad))

        # return the flattened string
        return separator.join([Template("$left_pad$text$right_pad").substitute(text=t, left_pad=lp, right_pad=rp) for t in input_list])
