import unittest

from jqqb.input import Input


class TestInputFieldJsonify(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {"dummy_key": "dummy_value"}
        return super().setUp()

    def test_input_field_jsonify(self):
        instance = Input(field="dummy_key", type="str")
        result = instance.jsonify(object=self.object)

        expected_result = {
            "field": "dummy_key", "value": "dummy_value", "type": "str"
        }
        self.assertEqual(result, expected_result)

    def test_input_value_jsonify(self):
        instance = Input(field=None, type="str", value="dummy_value")
        result = instance.jsonify(object=self.object)

        expected_result = {
            "field": None, "value": "dummy_value", "type": "str"
        }
        self.assertEqual(result, expected_result)

    def test_input_field_created_from_json_jsonify(self):
        instance_json = {"field": "dummy_key", "value": None, "type": "str"}
        instance = Input.create_input_from_json(input_json=instance_json)
        result = instance.jsonify(object=self.object)

        expected_result = {
            "field": "dummy_key", "value": "dummy_value", "type": "str"
        }
        self.assertEqual(result, expected_result)

    def test_input_value_created_from_json_jsonify(self):
        instance_json = {"field": None, "value": "dummy_value", "type": "str"}
        instance = Input.create_input_from_json(input_json=instance_json)
        result = instance.jsonify(object=self.object)

        expected_result = {
            "field": None, "value": "dummy_value", "type": "str"
        }
        self.assertEqual(result, expected_result)
