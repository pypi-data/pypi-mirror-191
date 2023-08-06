import click
from rpithingamajigs.lcdd.client.lcdd_client import LcddClient

@click.command()
@click.option('--duration', '-d', required=False, type=int, help='Minimum duration that the message is displayed.')
@click.option('--sessionbus/--no-sessionbus', '-s', required=False, default=False, help='Use the DBUS session bus instead of the system bus.')
@click.argument('lines', nargs=-1)
def lcdd_client(duration, lines, sessionbus):
    """LCDD client provides a command line interface to the LCDD display service."""
    client = LcddClient()
    try:
        client.connect(sessionbus)
        client.message(lines, duration or -1)
    except Exception as e:
        print(str(e))
        raise click.Abort(str(e))
    finally:
        client.disconnect()
if __name__ == '__main__':
    lcdd_client()  # pylint: disable=no-value-for-parameter
