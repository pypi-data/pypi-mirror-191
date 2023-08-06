from rpithingamajigs.lcdd.client.lcdd_client import LcddClient

class IgnorantLcddClient(LcddClient):
    '''IgnorantLcddClient acts like LcddClient, but the operational methods do not require a connection.
    The user will still have to ignore the RuntimeError raised by connect().'''
    def __init__(self):
        super().__init__()

    def message(self, lines, duration=-1):
        if self.is_connected():
            super().message(lines, duration)

    def clear(self):
        if self.is_connected():
            super().clear()

    def dimensions(self):
        if self.is_connected():
            return super().dimensions()
        else:
            return (5,2) # return some arbitrary values

if __name__ == '__main__':
    client = IgnorantLcddClient()
    # do not connect:
    # client.connect(True)

    # now this won't do anything, but it also does not throw exceptions:
    client.clear()
    print("{} columns / {} rows".format(*client.dimensions()))
    client.message( ["Hello, World!", "This is amazing!"], 5)
