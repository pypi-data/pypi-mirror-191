import pytest

from pythonpoet import DecoratorBuilder, ImportBuilder


class TestDecorator:
    def test_decorator_deserialization(self):
        builder = DecoratorBuilder().set_name("awaitable")
        result = builder.build()

        assert result.deserialize() == "@awaitable\n"
        assert len(result.get_imports()) == 0

    def test_decorator_deserialization_import(self):
        builder = (
            DecoratorBuilder()
            .set_name("dataclass")
            .set_import(
                ImportBuilder()
                .set_class_name("dataclass")
                .set_module_name("dataclasses")
            )
        )
        result = builder.build()

        assert result.deserialize() == "@dataclass\n"
        assert len(result.get_imports()) == 34

    def test_decorator_deserialization_arguments(self):
        builder = DecoratorBuilder().set_name("awaitable").add_argument("wait", True)
        result = builder.build()

        assert result.deserialize() == "@awaitable(wait=True,)\n"
        assert len(result.get_imports()) == 0

    def test_decorator_builder_build_exception(self):
        builder = DecoratorBuilder()
        with pytest.raises(ValueError):
            builder.build()
