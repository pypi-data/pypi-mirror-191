import asyncio
import time
import logging
import sys
import os

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit import print_formatted_text
from prompt_toolkit.keys import Keys 
from prompt_toolkit.key_binding.bindings.page_navigation import (
    scroll_page_up,
    scroll_page_down,
    scroll_forward,
    scroll_backward
)

from prompt_toolkit.application import Application, get_app
from prompt_toolkit.key_binding import KeyBindings


from .CommandDispatcher import CommandDispatcher
from . import UI


_log = logging.getLogger("katcpcli.app")


HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".katcpcli2_history")
REFRESH_RATE = 0.5


def create_app_and_dispatcher(prompt_application):
    """
    Create dispatcher and app, either full screen TUI or prompt app.
    """
    dispatcher = CommandDispatcher(print_formatted_text, print_formatted_text)

    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-d")
    @kb.add("c-q")
    async def _quit(*args):  # pylint: disable=unused-argument
        "Exit the application"
        _log.debug("Exit called")
        get_app().exit()

    @kb.add("f1")
    async def _help(*args):  # pylint: disable=unused-argument
        "Print help"
        UI.print_help(dispatcher, kb)

    dispatcher.commands["help"] = _help
    dispatcher.commands["quit"] = _quit
    dispatcher.commands["exit"] = _quit

    if prompt_application:
        app = prompt_app(dispatcher, kb)
    else:
        app = fs_app(dispatcher, kb)

    return dispatcher, app


def input_handler(buff, dispatcher):
    """
    Echos the input to the output stream and forward it to the dispatcher
    """
    if not buff.document.text:
        _log.debug("Received empty input")
        return
    ts = time.ctime()
    width = (get_app().output.get_size().columns or 80) - len(ts) - 4
    _log.debug("Received input, buffer width: %i", width)
    line_template = f">>> {{out:{width}}}{{ts}}\n"
    dispatcher.output_stream(line_template.format(out=buff.document.text, ts=ts))
    asyncio.create_task(dispatcher(buff.document.text))


def prompt_app(
    dispatcher, kb, history_file=HISTORY_FILE, refresh_interval=REFRESH_RATE
):
    """
    Create and return prompt application
    """

    completer = WordCompleter(words=[], WORD=True)
    completer.words = dispatcher.completion_set

    session = PromptSession(
        ">>> ",
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=completer,
        complete_in_thread=True,
        key_bindings=kb,
        rprompt=UI.rprompt,
        bottom_toolbar=lambda: UI.bottom_toolbar(dispatcher),
        refresh_interval=refresh_interval,
        style=UI.prompt_style,
        multiline=False,
    )

    session.default_buffer.accept_handler = lambda buff: input_handler(buff, dispatcher)

    return session.app


def fs_app(dispatcher, kb, history_file=HISTORY_FILE, refresh_interval=REFRESH_RATE):
    """
    Create and return full screen TUI application
    """
    completer = WordCompleter(words=[], WORD=True)
    completer.words = dispatcher.completion_set
    tui = UI.FSApplicationUI(completer, FileHistory(history_file))
    tui.bottom_toolbar_generator = lambda: UI.bottom_toolbar(dispatcher)

    dispatcher.output_stream = tui.output_field.write
    dispatcher.log_stream = tui.log_field.write

    tui.input_field.accept_handler = lambda buff: input_handler(buff, dispatcher)

    @kb.add("f2")
    def _(_):  # pylint: disable=unused-argument
        "Toggle log window visibility"
        tui.show_log_window = not tui.show_log_window

    @kb.add("pageup")
    def _(event):
        "Scroll up output window"
        w = event.app.layout.current_window
        event.app.layout.focus(tui.output_field)
        scroll_page_up(event)
        event.app.layout.focus(w)

    @kb.add("pagedown")
    def _(event):
        "Scroll up output window"
        w = event.app.layout.current_window
        event.app.layout.focus(tui.output_field)
        scroll_page_down(event)
        event.app.layout.focus(w)

    @kb.add("escape", "pageup")
    def _(event):
        "Scroll down log window"
        w = event.app.layout.current_window
        event.app.layout.focus(tui.log_field)
        scroll_page_up(event)
        event.app.layout.focus(w)

    @kb.add("escape", "pagedown")
    def _(event):
        "Scroll down log window"
        w = event.app.layout.current_window
        event.app.layout.focus(tui.log_field)
        scroll_page_down(event)
        event.app.layout.focus(w)

    @kb.add(Keys.Vt100MouseEvent)
    def _(event):
        w = event.app.layout.current_window
        event.app.layout.focus(tui.output_field)
        if event.data[4] == '4':
            scroll_backward(event)
        elif event.data[4] == '5':
            scroll_forward(event)

        event.app.layout.focus(w)

    application = Application(
        layout=tui.layout,
        key_bindings=kb,
        mouse_support=False,
        full_screen=True,
        style=UI.tui_style,
        refresh_interval=refresh_interval,
    )

    return application
