
class Display():
    """Display is an interface. It must be implemented by the supported display types."""
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert str(value) is not None
        self._name = str(value)

    def configure(self, settings):
        """configure() is called with the display setting found in the config file."""
        raise NotImplementedError('Abstract base class method called.')

    def dimensions(self):
        """dimensions() returns the rows and columns of characters supported by the display."""
        raise NotImplementedError('Abstract base class method called.')

    def message(self, lines):
        """message() diplays the provided text lines. Lines should match dimensions()."""
        raise NotImplementedError('Abstract base class method called.')

    def clear(self):
        """clear() clears the display and all pending messages."""
        raise NotImplementedError('Abstract base class method called.')

class SimulatedConsoleDisplay(Display):
    """SimulatedDisplay simulates an attached display by printing to the console."""
    def __init__(self, name):
        super().__init__(name)
        self._width = 16
        self.height = 2

    def configure(self, settings):
        self._width = int(settings.get('width', '16'))
        self._height = int(settings.get('height', '2'))

    def dimensions(self):
        return (self._width, self._height)

    def message(self, lines):
        columns, rows = self.dimensions()
        print('#{}#'.format('*' * columns))
        for _ in range(rows):
            line = lines.pop(0) if lines else ""
            print('#{0: <{width}}#'.format(line, width=columns))
        print('#{}#'.format('*' * columns))

    def clear(self):
        columns, _ = self.dimensions()
        print('\n#{0: <{width}}#\n'.format(" display clear ", width=columns))
