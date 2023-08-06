from logging import StreamHandler
import click

class ClickEchoHandler(StreamHandler):
    def __init__(self, **kwargs):
        StreamHandler.__init__(self, **kwargs)

    def emit(self, record):
        fg=''
        if record.levelname=="CRITICAL":
            fg='bright_red'
        elif record.levelname=="ERROR":
            fg='red'
        elif record.levelname=="WARNING":
            fg='yellow'
        elif record.levelname=="INFO":
            fg='blue'
        else: # NOTSET or DEBUG
            pass

        try:
            msg = self.format(record)
            click.secho(msg, fg=fg)
        except Exception:
            self.handleError(record)
