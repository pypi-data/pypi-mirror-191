from pythonpoet.types import Builder, DeserializableType, Documentable
from pythonpoet.types.decorator import Decoratorable, Decorator
from pythonpoet.types.field import ClassFieldBuilder, ClassField
from pythonpoet.types.import_ import Import, ImportBuilder
from pythonpoet.types.method import Method, MethodBuilder


def _generate_decorators(decorators: list[Decorator]) -> str:
    decorators_source_code = ""
    for decorator in decorators:
        decorators_source_code += decorator.deserialize()
    return decorators_source_code


def _generate_class_header(class_name: str, extends: str, comments: str) -> str:
    if len(extends) == 0:
        class_header = f"class {class_name}:\n"
    else:
        class_header = f"class {class_name}({extends}):\n"
    return f"{class_header}{comments}\n"


def _generate_class_fields(fields: list[ClassField]) -> str:
    fields_source_code = ""
    for field in fields:
        fields_source_code += field.deserialize()
    return fields_source_code


def _generate_class_methods(methods: list[Method]) -> str:
    methods_source_code = "\t"
    for method in methods:
        methods_source_code += f"{method.deserialize()}\n\t"
    return methods_source_code


class ClassConstructorArgument(DeserializableType):
    """
    Representation of a class' constructor's argument.

    .. warning::

        You shouldn't initialize this class via the `__init__`.
        Use :class:`ClassConstructorArgumentBuilder` instead.

    Attributes
    ----------
    name : str
        Argument's name.
    type_ : str
        Argument's type.
    value : str or None
        Argument's value.
    imports : list[:class:`Import`]
        Required argument's type.
    """

    def __init__(
            self, name: str, type_: str, value: str | None, imports: list[Import]
    ) -> None:
        self.name = name
        self.type_ = type_
        self.value = value
        self.imports = imports

    def get_imports(self) -> str:
        imports = ""
        for import_ in self.imports:
            imports += import_.to_string()
        return imports

    def deserialize(self) -> str:
        deserialized = f"{self.name}: {self.type_}"
        if self.value is not None:
            deserialized += f" = {self.value}"
        return deserialized

    def __repr__(self) -> str:
        return (
            f"ClassConstructorArgument<name={self.name}, type={self.type_}, "
            f"value={self.value}, imports={self.imports}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class ClassConstructorArgumentBuilder(Builder):
    """
    Builder for the :class:`ClassConstructorArgument`.

    Attributes
    ----------
    name : str
        Argument's name.
    type_ : str
        Argument's type.
    value : str or None
        Argument's value.
    imports : list[:class:`Import`]
        Required argument's type.
    """

    def __init__(self) -> None:
        self.name: str | None = None
        self.type_: str | None = None
        self.value: str | None = None
        self.imports: list[Import] = []

    def set_name(self, name: str) -> "ClassConstructorArgumentBuilder":
        """
        Sets a name for this argument.

        Parameters
        ----------
        name : str
            Argument's name.

        Returns
        -------
        :class:`ClassConstructorArgumentBuilder`
            Updated builder's instance.
        """
        self.name = name
        return self

    def set_type(
            self, type_: str, import_: ImportBuilder = None
    ) -> "ClassConstructorArgumentBuilder":
        """
        Sets a type for this argument.

        Parameters
        ----------
        type_ : str
            Argument's type.
        import_ : :class:`ImportBuilder` or None
            Import required for this type, if it's not built-in.

        Returns
        -------
        :class:`ClassConstructorArgumentBuilder`
            Updated builder's instance.
        """
        self.type_ = type_
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    def set_value(self, value: str) -> "ClassConstructorArgumentBuilder":
        """
        Sets value for this argument.

        Parameters
        ----------
        value : str
            Argument's value.

        Returns
        -------
        :class:`ClassConstructorArgumentBuilder`
            Updated builder's instance.
        """
        self.value = value
        return self

    def build(self) -> ClassConstructorArgument:
        if self.name is None:
            raise ValueError("Constructor's argument name cannot be None.")
        elif self.type_ is None:
            raise ValueError("Constructor's argument type cannot be None.")
        return ClassConstructorArgument(self.name, self.type_, self.value, self.imports)


class ClassConstructor(DeserializableType):
    """
    Representation of a class' constructor.

    .. warning::

        You shouldn't initialize this class via the `__init__`.
        Use :class:`ClassConstructorBuilder` instead.

    Attributes
    ----------
    arguments : list[:class:`ClassConstructorArgument`]
        List of constructor's arguments.
    """

    def __init__(self, arguments: list[ClassConstructorArgument]):
        self.arguments = arguments

    def get_imports(self) -> str:
        imports = ""
        for argument in self.arguments:
            imports += argument.get_imports()
        return imports

    def deserialize(self) -> str:
        arguments = ""
        for argument in self.arguments:
            arguments += argument.deserialize() + ", "
        header = f"def __init__({arguments}):\n"
        source = ""
        if len(self.arguments) > 0:
            for argument in self.arguments:
                source += f"\t\tself.{argument.name} = {argument.name}\n"
        else:
            source = "\t\tpass"
        return header + source

    def __repr__(self) -> str:
        return f"ClassConstructor<arguments={self.arguments}>"

    def __str__(self) -> str:
        return self.__repr__()


class ClassConstructorBuilder(Builder):
    """
    Builder for the :class:`ClassConstructor`.

    Attributes
    ----------
    arguments : list[:class:`ClassConstructorArgument`]
        List of constructor's arguments.
    """

    def __init__(self) -> None:
        self.arguments: list[ClassConstructorArgument] = []

    def add_argument(
            self, argument: ClassConstructorArgumentBuilder
    ) -> "ClassConstructorBuilder":
        """
        Adds a new argument to the list of constructor's arguments.

        Parameters
        ----------
        argument : :class:`ClassConstructorArgumentBuilder`
            Argument to be added.

        Returns
        -------
        :class:`ClassConstructorBuilder`
            Updated builder's instance.
        """
        self.arguments.append(argument.build())
        return self

    def build(self):
        return ClassConstructor(self.arguments)


class Class(DeserializableType):
    """
    Representation of a class.

    .. warning::

        You shouldn't initialize this class via the `__init__`. Use :class:`ClassBuilder` instead.

    Attributes
    ----------
    name : str
        Class' name.
    fields : list[:class:`ClassField`]
        Class' fields.
    extends : str
        Class(-es) that this class extends.
    methods : list[:class:`Method`]
        Class' methods.
    imports : list[:class:`Import`]
        Class' imports.
    decorators : list[:class:`Decorator`]
        Class' decorators.
    comments : list[str]
        Class' comments.
    constructor : :class:`ClassConstructor`
        Class' constructor.
    """

    def __init__(
            self,
            name: str,
            extends: str,
            imports: list[Import],
            fields: list[ClassField],
            decorators: list[Decorator],
            methods: list[Method],
            comments: list[str],
            constructor: ClassConstructor,
    ) -> None:
        self.name = name
        self.fields = fields
        self.extends = extends
        self.methods = methods
        self.imports = imports
        self.decorators = decorators
        self.comments = comments
        self.constructor = constructor

    def get_imports(self) -> str:
        imports = ""
        if self.constructor is not None:
            imports += self.constructor.get_imports()
        for decorator in self.decorators:
            imports += decorator.get_imports()
        for field in self.fields:
            imports += field.get_imports()
        for import_ in self.imports:
            imports += import_.to_string()
        return imports

    def deserialize(self) -> str:
        base = _generate_decorators(self.decorators) + _generate_class_header(
            self.name,
            self.extends,
            Documentable.generate_comments_source(self.comments),
        )
        if self.constructor is not None:
            base += f"\t{self.constructor.deserialize()}"
        if self.fields is not None and len(self.fields) > 0:
            base += _generate_class_fields(self.fields)
        if self.methods is not None and len(self.methods) > 0:
            base += _generate_class_methods(self.methods)
        return base

    def __repr__(self) -> str:
        return (
            f"<Class name={self.name}, decorators={self.decorators}, "
            f"fields={self.fields}, methods={self.methods}, "
            f"imports={self.imports}, extends={self.extends}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class ClassBuilder(Builder, Decoratorable, Documentable):
    """
    Builder for the :class:`Class`.

    Attributes
    ----------
    name : str or None, default: None
        Class' name.
    extends : list[str]
        Class(-es) that this class extends.
    methods : list[:class:`Method`]
        Class' methods.
    imports : list[:class:`Import`]
        Class' imports.
    fields : list[:class:`ClassField`]
        Class' fields.
    constructor : :class:`ClassConstructor` or None, default: None
        Class' constructor.
    """

    def __init__(self) -> None:
        super(Builder, self).__init__()
        super(Decoratorable, self).__init__()
        super(Documentable, self).__init__()

        self.name: str | None = None
        self.extends: list[str] = []
        self.methods: list[Method] = []
        self.imports: list[Import] = []
        self.fields: list[ClassField] = []
        self.constructor: ClassConstructor | None = None

    def set_name(self, name: str) -> "ClassBuilder":
        """
        Sets class' name.

        Parameters
        ----------
        name : str
            New name of the class.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.name = name
        return self

    def add_field(self, builder: ClassFieldBuilder) -> "ClassBuilder":
        """
        Adds a new fields from the builder.

        Parameters
        ----------
        builder : :class:`ClassFieldBuilder`
            Builder of the field to be added.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.fields.append(builder.build())
        return self

    def add_extends(self, class_: str, import_: ImportBuilder = None) -> "ClassBuilder":
        """
        Adds a new class to the list of extendable classes.

        Parameters
        ----------
        import_ : :class:`ImportBuilder`, optional, default: None
            Extendable class import.
        class_ : str
            Class to extend from.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.extends.append(class_)
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    def add_method(self, builder: MethodBuilder) -> "ClassBuilder":
        """
        Adds a new method to this class.

        Parameters
        ----------
        builder : :class:`MethodBuilder`
            Builder of the method to be added.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.methods.append(builder.build())
        return self

    def set_constructor(self, constructor: ClassConstructorBuilder) -> "ClassBuilder":
        """
        Sets class' constructor.

        Parameters
        ----------
        constructor : :class:`ClassConstructorBuilder`
            Constructor's builder to be set.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.constructor = constructor.build()
        return self

    def build(self) -> Class:
        if self.name is None:
            raise ValueError("Class' name cannot be None.")

        return Class(
            self.name,
            ",".join(self.extends),
            self.imports,
            self.fields,
            self.decorators,
            self.methods,
            self.comments,
            self.constructor,
        )
