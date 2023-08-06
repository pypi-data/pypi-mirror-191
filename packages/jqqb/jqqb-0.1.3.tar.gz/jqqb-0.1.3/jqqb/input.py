import json
from datetime import date, datetime, time
from functools import reduce
from typing import Any, Optional, Union


class Input:
    class NotRetrievedValue:
        pass

    _CAST_FUNCTIONS = {
        "boolean": bool,
        "datetime": lambda x: (
            datetime.fromisoformat(x) if isinstance(x, str) else x
        ),
        "date": lambda x: (
            date.fromisoformat(x) if isinstance(x, str) else x
        ),
        "double": float,
        "integer": int,
        "string": str,
        "time": lambda x: (
            time.fromisoformat(x) if isinstance(x, str) else x
        ),
    }

    def __init__(
        self,
        type: str,
        field: Optional[str] = None,
        value: Any = NotRetrievedValue,
    ) -> None:
        self.field = field
        self.type = type
        self.value = value

    @classmethod
    def create_input_from_json(cls, input_json: Union[dict, str]) -> "Input":
        """Construct an Input instance from a given JSON.

        Note:
            JSON format:
            ```
            {
                "field": string|null,
                "type": string,
                "value": number|string|null
            }
            ```
        """
        parsed_input_json = (
            json.loads(input_json)
            if isinstance(input_json, str)
            else input_json
        )
        field = parsed_input_json["field"]
        data = {"field": field, "type": parsed_input_json["type"]}

        if not field:
            data["value"] = parsed_input_json["value"]

        return cls(**data)

    def get_value(self, object: Optional[dict] = None) -> Any:
        if self.value is self.NotRetrievedValue and object is not None:
            self.value = self.get_value_from_object(object=object)

        return self.typecast_value(value_to_cast=self.value)

    def get_value_from_object(self, object: dict) -> Any:
        fields = self.field.split(".")
        last_object = reduce(lambda x, y: x.get(y, {}), fields[:-1], object)
        return last_object.get(fields[-1])

    def jsonify(self, object: dict) -> dict:
        return {
            "field": self.field,
            "type": self.type,
            "value": self.get_value(object=object),
        }

    def typecast_value(self, value_to_cast: Any) -> Any:
        cast_function = self._CAST_FUNCTIONS.get(self.type)

        if (
            value_to_cast in (None, self.NotRetrievedValue)
            or cast_function is None
        ):
            return value_to_cast

        return cast_function(value_to_cast)
