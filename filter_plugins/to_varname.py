from ansible.module_utils._text import to_text
from collections import OrderedDict
import re



class FilterModule(object):
    def filters(self):
        return {'to_varname': self.to_varname }

    def to_varname(self, param):
        ''' Perform a `re.sub` returning a string that is a valid Ansible variable name.'''
        param = to_text(param, errors='surrogate_or_strict', nonstring='simplerepr')
        lower_param = param.lower()
        output = re.sub(r'[^a-z0-9_]+', '_', lower_param)

        return output
