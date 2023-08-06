import unittest

from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.rule_group import RuleGroup
from jqqb.rule import Rule


class TestRuleGroupJsonify(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {"dummy_key": "dummy_value"}
        self.expected_result = {
            "condition": "AND",
            "rules": [{
                "operator": "equal",
                "inputs": [
                    {
                        "field": "dummy_key",
                        "value": "dummy_value",
                        "type": "str",
                    },
                    {
                        "field": None,
                        "value": "dummy_value",
                        "type": "str",
                    },
                ],
            }],
        }
        return super().setUp()

    def test_rule_group_jsonify(self):
        instance = RuleGroup(
            condition="AND",
            rules=[
                Rule(
                    operator=Operator.eval_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", field=None, value="dummy_value"),
                    ],
                ),
            ],
        )
        result = instance.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)

    def test_rule_group_created_from_json_jsonify(self):
        instance_json = {
            "condition": "AND",
            "rules": [{
                "operator": "equal",
                "inputs": [
                    {"field": "dummy_key", "value": None, "type": "str"},
                    {"field": None, "value": "dummy_value", "type": "str"},
                ],
            }],
        }
        instance = RuleGroup.create_rule_group_from_json(
            rule_group_json=instance_json
        )
        result = instance.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)
