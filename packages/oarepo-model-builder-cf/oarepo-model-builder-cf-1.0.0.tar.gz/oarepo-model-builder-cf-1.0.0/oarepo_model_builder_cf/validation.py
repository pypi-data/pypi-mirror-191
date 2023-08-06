import marshmallow as ma
from marshmallow.exceptions import ValidationError
from marshmallow import fields as fields


class CFSchema(ma.Schema):
    element = fields.String(required=False)
    config = fields.String(required=True)

    class Meta:
        unknown = ma.RAISE


class CFModelConfiguration(ma.Schema):
    custom_fields = fields.List(fields.Nested(CFSchema()), data_key="custom-fields")

    @ma.post_load(pass_many=False)
    def post_load(self, data, **kwargs):
        custom_fields = data.get("custom_fields", [])
        seen_inlined = False
        for cf in custom_fields:
            if not cf.get("element"):
                if seen_inlined:
                    raise ValidationError("Only one inline custom field is allowed")
                seen_inlined = True
        return data


VALIDATION = {"model": [CFModelConfiguration]}
