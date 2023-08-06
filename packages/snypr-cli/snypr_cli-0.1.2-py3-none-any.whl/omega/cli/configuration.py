from sigma.configuration import SigmaConfiguration
from sigma.config.mapping import FieldMapping


class Configuration(SigmaConfiguration):
    def get_fieldmapping(self, fieldname):
        """Return mapped fieldname if mapping defined or field name given in parameter value"""
        try:
            return self.fieldmappings[fieldname]
        except KeyError:
            return FieldMapping("MappingNotFound_"+fieldname)
