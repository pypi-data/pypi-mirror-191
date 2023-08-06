import asyncio
import copy
import glob
import os
import typing

from .CleanFolderData import Clean as Cln
from .Colours import CONSOLEFORMATS, Fore, Style


class search:
    def __init__(self):
        self.__FoundList = []

        self.directory = ""
        self.target = None
        self.layers = 2
        self.hidden = []
        self.searched = []
        self.logging = False

    def __Print(self, msg: str, colour: str = None, msgformat: str = None):
        if self.logging:
            print(f"{msgformat}{colour}{msg}{Style.RESET_ALL}")
            # Print(msg, colour, msgformat)

    def Locate(
        self,
        target: typing.List[str],
        *,
        directory: str = ".",
        layers: int = 2,
        hidden: typing.List[str] = None,
        logging: bool = False,
    ):
        """Find a file with paramaters

        Args:
            target (typing.List[str]): The file to find
            directory (str, optional): The directory to find the file in. Defaults to ".".
            layers (int, optional): How many layers above the directory to go. Defaults to 2.
            hidden (typing.List[str], optional): The files to skip over. Defaults to None.
            logging (bool, optional): Whever to output what is happening. Defaults to False.

        Returns:
            List[str]: A list of files found
        """
        self.hidden = hidden or []
        self.target = target
        self.layers = layers + 1
        self.directory = directory if directory != "." else os.path.abspath(
            ".")
        self.logging = logging

        return asyncio.run(self.__AsyncLocate())

    def Clear(self):
        """Reset the module ready for the next use"""
        self.__FoundList = []

        self.directory = ""
        self.target = None
        self.layers = 2
        self.hidden = []
        self.searched = []
        self.logging = False

    async def __AsyncLocate(self):
        await self.__searchDirectory(self.directory)
        return self.__FoundList

    def __FindFile(self, directory, file):
        # Using glob, finds files with `directory/file`
        files = glob.glob(os.path.join(directory, file))
        self.__FoundList.extend(files)

    async def __searchDirectory(self, directory, parentSearch=False):
        """Searches for a file in a directory

        Args:
            directory (str): The directory to search in.
            parentSearch (bool, optional): Disable searching parent directory. Defaults to False.
        """
        if self.layers == 0:
            raise IndexError("Invalid amount of layers! Must have at least 1")

        # Output the current check
        fileText = (
            "files"
            if isinstance(self.target, list) and len(self.target) > 1
            else "file"
        )
        self.__Print(
            f"Searching Directory: '{directory}' Target {fileText}: '{self.target}'",
            Fore.GREEN,
        )

        # checks if in current directory, returns if it is.
        if isinstance(self.target, list):
            for file in self.target:
                self.__FindFile(directory, file)

        # get files in current directory and remove the folder the user
        # just came out of (doesn't search the folder again)
        try:
            hiddenFiles = copy.deepcopy(self.hidden)
            hiddenFiles.extend(self.searched)
            files = Cln().clean(directory, hiddenFiles)
        except PermissionError:
            return self.__Print(
                f"Missing permissions to read from {directory}",
                Fore.RED,
                CONSOLEFORMATS.BOLD,
            )

        # loops though all the files
        for file in files:
            self.__Print(f"Looking at {file}", Fore.YELLOW)
            info = os.path.join(directory, file)

            if file == self.target:
                if info not in self.__FoundList:
                    self.__FoundList.append(info)

            # Is in list check
            if isinstance(self.target, list):
                if file in self.target:
                    if info not in self.__FoundList:
                        self.__FoundList.append(info)

            # Search sub directories if found.
            newFile = os.path.join(directory, file)
            if os.path.isdir(newFile):
                await self.__searchDirectory(newFile, True)  # noqa E501
                self.__Print(
                    f"Searching Directory: '{directory}' Target {fileText}: '{self.target}'",
                    Fore.GREEN,
                )

        # if sub directory, don't go back up 1 directory.
        if not parentSearch and self.layers > 1:
            self.searched = os.path.basename(os.path.abspath(directory))
            self.layers -= 1  # limit to how high we can check.
            await self.__searchDirectory(
                os.path.abspath(os.path.join(directory, "../"))
            )
