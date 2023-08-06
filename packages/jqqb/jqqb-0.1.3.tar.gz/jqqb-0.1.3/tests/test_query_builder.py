import json
import unittest

from jqqb import QueryBuilder


class TestCreateQueryBuilderInstance(unittest.TestCase):
    def setUp(self) -> None:
        self.rule_set_json = {
            "condition": "AND",
            "rules": [
                {
                    "operator": "equal",
                    "inputs": [
                        {
                            "field": "dummy_key1",
                            "value": "dummy_value1",
                            "type": "dummy_type1",
                        },
                        {
                            "field": "dummy_key2",
                            "value": "dummy_value2",
                            "type": "dummy_type2",
                        }
                    ],
                }
            ]
        }
        return super().setUp()

    def test_create_query_builder_instance_from_json(self):
        query_builder = QueryBuilder.create_query_builder_from_json(
            rule_set_json=self.rule_set_json
        )

        self.assertIsInstance(query_builder, QueryBuilder)


class TestQueryBuilderInspect(unittest.TestCase):
    def setUp(self) -> None:
        self.rule_set_json = {
            "condition": "AND",
            "rules": [
                {
                    "operator": "equal",
                    "inputs": [
                        {
                            "field": "dummy_key1",
                            "value": None,
                            "type": "dummy_type1",
                        },
                        {
                            "field": "dummy_key2",
                            "value": None,
                            "type": "dummy_type2",
                        }
                    ],
                }
            ]
        }
        self.query_builder = QueryBuilder.create_query_builder_from_json(
            rule_set_json=self.rule_set_json
        )
        return super().setUp()

    def test_query_builder_inspect(self):
        object = {"dummy_key1": "dummy_value", "dummy_key2": "dummy_value"}
        results = self.query_builder.inspect_objects(objects=[object])

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertIsInstance(result, dict)
        self.assertTrue(
            all(
                key in result
                for key in (
                    "object", "predicate", "results", "rules", "selected"
                )
            )
        )
        self.assertEqual(result["object"], object)
        self.assertEqual(
            result["predicate"], "AND(equal(dummy_value, dummy_value))"
        )
        self.assertIsInstance(result["rules"], dict)
        self.assertTrue(result["selected"])
        self.assertEqual(
            result["results"],
            [
                (
                    {
                        "operator": "equal",
                        "inputs": [
                            {
                                "field": "dummy_key1",
                                "value": "dummy_value",
                                "type": "dummy_type1",
                            },
                            {
                                "field": "dummy_key2",
                                "value": "dummy_value",
                                "type": "dummy_type2",
                            }
                        ],
                    },
                    ("dummy_value", "dummy_value", True),
                ),
            ]
        )

        try:
            json.dumps(results)
        except Exception as e:
            self.assertTrue(
                False,
                f"`inspect_objects` result should be JSON serializable: {e}"
            )

    def test_query_builder_inspect_missing_key_are_same_as_None_value(self):
        object = {"dummy_key1": None}
        results = self.query_builder.inspect_objects(objects=[object])

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertIsInstance(result, dict)
        self.assertTrue(
            all(
                key in result
                for key in (
                    "object", "predicate", "results", "rules", "selected"
                )
            )
        )
        self.assertEqual(result["object"], object)
        self.assertEqual(
            result["predicate"], "AND(equal(None, None))"
        )
        self.assertIsInstance(result["rules"], dict)
        self.assertTrue(result["selected"])
        self.assertEqual(
            result["results"],
            [
                (
                    {
                        "operator": "equal",
                        "inputs": [
                            {
                                "field": "dummy_key1",
                                "value": None,
                                "type": "dummy_type1",
                            },
                            {
                                "field": "dummy_key2",
                                "value": None,
                                "type": "dummy_type2",
                            }
                        ],
                    },
                    (None, None, True),
                ),
            ]
        )

        try:
            json.dumps(results)
        except Exception as e:
            self.assertTrue(
                False,
                f"`inspect_objects` result should be JSON serializable: {e}"
            )
