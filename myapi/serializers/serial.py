from dataclasses import dataclass
from datetime import datetime
from pyparsing import Opt
from serpyco import SchemaBuilder , AbstractValidator
from serpyco.validator import ValidationError
from typing import Optional
@dataclass
class ID:
    id : Optional[int]

@dataclass
class CreatedAt:
    created_at : Optional[datetime]

class Validator(AbstractValidator):

    def __init__(self, schema_builder: SchemaBuilder) -> None:
        super().__init__(schema_builder)

    def validate(self, data:dict, many: bool = False) -> None:
        prop = data.keys()
        valid_prop = self._schema['properties'].keys()
        print(prop)
        print(valid_prop)
        for i in prop :
            print(i)
            if i not in valid_prop:
                raise ValidationError(msg="Invalid data") 

    def validate_json(self, json_string: str, many: bool = False) -> None:
        self.validate(json_string,many)



