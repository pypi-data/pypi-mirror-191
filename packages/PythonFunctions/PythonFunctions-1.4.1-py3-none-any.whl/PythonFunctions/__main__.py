import argparse
import json
import os

from . import Version


def parserFunc():
    parser = argparse.ArgumentParser(
        prog="PythonFunctions.__main__", description="Some stuff"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        const=True,
        help="Print the module version",
    )
    parser.add_argument(
        "-s",
        "--settings",
        action="store_const",
        const=True,
        help="Generate the settings",
    )
    parser.add_argument(
        "-gs",
        "--generateSettings",
        action="store_const",
        const=True,
        help="Generate the settings file",
    )
    return parser.parse_args()


def Settings():
    # Get path
    settingPath = f"{os.getcwd()}/PyFuncSet.json"

    # Get settings
    localSettingsFound = os.path.exists(settingPath)

    # Load settings.
    defaultSettings = {"Mute": False}
    localSettings = {}

    # Read settings
    if localSettingsFound:
        with open(settingPath, encoding="utf-8") as f:
            localSettings = json.load(f)

    # Print
    print(f"SETTINGS (Local: {localSettingsFound}): ")
    for i in defaultSettings:
        if localSettings.get(i) is None:
            print(f"{i}: {defaultSettings.get(i)} (Default)")
        else:
            print(f"{i}: {localSettings.get(i)} (Default: {defaultSettings.get(i)})")


def GenerateSettings():
    with open(f"{os.getcwd()}/PyFuncSet.json", "w", encoding="utf-8") as f:
        data = {"Mute": False}
        json.dump(data, f)
    return "Generated setting file"


def GetVersion():
    return Version.ReadLocal()


def main():
    result = parserFunc()
    if result.version:
        Version.Compare()
        return
    if result.settings:
        Settings()
        return
    if result.generateSettings:
        GenerateSettings()
        return

    print("Please add `--help` on the end to view the arguments")


if Version.CanReadGlobal() and Version.LocalSettings():
    Version.Compare()

main()
