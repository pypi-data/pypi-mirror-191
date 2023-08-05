"""Python 2/3 compatible functions."""


def remove_symbols(text, symbols):
    """Remove from string given symbols."""
    for symbol in symbols:
        text = text.replace(symbol, '')

    return text


def load_module_by_path(path):
    """Load py module by file path.

    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    """
    # construct package name from module file path
    # drop file path specific symbols
    name = remove_symbols(path, '/\\:.')

    try:  # Python 3.5+
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)  # pylint: disable=no-member
        py_module = importlib.util.module_from_spec(spec)  # pylint: disable=no-member
        spec.loader.exec_module(py_module)
    except ImportError:  # Python 3.4 3.3
        try:
            from importlib.machinery import SourceFileLoader
            py_module = SourceFileLoader(  # pylint: disable=no-value-for-parameter,deprecated-method
              name, path
            ).load_module()
        except ImportError:  # Python 2
            import imp
            py_module = imp.load_source(name, path)

    return py_module


def win1251(text):
    """Convert to 1251 encoding."""
    return to_str(text).encode('windows-1251')


def to_str(text):
    """Convert to unicode."""
    try:  # Python 2
        return text.decode('utf-8')
    except AttributeError:
        # Python 3.5+
        return text


def is_contains(text_1251, utf8_string):
    """Check text with 1251 encoding contains string with utf-8 encoding."""
    try:  # Python 2
        return win1251(utf8_string) in text_1251
    except TypeError:
        # Python 3.5+
        return win1251(utf8_string) in text_1251.encode('windows-1251')


def replace1251(text_1251, utf8_source, utf8_dest):
    """Replace utf8 source string to utf8 destination string in 1251 encoding text."""
    try:  # Python 2
        return text_1251.replace(win1251(utf8_source), win1251(utf8_dest))
    except TypeError:
        # Python 3.5+
        return text_1251.encode('windows-1251').replace(win1251(utf8_source), win1251(utf8_dest))


def gen_next(generator):
    """Next method for generator."""
    try:  # Python 2
        return generator.next()
    except AttributeError:
        # Python 3.5+
        return generator.__next__()


def open_text_file(file_path, mode, encoding):
    """Open text file with encoding."""
    try:  # Python 3.5+
        fhandle = open(file_path, mode + 't', encoding=encoding)
    except TypeError:
        # Python 2
        fhandle = open(file_path, mode + 'b')

    return fhandle


def super23(self):
    """Class super. In py2 works with new-style classes (object).

    https://stackoverflow.com/questions/43778914/python3-using-super-in-eq-methods-raises-runtimeerror-super-class
    https://stackoverflow.com/questions/1713038/super-fails-with-error-typeerror-argument-1-must-be-type-not-classobj-when
    """
    return super(self.__class__, self)
