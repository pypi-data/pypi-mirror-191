import pytest

from pythonpoet import ClassBuilder, ClassFieldBuilder, ImportBuilder
from pythonpoet.types.class_ import (
    ClassConstructorBuilder,
    ClassConstructorArgumentBuilder,
)
from pythonpoet.types.method import MethodBuilder


class TestClass:
    def test_class_deserialization(self):
        builder = ClassBuilder().set_name("User")
        result = builder.build()

        assert result.deserialize() == "class User:\n\n"
        assert len(result.get_imports()) == 0

    def test_class_deserialization_methods(self):
        builder = (
            ClassBuilder()
            .set_name("User")
            .add_method(
                MethodBuilder()
                .set_name("print_hello")
                .set_source_code('print("Hello from User class!")')
            )
        )
        result = builder.build()

        assert (
                result.deserialize() == "class User:\n\n\tdef print_hello():"
                                        '\n\t\tprint("Hello from User class!")\n\n\t'
        )
        assert len(result.get_imports()) == 0

    def test_class_deserialization_extends(self):
        builder = (
            ClassBuilder()
            .set_name("User")
            .add_extends(
                "ABC", ImportBuilder().set_class_name("ABC").set_module_name("abc")
            )
        )
        result = builder.build()

        assert result.deserialize() == "class User(ABC):\n\n"
        assert len(result.get_imports()) == 20

    def test_class_deserialization_fields(self):
        builder = (
            ClassBuilder()
            .set_name("User")
            .add_field(ClassFieldBuilder().set_name("username").set_type(str.__name__))
        )
        result = builder.build()

        assert result.deserialize() == "class User:\n\n\tusername: str\n\n"
        assert len(result.get_imports()) == 0

    def test_class_deserialization_comments(self):
        builder = (
            ClassBuilder().set_name("User").add_comment("This is a simple comment")
        )
        result = builder.build()

        assert (
                result.deserialize()
                == 'class User:\n\t"""\n\tThis is a simple comment\n\t"""\n\n'
        )
        assert len(result.get_imports()) == 0

    def test_class_deserialization_constructor(self):
        builder = (
            ClassBuilder()
            .set_name("User")
            .set_constructor(
                ClassConstructorBuilder().add_argument(
                    ClassConstructorArgumentBuilder().set_name("name").set_type("str")
                )
            )
        )
        result = builder.build()

        assert (
                result.deserialize()
                == "class User:\n\n\tdef __init__(name: str, ):\n\t\tself.name = name\n"
        )
        assert len(result.get_imports()) == 0

    def test_class_builder_build_exception(self):
        builder = ClassBuilder()
        with pytest.raises(ValueError):
            builder.build()
