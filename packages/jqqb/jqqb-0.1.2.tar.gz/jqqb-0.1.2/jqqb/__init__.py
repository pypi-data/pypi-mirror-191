from typing import Union

from jqqb.rule_group import RuleGroup


class QueryBuilder:
    def __init__(self, rule_group: RuleGroup):
        self.rule_group = rule_group

    @classmethod
    def create_query_builder_from_json(
        cls, rule_set_json: Union[str, dict]
    ) -> "QueryBuilder":
        return cls(
            rule_group=RuleGroup.create_rule_group_from_json(
                rule_group_json=rule_set_json
            )
        )

    def match_objects(self, objects: list[dict]) -> list[dict]:
        return [
            object for object in objects if self.object_matches_rules(object)
        ]

    def object_matches_rules(self, object: dict) -> dict:
        return self.rule_group.evaluate(object)

    def inspect_objects(self, objects: list[dict]) -> list[dict]:
        return [
            {
                "object": object,
                "predicate": self.rule_group.get_predicate(object=object),
                "results": self.rule_group.inspect(object=object),
                "rules": self.rule_group.jsonify(object=object),
                "selected": self.object_matches_rules(object=object),
            } for object in objects
        ]
