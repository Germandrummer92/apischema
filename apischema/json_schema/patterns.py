from typing import Pattern

from apischema.conversions.conversions import DefaultConversions
from apischema.types import AnyType


def infer_pattern(tp: AnyType, default_conversions: DefaultConversions) -> Pattern:
    from apischema.json_schema.schema import DeserializationSchemaBuilder

    try:
        builder = DeserializationSchemaBuilder(
            False, lambda s: s, default_conversions, False, lambda r: r, {}
        )
        prop_schema = builder.visit(tp)
    except RecursionError:
        pass
    else:
        if (
            len(prop_schema.get("patternProperties", {})) == 1
            and "additionalProperties" not in prop_schema
        ):
            return next(iter(prop_schema["patternProperties"]))
    raise TypeError("Cannot inferred pattern from type schema") from None
