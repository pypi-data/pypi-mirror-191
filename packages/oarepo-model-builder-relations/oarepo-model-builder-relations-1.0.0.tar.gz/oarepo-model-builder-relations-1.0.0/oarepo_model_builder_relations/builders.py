from oarepo_model_builder.builders import process
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.validation import InvalidModelException
from munch import unmunchify
from oarepo_model_builder.utils.python_name import convert_name_to_python


class InvenioRecordRelationsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_relations"
    class_config = "record-class"
    template = "record_relations"

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.relations = []

    @process("**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        self.build_children()
        data = self.stack.top.data
        if self.stack.top.schema_element_type not in (
            "property",
            "items",
        ) or not isinstance(data, dict):
            return
        if "relation" not in data:
            return
        relation_extension = data["relation"]

        relation = {
            x.replace("-", "_"): relation_extension[x] for x in relation_extension
        }

        keys = relation["keys"]
        model_class = relation["model_class"]
        relation_classes = relation["relation_classes"]
        relation_class = relation["relation_class"]
        relation_args = relation["relation_args"]
        pid_field = relation["pid_field"]

        keys = [x if isinstance(x, str) else x.key for x in keys]
        relation_args.setdefault("keys", repr(keys))

        if pid_field or model_class:
            relation_args.setdefault("pid_field", pid_field or f"{model_class}.pid")

        if not relation_class:
            relation["relation_class"] = self._get_relation_class(
                relation_classes, relation, relation_args
            )
        relation.setdefault("path", self._property_path(self.stack))
        relation = {k.replace("-", "_"): v for k, v in unmunchify(relation).items()}
        relation["relation_args"] = {
            k.replace("-", "_"): v for k, v in relation["relation_args"].items()
        }
        relation["name"] = convert_name_to_python(relation["name"])
        for suffix in ("", *[f"_{i}" for i in range(1, 100)]):
            name = relation["name"] + suffix
            for rr in self.relations:
                if name == rr["name"]:
                    break
            else:
                relation["name"] = name
                break

        self.relations.append(relation)

    def _get_relation_class(self, relation_classes, relation, relation_args):
        # check if not path of an array
        array_paths = []
        path = ""
        top_is_array = False
        for stack_entry in self.stack.stack:
            if stack_entry.schema_element_type == "property":
                if path:
                    path = f"{path}."
                path += stack_entry.key

            if stack_entry.schema_element_type != "items":
                top_is_array = False
            else:
                array_paths.append(path)
                top_is_array = True
        if len(array_paths) > 1:
            # array inside array => return nested array relation
            if top_is_array:
                relation_args.setdefault(
                    "relation_field", repr(path[len(array_paths[0]) + 1 :])
                )
                relation.setdefault("path", array_paths[0])
                return relation_classes["nested-array"]

            raise InvalidModelException(
                "Related items in double arrays are not supported yet"
            )
        # not in array => return single relation
        if not array_paths:
            return relation_classes["single"]

        # array itself => return list relation
        if top_is_array:
            return relation_classes["list"]
        # inside an array => return nested relation
        relation_args.setdefault(
            "relation_field", repr(path[len(array_paths[0]) + 1 :])
        )
        relation.setdefault("path", array_paths[0])
        return relation_classes["nested"]

    def process_template(self, python_path, template, **extra_kwargs):
        if self.relations:
            return super().process_template(
                python_path,
                template,
                **{**extra_kwargs, "invenio_relations": self.relations},
            )

    def _property_path(self, stack):
        path = []
        for entry in stack:
            if entry.schema_element_type == "property":
                path.append(entry.key)
        return ".".join(path)
