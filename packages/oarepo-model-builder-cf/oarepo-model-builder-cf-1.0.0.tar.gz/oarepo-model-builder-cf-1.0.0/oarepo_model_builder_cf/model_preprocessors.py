import os
from pathlib import Path
from typing import Dict

from oarepo_model_builder.utils.jinja import split_base_name

from oarepo_model_builder.schema import ModelSchema
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class CFModelPreprocessor(ModelPreprocessor):
    TYPE = "extend-base-classes"

    def transform(self, schema: ModelSchema, settings: Dict):
        current_model = schema.current_model
        custom_fields = current_model.get("custom-fields", [])
        if not custom_fields:
            return

        # need DataComponent in order to work properly
        components_key = "record-service-config-components"
        data_component = (
            "invenio_records_resources.services.records.components.DataComponent"
        )
        if components_key not in current_model:
            current_model[components_key] = []
        for c in current_model[components_key]:
            if c == data_component:
                break
        else:
            current_model[components_key].append(data_component)

        for cf in custom_fields:
            element = cf.get("element", None)
            config = cf.get("config", None)

            if element:
                # add this element to the model and let the rest of the framework generate the schema etc.
                current_model["properties"][element] = {
                    "type": "object",
                    "jsonschema": {"additionalProperties": True},
                    "mapping": {"type": "object", "dynamic": True},
                    "marshmallow": {
                        "field": f'NestedAttribute(partial(CustomFieldsSchema, fields_var="{config}"))',
                        "imports": [
                            {
                                "import": "invenio_records_resources.services.custom_fields.CustomFieldsSchema"
                            },
                            {"import": "functools.partial"},
                            {"import": "marshmallow_utils.fields.NestedAttribute"},
                        ],
                    },
                    "sample": {"skip": True},
                }
            else:
                # just make the schema extensible
                if "jsonschema" not in current_model:
                    current_model["jsonschema"] = {}
                current_model["jsonschema"]["additionalProperties"] = True

                # make mapping extensible
                path = ["mapping", "os-v2", "mappings"]
                d = current_model
                for p in path:
                    if p not in d:
                        d[p] = {}
                    d = d[p]
                d["dynamic"] = True

                # in marshmallow, inherit from extensible mixin
                if "marshmallow" not in current_model:
                    current_model["marshmallow"] = {}
                marshmallow = current_model["marshmallow"]
                if "base-classes" not in marshmallow:
                    marshmallow["base-classes"] = []
                marshmallow["base-classes"].insert(0, "InlinedCustomFieldsSchemaMixin")
                if "imports" not in marshmallow:
                    marshmallow["imports"] = []
                marshmallow["imports"].append(
                    {"import": "oarepo_runtime.cf.InlinedCustomFieldsSchemaMixin"}
                )
                if "extra-fields" not in marshmallow:
                    marshmallow["extra-fields"] = []
                marshmallow["extra-fields"].append(
                    {"name": "CUSTOM_FIELDS_VAR", "value": f'"{config}"'}
                )
