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

# main filter class
class FilterModule(object):
    def filters(self):
        # return methods for use in ansible templates
        return {'list_to_string': self.list_to_string}

    # list flatten method
    def list_to_string(self, input_list, separator=";"):
        if type(input_list) is not list:
            raise TypeError("input_list must be a python-compatible list object")

        # return the flattened string
        return separator.join(input_list)

