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




class NestValidator(AbstractValidator):
    def __init__(self,schema_builder:SchemaBuilder) -> None:
        super().__init__(schema_builder)

    def validate(self, data: dict, nest:dict, many: bool = False) -> None:
        prop =data.keys()
        other = nest
        valid_prop = self._schema['properties'].keys()
        for i in prop :
            if i not in other:
                if i not in valid_prop:
                    print("Error")
                    raise ValidationError(msg="Invalid data")
            else :
                if i in valid_prop:
                    print(" Check")
                    for q in QuestionBaseValid.__subclasses__():
                        print(q.__name__.lower().replace("valid",""))
                        if data['type'].lower() in q.__name__.lower() :
                            print(GQValid)
                            schema = SchemaBuilder(GQValid)
                            x = Validator(schema_builder=schema)
                            x.validate(data=data[i])
                else :
                    print(" Check2")
                    raise ValidationError(msg="Invalid nested data")
        return True
        return super().validate(data, many)
    def validate_json(self, json_string: str, many: bool = False) -> None:
        return super().validate_json(json_string, many)