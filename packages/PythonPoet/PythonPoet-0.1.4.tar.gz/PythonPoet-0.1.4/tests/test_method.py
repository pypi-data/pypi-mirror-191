import pytest

from pythonpoet.types.method import MethodBuilder


class TestMethod:
    def test_method_deserialization(self):
        builder = MethodBuilder().set_name("print_name")

        result = builder.build()
        assert result.deserialize() == "def print_name():\n\t\tpass\n"

    def test_method_deserialization_return_type(self):
        builder = MethodBuilder().set_name("print_name").set_return_type(str)

        result = builder.build()
        assert result.deserialize() == "def print_name() -> str:\n\t\tpass\n"

    def test_method_deserialization_source(self):
        builder = (
            MethodBuilder()
            .set_name("print_name")
            .set_return_type(str)
            .set_source_code('return "Hello"')
        )

        result = builder.build()
        assert result.deserialize() == 'def print_name() -> str:\n\t\treturn "Hello"\n'

    def test_method_deserialization_arguments(self):
        builder = (
            MethodBuilder()
            .set_name("print_name")
            .set_return_type(str)
            .set_source_code("return name")
            .add_argument("name", "str")
        )

        result = builder.build()
        assert (
                result.deserialize()
                == "def print_name(name: str) -> str:\n\t\treturn name\n"
        )

    def test_method_deserialization_async(self):
        builder = (
            MethodBuilder()
            .set_name("say_hello")
            .set_async()
            .set_source_code("print('Hello!')")
        )

        result = builder.build()
        assert result.deserialize() == "async def say_hello():\n\t\tprint('Hello!')\n"

    def test_method_builder_build_exception(self):
        builder = MethodBuilder()
        with pytest.raises(ValueError):
            builder.build()
