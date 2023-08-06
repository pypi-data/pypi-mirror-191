import json
from typing import Literal, Union

from jqqb.rule import Rule


class RuleGroup:
    _CONDITIONS = {"AND": all, "OR": any}

    def __init__(
        self,
        condition: Literal["AND", "OR"],
        rules: list[Union["RuleGroup", Rule]],
    ):
        self.condition = condition
        self.condition_operation = self._CONDITIONS[condition]
        self.rules = rules

    @classmethod
    def create_rule_group_from_json(
        cls, rule_group_json: Union[str, dict]
    ) -> "RuleGroup":
        """Construct a RuleGroup instance from a given JSON.

        Note:
            JSON format:
            ```
            {
                "condition": "AND"|"OR",
                "rules": list[dict]
            }
            ```
        """
        parsed_rule_group_json = (
            json.loads(rule_group_json)
            if isinstance(rule_group_json, str)
            else rule_group_json
        )
        return cls(
            condition=parsed_rule_group_json["condition"],
            rules=[
                cls.create_rule_group_from_json(
                    rule_group_json=parsed_rule_group_json_rule
                )
                if "rules" in parsed_rule_group_json_rule
                else Rule.create_rule_from_json(
                    rule_json=parsed_rule_group_json_rule
                )
                for parsed_rule_group_json_rule
                in parsed_rule_group_json["rules"]
            ]
        )

    def evaluate(self, object: dict) -> bool:
        return self.condition_operation(
            [rule.evaluate(object) for rule in self.rules]
        )

    def get_predicate(self, object: dict) -> str:
        rule_predicates = [
            rule.get_predicate(object=object) for rule in self.rules
        ]
        return f"{self.condition}({', '.join(rule_predicates)})"

    def inspect(self, object: dict) -> list[tuple]:
        return [
            (rule.jsonify(object=object), rule.inspect(object=object))
            for rule in self.rules
        ]

    def jsonify(self, object: dict) -> dict:
        return {
            "condition": self.condition,
            "rules": [rule.jsonify(object=object) for rule in self.rules],
        }
