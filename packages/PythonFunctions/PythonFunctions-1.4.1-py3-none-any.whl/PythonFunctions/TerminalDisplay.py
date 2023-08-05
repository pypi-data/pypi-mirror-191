import os
import time
import typing

from . import Colours
from .Check import Check
from .Message import Message

canRead = True
try:
    from readchar import key, readkey
except ModuleNotFoundError:
    canRead = False


class Display:
    """The main class to give the user an option"""

    def __init__(self) -> None:
        if not canRead:
            print(
                "NOTE: readchar is NOT INSTALLED. This means you can only use list view"
            )

        self.options: typing.Dict = {}  # specific formaat.
        self.__storedText = None
        self.gridData = []
        self.__highest: int = 2_147_483_648
        self.__lowest: int = -2_147_483_648
        self.chk: Check = Check()
        self.cursorPosition = [0, 0]

    def SetOptions(self, options: typing.Dict):
        """Set the program options

        Args:
            options (typing.Dict): The options to set
        """

        # Validation check
        cleanOptions = {}
        for option in options:
            if isinstance(options.get(option), tuple):
                newOptions = (
                    (options.get(option)[0],)
                    + (options.get(option)[1].replace(" ", "_"),)
                    + options.get(option)[2:]
                )

                cleanOptions.update({int(option): newOptions})
            else:
                print(
                    f"{option} with data {options.get(option)} has an invalid data structure"
                )

        self.options = cleanOptions

    def AddOption(self, option: typing.Tuple, *, index: int = None):
        """Add another option to the list

        Args:
            option (typing.Tuple): The information about the option to set
            index (int, optional): The index place to place the item
        """
        if index is None:
            index = len(self.options)

        newOptions = (option[0],) + (option[1].replace(" ", "_"),) + option[2:]
        self.options.update({index: newOptions})

    def RemoveOption(self, index: int):
        """Remove an option at the selected index

        Args:
            index (int): The index to remove an option
        """
        return self.options.pop(index)

    def RemoveOptions(self, *index: int):
        """Remove all the options with the selected index

        Args:
            *index (int): The indexs to remove

        Returns:
            list: The list of removed options
        """
        removedOptions = []
        for item in index:
            removedOptions.append(self.options.pop(item))
        return removedOptions

    def RemoveAllOptions(self):
        """Remove all of the options in the list"""
        self.options = {}

    def ShowHeader(
        self, *, text: str = "Display.py", typewriter: bool = False, pace: int = 100
    ):
        """Print out a header message

        Args:
            text: (str, option) The text to display. Deafults to "Display.py".
            typewritter: (str, optional): Shows the text letter by letter. Defaults to False.
            pace: (int, optional): Words per second to show using typewritter effect.Defaults to 100
        """
        print(f"{Colours.c('g')}{'-' * os.get_terminal_size().columns}{Colours.c()}")

        if typewriter:
            for i in text:
                print(i, end="", flush=True)
                time.sleep(pace * 0.001)
            print()
        else:
            print(text)

        print(f"{Colours.c('g')}{'-' * os.get_terminal_size().columns}{Colours.c()}")

        self.__storedText = text

    def __GenerateGridData(self):
        """Generate the data of the grid. What goes where etc"""
        self.gridData = []
        row = []

        length, consoleLen = 0, os.get_terminal_size().columns  # Size limitations
        for itemIndex in self.options:
            item = self.options.get(itemIndex)[1]

            # Go onto a new row if going to go over the limit
            if (length + 6) // consoleLen >= 1:
                row[len(row) - 1] = row[len(row) - 1].replace(" ", "")
                self.gridData.append(row)
                row = []
                length = 0

            row.append(f"{item}   ")
            length += len(item) + 3

        self.gridData.append(row)

    def __ShowGrid(self):
        """Prints out the grid generated in __GenerateGridData"""
        for yIndex, yValue in enumerate(self.gridData):
            for xIndex, xValue in enumerate(yValue):
                # Complicated string, but it calculates the square that should have the `> ` pointer
                v = (
                    f"{Colours.c('bgblue')}>{Colours.c()} {xValue}"
                    if self.cursorPosition[0] == xIndex
                    and self.cursorPosition[1] == yIndex
                    else xValue
                )
                v = v.replace("_", " ")

                print(v, end="")
            print()
        print(
            """

Controls:
---------------------------------------------------------
W: Up, A: Left, S: Down, D: Right, Q: Quit, Enter: Select"""
        )

    def __ShowList(self):
        optionList = dict(sorted(self.options.items(), key=lambda ele: ele[0]))

        negList = []
        for opt in optionList:
            if opt < 0:
                negList.append(opt)
                continue

            print(f"{opt:5}:{optionList.get(opt)[1]}")
            self.__highest = opt

        print()

        self.__lowest = negList[0]
        negList = reversed(negList)
        for item in negList:
            print(f"{item:5}:{optionList.get(item)[1]}")

    def __GetListInput(self):
        try:
            v = self.chk.getInput(
                "Please enter the number you want to select: ",
                "INT",
                lower=self.__lowest,
                higher=self.__highest,
            )
            return self.options.get(v)[0](self.options.get(v)[1:])
        except TypeError:
            Message().clear("Invalid input!", timeS=2, colour="red")
            return None

    def ShowOptions(self, *, useList: bool = False):
        """Returns the item at that index

        Args:
            list (bool, optional): To show in a list or grid view. Defaults to False.

        Returns:
            _type_: The item returned
        """
        if not useList and canRead:
            self.cursorPosition = [0, 0]
            self.__GenerateGridData()
            self.__ShowGrid()
            return self.__MoveCursor()

        self.__ShowList()
        return self.__GetListInput()

    def __GetItemInfo(self, item: str):
        """Trys to find item in the list.

        Args:
            item (str): The item to find

        Returns:
            Tuple: The information about that item.
        """
        item = item.strip()
        for option in self.options:
            info = self.options.get(option)
            if info[1] == item:
                return info

        return None

    def __MoveCursor(self):
        """Moves the cursor on the screen"""
        chosen = False
        while not chosen:
            k = readkey().lower()
            if k == "w":
                self.cursorPosition[1] -= 1
                # Lock
                if self.cursorPosition[1] < 0:
                    self.cursorPosition[1] = 0

            elif k == "a":
                self.cursorPosition[0] -= 1
                # Lock
                if self.cursorPosition[0] < 0:
                    self.cursorPosition[0] = 0

            elif k == "s":
                self.cursorPosition[1] += 1
                # lock
                if self.cursorPosition[1] > len(self.gridData) - 1:
                    self.cursorPosition[1] = len(self.gridData) - 1

            elif k == "d":
                self.cursorPosition[0] += 1
                # Lock
                if (
                    self.cursorPosition[0]
                    > len(self.gridData[self.cursorPosition[1]]) - 1
                ):
                    self.cursorPosition[0] = (
                        len(self.gridData[self.cursorPosition[1]]) - 1
                    )

            elif k == key.ENTER:
                chosen = True
                itemInfo = self.__GetItemInfo(
                    self.gridData[self.cursorPosition[1]][self.cursorPosition[0]]
                )

                if len(itemInfo) > 2:
                    return itemInfo[0](itemInfo[1:])

                return itemInfo[0](itemInfo[1])

            elif k == "q":
                chosen = True
                return None

            # moves the cursor, Makes it look clearer
            print("\033[0;0H", end="")
            self.ShowHeader(text=self.__storedText)
            self.__ShowGrid()
