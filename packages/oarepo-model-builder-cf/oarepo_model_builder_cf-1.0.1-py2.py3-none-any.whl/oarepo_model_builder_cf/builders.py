from oarepo_model_builder.builders import process
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.validation import InvalidModelException
from munch import unmunchify


class InvenioRecordCFBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_cf"
    class_config = "record-class"
    template = "record_cf"

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.cf = schema.current_model.get("custom-fields", [])

    def process_template(self, python_path, template, **extra_kwargs):
        if self.cf:
            return super().process_template(
                python_path,
                template,
                **{**extra_kwargs, "custom_fields": self.cf},
            )
