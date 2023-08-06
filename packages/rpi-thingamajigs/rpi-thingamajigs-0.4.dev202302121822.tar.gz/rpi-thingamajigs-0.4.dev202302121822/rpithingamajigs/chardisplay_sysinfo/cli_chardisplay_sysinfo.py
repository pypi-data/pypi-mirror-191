import click
from rpithingamajigs.lcdd.client.lcdd_client import LcddClient
from rpithingamajigs.chardisplay_sysinfo.chardisplay_sysinfo import queue_messages
from time import sleep

@click.command()
@click.option('--duration', '-d', required=False, type=int, default = 2, help='Minimum duration that the message is displayed (default: 2).')
@click.option('--period', '-p', required=False, type=int, default = 60, help='Period between messages (default: 60).')
@click.option('--sessionbus/--no-sessionbus', '-s', required=False, default=False, help='Use the DBUS session bus instead of the system bus.')
def chardisplay_sysinfo(duration, period, sessionbus):
    """chardisplay_sysinfo periodically displays system information on the LCDD display."""
    client = LcddClient()
    try:
        client.connect(sessionbus)
        while(True):
            queue_messages(client, duration)
            sleep(period)
    except Exception as e:
        print(str(e))
        raise click.Abort(str(e))
    finally:
        client.disconnect()

if __name__ == '__main__':
    chardisplay_sysinfo()  # pylint: disable=no-value-for-parameter
