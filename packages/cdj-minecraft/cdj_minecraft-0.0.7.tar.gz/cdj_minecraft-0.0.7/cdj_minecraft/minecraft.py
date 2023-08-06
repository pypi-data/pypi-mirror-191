import traceback
from inspect import signature

from javascript import require, On

from cdj_minecraft import translations

mineflayer = require("mineflayer")
pathfinder = require("mineflayer-pathfinder").pathfinder

DEFAULT_CONFIG = {
    "naam": "MinecraftBot",
    "server": "localhost",
    "poort": 25_565
}

registered_events: dict[str, list[callable]] = {}


def on_event(event: str):
    event = translations.events.get(event, event)

    def decorator(func: callable):
        if event not in registered_events:
            registered_events[event] = []
        registered_events[event].append(func)
        return func

    return decorator


wanneer = on_event


class Bot:
    def __init__(self, **kwargs):
        self.bot = None
        self.config = DEFAULT_CONFIG | kwargs

    @property
    def naam(self):
        return self.config["naam"]

    @property
    def server(self):
        return self.config["server"]

    @property
    def poort(self):
        return self.config["poort"]

    def __register_event(self, event: str):
        On(self.bot, event)(lambda *args: self.__dispatch_event(event, *args))

    @staticmethod
    def __handle_event(event: str, *args):
        if event in registered_events:
            for func in registered_events[event]:
                amount_of_params = len(signature(func).parameters)
                if amount_of_params == 0 or len(args) == 0:
                    return func()
                elif len(args) >= amount_of_params + 1:
                    return func(*args[1:amount_of_params + 1])

                raise RuntimeError(
                    f"Event '{event}' heeft '{amount_of_params}' parameters, "
                    f"maar er zijn er maar '{len(args)}' gegeven."
                )

    def __dispatch_event(self, event: str, *args):
        try:
            self.__handle_event(event, *args)
        except Exception as e:
            def format_arg(arg):
                representation = repr(arg)

                if len(representation) > 20:
                    representation = f"{representation[:17]}..."

                return representation

            print(f"Error in {repr(event)} (args: {repr([format_arg(arg) for arg in args])})", traceback.format_exc())

    def start(self):
        self.bot = mineflayer.createBot({
            "host": self.server,
            "port": self.poort,
            "username": self.naam
        })
        self.bot.loadPlugin(pathfinder)
        any(self.__register_event(event) for event in registered_events)

    def zeg(self, text: str):
        self.bot.chat(text)
