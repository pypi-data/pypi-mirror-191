from strenum import LowercaseStrEnum
from craft_ai_sdk.utils import remove_none_values


class INPUT_OUTPUT_TYPES(LowercaseStrEnum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"
    ARRAY = "array"
    FILE = "file"


class Input:
    def __init__(
        self, name, data_type, description=None, is_required=None, default_value=None
    ):
        self.name = name
        self.data_type = data_type
        self.description = description
        self.is_required = is_required
        self.default_value = default_value

    def to_dict(self):
        input = {
            "name": self.name,
            "data_type": self.data_type,
            "description": self.description,
            "is_required": self.is_required,
            "default_value": self.default_value,
        }
        return remove_none_values(input)


class Output:
    def __init__(self, name, data_type, description=None):
        self.name = name
        self.data_type = data_type
        self.description = description

    def to_dict(self):
        output = {
            "name": self.name,
            "data_type": self.data_type,
            "description": self.description,
        }

        return remove_none_values(output)


class DeploymentInputMapping:
    def __init__(
        self,
        step_input_name,
        endpoint_input_name=None,
        environment_variable_name=None,
        is_required=None,
        default_value=None,
        constant_value=None,
        is_null=None,
    ):
        self.step_input_name = step_input_name
        self.endpoint_input_name = endpoint_input_name
        self.environment_variable_name = environment_variable_name
        self.is_required = is_required
        self.default_value = default_value
        self.constant_value = constant_value
        self.is_null = is_null

    def to_dict(self):
        input_mapping_dict = {
            "step_input_name": self.step_input_name,
            "endpoint_input_name": self.endpoint_input_name,
            "environment_variable_name": self.environment_variable_name,
            "is_required": self.is_required,
            "default_value": self.default_value,
            "constant_value": self.constant_value,
            "is_null": self.is_null,
        }

        return remove_none_values(input_mapping_dict)


class DeploymentOutputMapping:
    def __init__(self, step_output_name, endpoint_output_name=None, is_null=None):
        self.step_output_name = step_output_name
        self.endpoint_output_name = endpoint_output_name
        self.is_null = is_null

    def to_dict(self):
        output_mapping_dict = {
            "step_output_name": self.step_output_name,
            "endpoint_output_name": self.endpoint_output_name,
            "is_null": self.is_null,
        }

        return remove_none_values(output_mapping_dict)
