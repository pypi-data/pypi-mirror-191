import json
import pandas as pd

"""
Schema formats:

Field: dict
{
    "name": "firstname",
    "dtype": "string",
    "primary": False,
    "nullable": True
}

Schema format: dict

{
    version: "1",
    fields: Field[]
}

Some notes: SQLAlchemy only references precision and length when creating tables: https://docs.sqlalchemy.org/en/14/core/tutorial.html

"""


class SchemaException(Exception):
    pass


class Schema:
    def __init__(self, schema_dict: dict, validate=True):
        if "version" not in schema_dict:
            schema_dict["version"] = None

        if "fields" not in schema_dict:
            raise SchemaException("Schema is missing fields")

        self.fields = [Schema.make_field(**field) for field in schema_dict["fields"]]
        self.version = schema_dict["version"]

        if validate:
            self.validate()

    @staticmethod
    def make_field(name: str, dtype: str, nullable: bool = True, primary: bool = False, delete: bool = False):
        return {
            "name": name,
            "dtype": dtype,
            "primary": primary,
            "delete": delete,
            "nullable": nullable and not primary and not delete  # Primary keys and delete columns can't be nullable
        }

    @staticmethod
    def shorten_field(field: dict):
        representation = {
            "name": field["name"],
            "dtype": field["dtype"]
        }

        if field["primary"]:
            representation["primary"] = True

        if field["delete"]:
            representation["delete"] = True

        if "nullable" in field and not field["nullable"]:
            representation["nullable"] = False

        return representation

    @staticmethod
    def from_df(df: pd.DataFrame):
        fields = [{"name": name, "dtype": str(dtype)} for name, dtype in zip(df.columns, df.dtypes)]

        schema_dict = {
            "version": None,
            "fields": fields
        }

        return Schema(schema_dict)

    def make_df(self) -> pd.DataFrame:
        df = pd.DataFrame({field["name"]: pd.Series(dtype=field["dtype"]) for field in self.get_fields()})
        return df

    def to_json(self):
        schema_dict = {
            "version": self.version,
            "fields": [Schema.shorten_field(field) for field in self.fields]
        }

        return json.dumps(schema_dict, indent=4)

    def __str__(self):
        return self.to_json()

    def get_fields(self):
        return [Schema.make_field(**field) for field in self.fields]

    def field_names(self):
        return [field["name"] for field in self.fields]

    def dtypes(self):
        return [field["dtype"] for field in self.fields]

    def dtype_dict(self):
        return {field["name"]: field["dtype"] for field in self.fields}

    def primary_keys(self):
        return [field["name"] for field in self.fields if field["primary"]]

    def delete_columns(self):
        return [field["name"] for field in self.fields if field["delete"]]

    def compare(self, other, dtypes_only=False, do_print=True):
        differences = 0
        for own_field, other_field in zip(self.get_fields(), other.get_fields()):
            differences_here = 0

            if own_field["name"] != other_field["name"]:
                differences_here += 1

            if own_field["dtype"] != other_field["dtype"]:
                differences_here += 1

            if not dtypes_only:
                if own_field["primary"] != other_field["primary"]:
                    differences_here += 1
                if own_field["nullable"] != other_field["nullable"]:
                    differences_here += 1
                if own_field["delete"] != other_field["delete"]:
                    differences_here += 1

            if differences_here > 0:
                differences += differences_here
                if do_print:
                    print("Expected:", own_field)
                    print("Actual:", other_field)

        if differences > 0:
            if do_print:
                print(differences, "differences found")
            return False

        return True

    def matches_df(self, df: pd.DataFrame, do_print=True):
        return self.compare(Schema.from_df(df), do_print=do_print)

    def validate(self):
        has_deletes = len(self.delete_columns()) > 0
        has_pks = len(self.primary_keys()) > 0

        if has_deletes and has_pks:
            raise SchemaException("Schema can only have one of delete columns or primary keys")
