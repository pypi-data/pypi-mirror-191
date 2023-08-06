from dataclasses import dataclass

# pylint: disable=W0611
from colorama import Back, Fore, Style
# Disabled as imported from other module to make it all fit together
# pylint: enable=W0611


@dataclass
class CONSOLEFORMATS:
    RESET = "\033[0m"
    BOLD = "\033[01m"
    DISABLE = "\033[02m"
    ITALIC = "\033[03m"
    UNDERLINE = "\033[04m"
    REVERSE = "\033[07m"
    STRIKETHROUGH = "\033[09m"
    INVISIBLE = "\033[08m"


@dataclass
class CONSOLECOLOURS:
    @dataclass
    class Fore:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GREY = "\033[37m"
        DARK_GREY = "\033[90m"
        LIGHT_RED = "\033[91m"
        LIGHT_GREEN = "\033[92m"
        YELLOW = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        PINK = "\033[95m"
        LIGHT_CYAN = "\033[96m"

    @dataclass
    class Back:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        ORANGE = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        LIGHT_GREY = "\033[47m"
