from pythonpoet.types import Builder, DeserializableType, Documentable
from pythonpoet.types.import_ import Import, ImportBuilder


class ClassField(DeserializableType):
    """
    Representation of a class field.

    .. warning::

        You shouldn't initialize this class via the `__init__`.
        Use :class:`ClassFieldBuilder` instead.

    Attributes
    ----------
    name : str
        Field's name.
    type : str
        Field's type.
    value : str or None
        Field's value.
    imports : list[:class:`Import`]
        Required field's imports.
    comments : list[str]
        Field's comments.
    """

    def __init__(
        self,
        name: str,
        type_: str,
        value: str | None,
        imports: list[Import],
        comments: list[str],
    ) -> None:
        self.name = name
        self.type = type_
        self.value = value
        self.imports = imports
        self.comments = comments

    def get_imports(self) -> str:
        imports_source_code = ""
        for import_ in self.imports:
            imports_source_code += import_.to_string()
        return imports_source_code

    def deserialize(self) -> str:
        field_source_code = f"\t{self.name}: {self.type}"
        if self.value is not None:
            field_source_code += f" = {self.value}"
        return (
            f"{field_source_code}\n"
            + Documentable.generate_comments_source(self.comments)
            + "\n"
        )

    def __repr__(self) -> str:
        return (
            f"ClassField<name={self.name}, type={self.type}, "
            f"value={self.value}, imports={self.imports}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class ClassFieldBuilder(Builder, Documentable):
    """
    Builder for the :class:`ClassField`.

    Attributes
    ----------
    name : str or None, default: None
        Field's name.
    type : str or None, default: None
        Field's type.
    value : str or None, default: None
        Field's value.
    imports : list[:class:`Import`]
        Required field's imports.
    """

    def __init__(self) -> None:
        super(Builder, self).__init__()
        super(Documentable, self).__init__()

        self.name: str | None = None
        self.type: str | None = None
        self.value: str | None = None
        self.imports: list[Import] = []

    def set_name(self, name: str) -> "ClassFieldBuilder":
        """
        Sets field's name.

        Parameters
        ----------
        name : str
            New name of the field.

        Returns
        -------
        :class:`ClassFieldBuilder`
            Updated builder's instance.
        """
        self.name = name
        return self

    def set_type(
        self, type_: str, import_: ImportBuilder = None
    ) -> "ClassFieldBuilder":
        """
        Sets field's type.

        Parameters
        ----------
        import_ : :class:`Import`, optional, default: None
            Import path for the type (if it isn't built-in).
        type_ : :class:`str`
            New type of the field.

        Returns
        -------
        :class:`ClassFieldBuilder`
            Updated builder's instance.
        """
        self.type = type_
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    def set_value(
        self, value: str, import_: ImportBuilder = None
    ) -> "ClassFieldBuilder":
        """
        Sets a new field's value.

        Parameters
        ----------
        import_ : :class:`ImportBuilder`, optional, default: None
            Import path for the value.
        value : str
            New field's value.

        Returns
        -------
        :class:`ClassFieldBuilder`
            Updated builder's instance.
        """
        self.value = value
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    def build(self) -> ClassField:
        if self.name is None:
            raise ValueError("Field's name cannot be None.")
        elif self.type is None:
            raise ValueError("Field's type cannot be None.")

        return ClassField(self.name, self.type, self.value, self.imports, self.comments)
