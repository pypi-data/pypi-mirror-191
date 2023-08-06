import os
import time

from .Colours import CONSOLECOLOURS, Fore, Style


class Message:
    """Another way to handle console clearing"""

    @staticmethod
    def __messageSort(
        *,
        timeS: int = 0,
        message: str = None,
        clear: bool = False,
        colour: str = "",
        delete: bool = False,
    ):
        # checks for timeS is string instead of time
        if isinstance(timeS, str):
            lr = Fore.LIGHTRED_EX
            print(
                f"{lr}Automatically fixed error! `timeS` was string instead of number!{Fore.RESET}"
            )
            time.sleep(2)  # force wait
            message = timeS
            timeS = 2  # default time, 2 seconds for message

        # Prints the message
        if message:
            print(f"{colour}message{Style.RESET_ALL}")

        # Waits X seconds
        time.sleep(timeS)

        # If clearing console data
        if clear:
            # Check if we don't care about previous data
            if delete:
                return os.system("cls" if os.name == "nt" else "clear")
            return print("\x1b[2J\x1b[H", end="")
        return None

    @staticmethod
    def clear(
        message: str = "",
        *,
        timeS: int = 0,
        delete: bool = False,
    ):
        """Clears the console with some options

        Args:
            message (str, optional): The message to show. Defaults to None.
            timeS (int, optional): Time to wait after showing the message. Defaults to 0.
            delete (bool, optional): Whever to delete the console log afterwards. Defaults to False.
        """
        Message.__messageSort(
            timeS=timeS,
            message=message,
            clear=True,
            delete=delete,
            colour=CONSOLECOLOURS.Fore.ORANGE,
        )

    @staticmethod
    def warn(message: str = None, *, timeS: int = 0):
        """Not as bad as clear, but still shows as many options

        Args:
            message (str, optional): The message to show. Defaults to None.
            timeS (int, optional): The time to wait before carring on. Defaults to 0.
        """
        Message.__messageSort(
            timeS=timeS, message=message, colour=CONSOLECOLOURS.Fore.ORANGE
        )
