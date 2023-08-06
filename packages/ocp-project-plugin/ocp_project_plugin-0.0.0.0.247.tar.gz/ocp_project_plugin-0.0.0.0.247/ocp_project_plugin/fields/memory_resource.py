from django import forms
from django.db import models
from django.core import exceptions, validators


class MemoryResourceFormField(forms.Field):
    def __init__(
        self, *, empty_value="", **kwargs
    ):
        self.empty_value = empty_value
        super().__init__(**kwargs)
        self.validators.append(validators.ProhibitNullCharactersValidator())

    def to_python(self, value):
        """Return a string."""
        if value in self.empty_values:
            return self.empty_value

        if str(value).endswith('Mi'):
            string_value = str(value)[:-2]
            int_value = int(string_value) / 1000
            return f"{int_value}Gi"

        # Return Gigabyte
        if str(value).endswith('Gi'):
            return f"{value}"

        return value


class MemoryResourceField(models.Field):
    empty_strings_allowed = False
    default_error_messages = {
        "invalid": "“%(value)s” value must end with Mi (Megabyte) or Gi (Gigabyte)",
        "invalid_nullable": "“%(value)s” value must contain a value"
    }
    description = "Memory resource field, suffix allowed: Mi, Gi"

    def get_internal_type(self):
        return "MemoryResourceField"

    def to_python(self, value):
        # Null or empty
        if self.null and value in self.empty_values:
            return None

        # Megabyte to Gigabyte
        if str(value).endswith('Mi'):
            string_value = str(value)[:-2]
            int_value = int(string_value) / 1000
            return f"{int_value}Gi"

        # Return Gigabyte
        if str(value).endswith('Gi'):
            return f"{value}"

        raise exceptions.ValidationError(
            self.error_messages["invalid_nullable" if self.null else "invalid"],
            code="invalid",
            params={"value": value},
        )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return self.to_python(value)

    def formfield(self, **kwargs):
        form_class = MemoryResourceFormField
        defaults = {"form_class": form_class, "required": False}
        return super().formfield(**{**defaults, **kwargs})
