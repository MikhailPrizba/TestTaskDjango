# fields.py
from drf_extra_fields.fields import Base64ImageField


class Base64ImageFieldWithSwagger(Base64ImageField):
    class Meta:
        swagger_schema_fields = {
            "type": "string",
            "title": "Photo",
            "description": "Base64 encoded image",
            "read_only": False,
        }
