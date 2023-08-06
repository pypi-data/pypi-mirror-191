import json
from typing import Union

from jqqb.input import Input
from jqqb.operator import Operator


class Rule:
    def __init__(self, operator: Operator, inputs: list[Input]):
        self.inputs = inputs
        self.operator = operator

    @classmethod
    def create_rule_from_json(cls, rule_json: Union[dict, str]) -> "Rule":
        """Construct a Rule instance from a given JSON.

        Note:
            JSON format:
            ```
            {
                "inputs": list[object],
                "operator": string
            }
            ```
        """
        parsed_rule_json = (
            json.loads(rule_json)
            if isinstance(rule_json, str)
            else rule_json
        )
        return cls(
            operator=Operator.get_operator(parsed_rule_json["operator"]),
            inputs=[
                Input.create_input_from_json(input_json=parsed_rule_input_json)
                for parsed_rule_input_json
                in parsed_rule_json["inputs"]
            ]
        )

    def _get_input_values(self, object: dict) -> list:
        return [input.get_value(object=object) for input in self.inputs]

    def evaluate(self, object: dict) -> bool:
        return self.operator(*self._get_input_values(object))

    def get_predicate(self, object: dict) -> str:
        input_predicates = [
            str(input.get_value(object=object)) for input in self.inputs
        ]
        return (
            f"{Operator.get_operator_predicate(operator=self.operator)}("
            f"{', '.join(input_predicates)})"
        )

    def inspect(self, object: dict) -> tuple:
        return (
            *[input.get_value(object=object) for input in self.inputs],
            self.evaluate(object=object),
        )

    def jsonify(self, object: dict) -> dict:
        return {
            "inputs": [input.jsonify(object=object) for input in self.inputs],
            "operator": Operator.jsonify(operator=self.operator),
        }
