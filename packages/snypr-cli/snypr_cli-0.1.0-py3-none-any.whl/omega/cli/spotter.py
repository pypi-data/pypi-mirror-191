import re
import sigma
from sigma.backends.base import SingleTextQueryBackend

from sigma.parser.modifiers.base import SigmaTypeModifier
from sigma.parser.modifiers.type import SigmaRegularExpressionModifier
from sigma.parser.modifiers.transform import SigmaContainsModifier, SigmaStartswithModifier, SigmaEndswithModifier

_notConditionMapping = {
    'EQUALS': '!=',
    '=': '!=',
    'CONTAINS': 'NOT CONTAINS',
    'ENDS WITH': 'NOT ENDS WITH',
    'STARTS WITH': 'NOT STARTS WITH',
    'exists':  'NOT NULL',
    'NULL': 'NOT NULL'
}


class Spotter(SingleTextQueryBackend):
    """Converts Sigma rule into Securonix Search Processing Language (SPL)."""
    identifier = "securonix"
    active = True
    iindex_field = None

    def __init__(self, options, config_file):
        super().__init__(options, config_file)
    reEscape = None
    reClear = None
    andToken = " AND "
    orToken = " OR "
    notToken = ""
    subExpression = "%s"
    listExpression = "(%s)"
    listSeparator = " "
    valueExpression = "\"%s\""
    nullExpression = "%s NULL "
    notNullExpression = "%s NOT NULL"
    mapExpression = "%s=%s"
    mapListsSpecialHandling = True
    mapListValueExpression = "%s IN %s"

    def generateMapItemListNode(self, key, value):
        if not set([type(val) for val in value]).issubset({str, int}):
            raise TypeError("List values must be strings or numbers")
        return "(" + (" OR ".join(['%s=%s' % (key, self.generateValueNode(item)) for item in value])) + ")"

    def generateAggregation(self, agg):
        if agg == None:
            return ""
        if agg.aggfunc == sigma.parser.condition.SigmaAggregationParser.AGGFUNC_NEAR:
            raise NotImplementedError(
                "The 'near' aggregation operator is not yet implemented for this backend")
        if agg.groupfield == None:
            raise NotImplementedError(
                "The 'groupfield' aggregation operator is not yet implemented for this backend")
        else:
            raise NotImplementedError(
                "The 'groupfield2' aggregation operator is not yet implemented for this backend")

    def generate(self, sigmaparser):
        """Method is called for each sigma rule and receives the parsed rule (SigmaParser)"""
        columns = list()
        mapped = None
        try:
            for field in sigmaparser.parsedyaml["fields"]:
                mapped = sigmaparser.config.get_fieldmapping(
                    field).resolve_fieldname(field, sigmaparser)
                if type(mapped) == str:
                    columns.append(mapped)
                elif type(mapped) == list:
                    columns.extend(mapped)
                else:
                    raise TypeError("Field mapping must return string or list")
            fields = ""
        except KeyError:
            mapped = None
            pass
        for parsed in sigmaparser.condparsed:
            query = self.generateQuery(parsed)
            before = self.generateBefore(parsed)
            after = self.generateAfter(parsed)
            result = ""
            if before is not None:
                result = before
            if query is not None:
                result += query
            if after is not None:
                result += after
            if mapped is not None:
                result += fields
            if "(" == result[:1] and ")" == result[-1:]:
                result = result[1:]
                result = result[:-1]
            return result

    def default_value_mapping(self, val):
        op = "="
        if isinstance(val, str):
            if val.startswith("*") or val.endswith("*"):
                if val.startswith("*") and val.endswith("*"):
                    op = "CONTAINS"
                elif val.startswith("*"):
                    op = "ENDS WITH"
                elif val.endswith("*"):
                    op = "STARTS WITH"
                val = re.sub('^\*|\*$', '', val)
                return "%s \"%s\"" % (op, self.cleanValue(val))
        return "%s \"%s\"" % (op, self.cleanValue(val))

    def generateNOTNode(self, node):
        generated = self.generateNode(node.item)
        if generated is not None:
            ops = ["=", "EQUALS", "CONTAINS", "ENDS WITH",
                   "STARTS WITH", "exists", "NULL"]
            for op in ops:
                if op in generated and op in _notConditionMapping:
                    generated = generated.replace(" {} ".format(
                        op), " {} ".format(_notConditionMapping[op]))
            return self.notToken + generated
        else:
            return None

    def cleanValue(self, val):
        if val and isinstance(val, str) and val.endswith("\\\\*"):
            val = val[:-2]
            val += "*"
        return super().cleanValue(val)

    def generateMapItemNode(self, node):
        key, value = node
        key = self.fieldNameMapping(key, value)
        if type(value) == list:
            result = self.generateORNode(
                [(key, v) for v in value]
            )
            if len(value) > 1:
                return "(" + result + ")"
            else:
                return result

        elif type(value) in [SigmaTypeModifier, SigmaContainsModifier, SigmaRegularExpressionModifier, SigmaStartswithModifier, SigmaEndswithModifier]:
            return self.generateMapItemTypedNode(key, value)
        elif type(value) in (str, int):
            value_mapping = self.default_value_mapping
            mapping = (key, value_mapping)
            if len(mapping) == 1:
                mapping = mapping[0]
                if type(mapping) == str:
                    return mapping
                elif callable(mapping):
                    return self.generateSubexpressionNode(
                        self.generateANDNode(
                            [cond for cond in mapping(
                                key, self.cleanValue(value))]
                        )
                    )
            elif len(mapping) == 2:
                result = list()
                for mapitem, val in zip(mapping, node):
                    if type(mapitem) == str:
                        result.append(mapitem)
                    elif callable(mapitem):
                        result.append(mapitem(self.cleanValue(val)))
                return "{} {}".format(*result)
            else:
                raise TypeError(
                    "Backend does not support map values of type " + str(type(value)))
        elif type(value) == list:
            return self.generateMapItemListNode(key, value)
        elif value is None:
            return self.nullExpression % (key, )
        else:
            raise TypeError(
                "Backend does not support map values of type " + str(type(value)))
