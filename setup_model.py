import os
import sys

FIELD_TYPES = {
    "c": "models.CharField(max_length={max_length}, {null_blank})",
    "b": "models.BooleanField(default={default})",
    "f": "models.FloatField(default={default})",
    "i": "models.IntegerField(default={default}, {null_blank})",
    "choice": "models.CharField(\n        choices={choices},\n        max_length={max_length},\n        default='{default}',\n        {null_blank}{index}\n    )" # noqa501
}


def parse_field(param):
    split_param = param.split("=", 1)
    if len(split_param) != 2:
        raise ValueError(f"Formato inválido para o campo: {param}")

    name, details = split_param

    if details.startswith("choice("):
        choice_part, rest = details[7:].split(")", 1)
        choices_list = choice_part.split(",")
        field_type = "choice"
        parts = rest.split(",") if rest else []
    else:
        parts = details.split(",")
        field_type = parts[0]

    kwargs = {
        "max_length": "120",
        "null_blank": "",
        "default": "None",
        "index": "",
        "choices": "()"
    }

    if field_type == "choice":
        kwargs["choices"] = "(" + ", ".join(f"('{c}', '{c}')" for c in choices_list) + ")" # noqa501
        kwargs["max_length"] = parts[0] if parts else "120"
        parts = parts[1:] if len(parts) > 1 else []
    elif field_type in ["c", "f", "i"]:
        kwargs["max_length"] = parts[1] if field_type == "c" else ""
        parts = parts[2:] if field_type == "c" else parts[1:]
    else:
        parts = parts[1:]

    for p in parts:
        if p == "n":
            kwargs["null_blank"] = "null=True, blank=True,"
        elif p == "b":
            kwargs["null_blank"] = "blank=True, "
        elif p.startswith("df="):
            kwargs["default"] = p.split("=")[1]
        elif p == "index":
            kwargs["index"] = "db_index=True, "

    field_template = FIELD_TYPES[field_type]
    return f"    {name} = " + field_template.format(**kwargs)


def create_model(app_name, fields):
    model_name = app_name.capitalize()
    model_path = os.path.join("apps", app_name, "models.py")

    if not os.path.exists(model_path):
        print(f"Erro: O arquivo {model_path} não existe.")
        return

    field_definitions = "\n".join(parse_field(f) for f in fields)

    choices_definitions = ""
    for field in fields:
        if "choice(" in field:
            name, details = field.split("=", 1)
            choices_list = details.split("(")[1].split(")")[0].split(",")
            choices_definitions += f"{name.upper()}_CHOICES = (" + ", ".join(f"('{c}', '{c}')" for c in choices_list) + ")\n\n" # noqa501

    model_content = f"""from django.db import models\nfrom api_core.models import BaseModel\n\n{choices_definitions}class {model_name}(BaseModel):\n{field_definitions}\n\n    class Meta:\n        verbose_name = "{model_name}"\n        verbose_name_plural = "{model_name}s"\n        ordering = ['-id']\n\n    def __str__(self) -> str:\n        return f"{model_name} {{self.name}}"\n""" # noqa501

    with open(model_path, "w", encoding="utf-8") as f:
        f.write(model_content)

    print(f"Modelo {model_name} gerado com sucesso no arquivo {model_path}.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python setup_model.py <app_name> <field1=type,max_length,n,b,...> <field2=...>") # noqa501
    else:
        create_model(sys.argv[1], sys.argv[2:])

# python setup_model.py evaluation 'desc=c,225,n,b' 'published=b,df=False' 'status_user_type=choice(user,admin,platform)120,n,index' 'evaluation=i,df=0,n,b' 'rate=f,df=0' # noqa501
