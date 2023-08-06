from os import PathLike
from typing import TypeVar

from .types import BarTemplateSpec, BarSpec, JSONText


# Bar = TypeVar('Bar')
BarTemplate = TypeVar('BarTemplate')


class BarTemplate:
    '''
    Build and transport Bar configs between files, dicts and command line args.

    :param options: Optional :class:`BarTemplateSpec` parameters that override those of `defaults`
    :type options: :class:`BarTemplateSpec`

    :param defaults: Parameters to use by default,
        defaults to :attr:`Bar._default_params`
    :type defaults: :class:`dict`

    .. note:: `options` and `defaults` must be :class:`dict` instances of form :class:`BarTemplateSpec`

    '''

    def __init__(self,
        options: BarTemplateSpec = {},
        defaults: BarTemplateSpec = None,
    ) -> None:
        if defaults is None:
            self.defaults = Bar._default_params.copy()
        else:
            self.defaults = defaults.copy()
        self.options = options.copy()

        self.bar_spec = self.defaults | self.options
        self.file = None
        debug = self.options.pop('debug', None) or DEBUG

    def __repr__(self) -> str:
        cls = type(self).__name__
        file = self.file
        maybe_file = f"{file=}, " if file else ""
        bar_spec = self.bar_spec
        return f"<{cls} {maybe_file}{bar_spec=}>"

    @classmethod
    def from_file(cls: BarTemplate,
        file: PathLike = None,
        defaults: BarTemplateSpec = None,
        overrides: BarTemplateSpec = {}
    ) -> BarTemplate:
        '''
        Return a new :class:`BarTemplate` from a config file path.

        :param file: The filepath to the config file,
            defaults to ``'~/.mybar.json'``
        :type file: :class:`PathLike`

        :param defaults: The base :class:`BarTemplateSpec` dict whose
            params the new :class:`BarTemplate` will override,
            defaults to :attr:`Bar._default_params`
        :type defaults: :class:`BarTemplateSpec`

        :param overrides: Additional param overrides to the config file
        :type overrides: :class:`BarTemplateSpec`

        :returns: A new :class:`BarTemplate` instance
        :rtype: :class:`BarTemplate`
        :raises: :class:`AskWriteNewFile` to ask the user for write
            permission when the requested file path does not exist
        '''
        if defaults is None:
            defaults = Bar._default_params
        overrides = overrides.copy()

        file_given = True if file or 'config_file' in overrides else False
        if file is None:
            file = overrides.pop('config_file', CONFIG_FILE)

        file_spec = {}
        absolute = os.path.abspath(os.path.expanduser(file))
        if os.path.exists(absolute):
            file_spec, text = cls.read_file(absolute)
        elif file_given:
            raise AskWriteNewFile(absolute)
        else:
            cls.write_file(absolute, overrides, defaults)

        options = file_spec | overrides
        t = cls(options, defaults)
        t.file = absolute
        return t

    @staticmethod
    def read_file(file: PathLike) -> tuple[BarTemplateSpec, JSONText]:
        '''
        Read a given config file.
        Convert its JSON contents to a dict and return it along with the
        raw text of the file.

        :param file: The file to convert
        :type file: :class:`PathLike`
        :returns: The converted file and its raw text
        :rtype: tuple[:class:`BarTemplateSpec`, :class:`JSONText`]
        '''
        with open(file, 'r') as f:
            data = json.load(f)
            text = f.read()
        return data, text

    @staticmethod
    def write_file(
        file: PathLike,
        obj: BarTemplateSpec = {},
        defaults: BarSpec = None
    ) -> None:
        '''Write :class:`BarTemplateSpec` params to a JSON file.

        :param file: The file to write to
        :type file: :class:`PathLike`
        :param obj: The :class:`BarTemplateSpec` to write
        :type obj: :class:`BarTemplateSpec`, optional
        :param defaults: Any default parameters that `obj` should override,
            defaults to :attr:`Bar._default_params`
        :type defaults: :class:`BarSpec`
        '''
        if defaults is None:
            defaults = Bar._default_params.copy()

        obj = obj.copy()
        obj.pop('config_file', None)
        obj = defaults | obj

        dft_fields = Field._default_fields.copy()

        for name, field in dft_fields.items():
            new = dft_fields[name] = field.copy()
            for param in ('name', 'func', 'setup'):
                try:
                    del new[param]
                except KeyError:
                    pass

        obj['field_definitions'] = dft_fields

        with open(os.path.expanduser(file), 'w') as f:
            json.dump(obj, f, indent=4, ) #separators=(',\n', ': '))



