import unittest

from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.rule import Rule


class TestRuleJsonify(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {"dummy_key": "dummy_value"}
        self.expected_result = {
            "operator": "equal",
            "inputs": [
                {"field": "dummy_key", "value": "dummy_value", "type": "str"},
                {"field": None, "value": "dummy_value", "type": "str"},
            ],
        }
        return super().setUp()

    def test_rule_jsonify(self):
        rule = Rule(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key"),
                Input(type="str", field=None, value="dummy_value"),
            ],
        )
        result = rule.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)

    def test_rule_created_from_json_jsonify(self):
        rule_json = {
            "operator": "equal",
            "inputs": [
                {"field": "dummy_key", "value": None, "type": "str"},
                {"field": None, "value": "dummy_value", "type": "str"},
            ],
        }
        rule = Rule.create_rule_from_json(rule_json=rule_json)
        result = rule.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)
