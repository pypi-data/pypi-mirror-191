import logging
import time

from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import HTML, to_formatted_text, fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout import BufferControl, ConditionalContainer
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style

from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.controls import FormattedTextControl

from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.widgets import TextArea

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


_log = logging.getLogger("katcpcli.UI")

# Style.
tui_style = Style(
    [
        ("output-field", "bg:#000044 #ffffff"),
        ("status", "bg:#000000 #ffffff"),
        ("line", "#004400"),
        ("connected", "fg:#00cf00"),
        ("disconnected", "fg:#cf0000"),
    ]
)

prompt_style = Style(
    [
        ("output-field", "bg:#000044 #ffffff"),
        ("status", "bg:#000000 #ffffff"),
        ("line", "#004400"),
        ("connected", "bg:#00cf00"),
        ("disconnected", "bg:#cf0000"),
    ]
)


def print_help(dispatcher, kb):
    """
    write help to the dispatcher
    """
    dispatcher.output_stream("")
    dispatcher.output_stream(
        "The following commands and key bindings are supported by the application. [?] can be used as a shortcut for katpcmd."
    )
    dispatcher.output_stream("")
    dispatcher.output_stream(HTML("<b>Commands:</b>"))
    for c, v in dispatcher.commands.items():
        desc = v.__doc__.lstrip().rstrip()
        dispatcher.output_stream(f"{c:15} - {desc}")

    dispatcher.output_stream("")
    dispatcher.output_stream(HTML("<b>Key Bindings:</b>"))
    for b in kb.bindings:
        keys = ",".join(k.value for k in b.keys)
        desc = b.handler.__doc__

        keys = keys.replace("escape,", "alt+")

        dispatcher.output_stream(f"{keys:15} - {desc}")


def _bouble_gen():
    while True:
        for s in [".", "o", "O"]:
            yield s


bouble = _bouble_gen()


def bottom_toolbar(dispatcher):
    """
    Render right bottom toolbar.
    """
    style = "disconnected"
    host = "-"
    port = "-"
    if dispatcher.katcpclient:
        host = dispatcher.katcpclient.host
        port = dispatcher.katcpclient.port
        if dispatcher.katcpclient.is_connected:
            style = "connected"

    # Indicate that a task is being processed
    if dispatcher.running_tasks:
        active = next(bouble)
    else:
        active = " "

    return HTML(
        f"<b>KATCP cli</b> connected to (<{style}><b>{host}:{port}</b></{style}>) [{active}] -  Use [Ctrl-C] to terminate, [F1] for help"
    )


def rprompt():
    """
    Render right prompt.
    """
    return HTML(f"<style color='green'>{time.ctime()}</style>")


class Buffer_(Buffer):
    """
    Buffer that handles formatted text. See prompt_toolkit issue #711
    https://github.com/prompt-toolkit/python-prompt-toolkit/issues/711
    """

    def write(self, data):
        """
        Write data as a new line to the buffer. Mimics the stream interface to enable usage in log handler.
        """
        if isinstance(data, HTML):
            line = data.value
        else:
            line = str(data)

        self.text += line.rstrip() + "\n"

        if not get_app().layout.has_focus(self):
            self.cursor_position = len(self.text)

    def flush(self):
        """
        No op as flushing is handled by toolkit.
        """


class FormatText(Processor):  # pylint: disable=too-few-public-methods
    """
    Formatter for buffer to handle formatted text. See prompt_toolkit issue #711
    https://github.com/prompt-toolkit/python-prompt-toolkit/issues/711
    """

    def apply_transformation(self, transformation_input):
        try:
            fragments = to_formatted_text(
                HTML(fragment_list_to_text(transformation_input.fragments))
            )
        except Exception as E:
            return Transformation(transformation_input.fragments)
        return Transformation(fragments)


class FSApplicationUI:
    """
    User-interface for full screen application
    """

    def __init__(self, completer, history):

        self.show_log_window = False

        self.bottom_toolbar_generator = None

        # The Buffers for the log and output stream
        self.log_field = Buffer_()
        self.output_field = Buffer_()

        self.input_field = TextArea(
            height=1,
            completer=completer,
            auto_suggest=AutoSuggestFromHistory(),
            history=history,
            prompt=">>> ",
            style="class:input-field",
            multiline=False,
            wrap_lines=False,
        )

        # Building the application layout
        container = HSplit(
            [
                Window(
                    FormattedTextControl("Log Informs (Toggle using F2)"),
                    style="class:status",
                    char="-",
                    height=1,
                ),
                ConditionalContainer(
                    content=Window(
                        BufferControl(
                            self.log_field,
                            input_processors=[FormatText()],
                            include_default_input_processors=True,
                        ),
                        height=6,
                        wrap_lines=True,
                    ),
                    filter=Condition(lambda: self.show_log_window),
                ),
                Window(
                    FormattedTextControl("Output"),
                    style="class:status",
                    height=1,
                    char="-",
                ),
                Window(
                    BufferControl(
                        self.output_field,
                        input_processors=[FormatText()],
                        include_default_input_processors=True,
                    ),
                    wrap_lines=True,
                ),
                VSplit(
                    [
                        Window(
                            FormattedTextControl(self.bottom_toolbar),
                            style="class:status",
                            height=1,
                        ),
                        Window(
                            FormattedTextControl(rprompt),
                            style="class:status",
                            height=1,
                            align=WindowAlign.RIGHT,
                            dont_extend_width=True,
                        ),
                    ]
                ),
                self.input_field,
            ]
        )

        self.layout = Layout(container, focused_element=self.input_field)

        # TUI logs to log window
        logging.root.handlers.clear()
        sh = logging.StreamHandler(stream=self.log_field)
        sh.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(filename)s:"
                "%(lineno)s - %(levelname)s - %(message)s"
            )
        )
        logging.getLogger('').addHandler(sh)

    def bottom_toolbar(self):
        """
        Return bottom toolbar content
        """
        if self.bottom_toolbar_generator is None:
            return ""
        return self.bottom_toolbar_generator()
