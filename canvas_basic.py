import json
import os

from rich.table import Table
from rich.console import Console

console = Console()


# helper class for the main menu
class CanvasBootstrap:
    @staticmethod
    def convert_path(path, root):
        """convert path to lightbulb compatible path

        Args:
            path (str): path to the extension
            root (str): root script of the extension

        Returns:
            str: converted path
        """

        # add the root script onto the end of path
        # since they are stored separately in the config
        combined = f"{path}/{root}"
        # strip the .py off the path
        new_path = combined.removesuffix('.py')
        # return path with all / replaced with .
        # so the path is compatible with lightbulb
        return new_path.replace("/", ".")

    @staticmethod
    def change_display_name(bot_name):
        """change the display name of the

        Args:
            bot_name (str): current display name

        Returns:
            str: new display name
        """

        console.print(f"Current display name: {bot_name}")
        new_bot_name = input("Enter new name (or q to cancel):\n")
        if new_bot_name == "q":
            console.print("Cancelled...")
            return bot_name
        else:
            console.print("New display name saved")
            return new_bot_name

    @staticmethod
    def get_extensions(config_data):
        """get a list of all extensions and their status

        Args:
            config_data (dict): configuration data

        Returns:
            list: list of extensions and their status
        """

        # get extensions both defined and in files
        ext_list = []
        # state:
        #  -1: valid and required
        #   0: valid and functional
        #   1: missing defined root script.py
        #   2: directory invalid or missing
        ext_list_def = config_data['extensions']
        for ext in ext_list_def:
            name, path, root, enabled = ext['name'], ext['path'], ext['root_script'], ext['enabled']
            if os.path.exists(path):
                if os.path.exists(f"{path}/{root}"):
                    if "required" in ext.keys():
                        state = -1
                    else:
                        state = 0
                else:
                    state = 1
            else:
                state = 2
            ext_list.append([name, path, state, enabled])
        # return results
        return ext_list

    @classmethod
    def toggle_extension(cls, config_data):
        """toggle an extension on or off

        Args:
            config_data (dict): configuration data

        Returns:
            dict: updated configuration data
        """

        while True:
            # display a table of all extensions
            cls.display_extension_table(config_data)
            # get plugin to toggle
            selected = input("\nSelect extension to toggle (or q to cancel):\n")
            found = False

            # quit and non-optional extensions
            if selected.lower() == "q":
                console.print("[yellow]Cancelled...")
                return config_data

            # toggle extension
            for extension in config_data['extensions']:
                if extension['name'].lower() == selected.lower():
                    if "required" in extension.keys():
                        break
                    else:
                        extension['enabled'] = not extension['enabled']
                        found = True
                        break
            if not found:
                console.print("[red]Select a valid extension")
                continue
            else:
                return config_data

    @classmethod
    def extension_info(cls, config_data):
        """display information about an extension

        Args:
            config_data (dict): configuration data

        Returns:
            dict: updated configuration data
        """

        while True:
            # display a table of all extensions
            cls.display_extension_table(config_data)
            # get plugin to toggle
            selected = input("\nSelect extension to view description:\n")
            found = False

            # quit and non-optional extensions
            if selected.lower() == "q":
                console.print("[yellow]Cancelled...")
                return config_data

            # toggle extension
            for ext in config_data['extensions']:
                if ext['name'].lower() == selected.lower():
                    name, desc, enabled = ext['name'], ext['desc'], ext['enabled']
                    enabled, enabled_color = "Enabled" if enabled else "Disabled", "green" if enabled else "yellow"
                    path = f"{ext['path']}/{ext['root_script']}"
                    ext_info = f"""
[cyan bold]{name}:[/cyan bold] [{enabled_color}]{enabled}[/{enabled_color}]
{desc}
[gray]Path: {path}[/gray]
"""
                    print(ext_info)
                    continue

    @classmethod
    def display_extension_table(cls, config_data):
        """display a table of all extensions to the console

        Args:
            config_data (dict): configuration data
        """

        # list all extensions
        ext_list = cls.get_extensions(config_data)
        ext_table = []
        for ext in ext_list:
            enabled = "Enabled" if ext[3] else "Disabled"
            enabled_color = "green" if ext[3] else "yellow"
            match ext[2]:
                case -1:
                    ext_table.append(["cyan", f"{ext[0]}", ext[1], "OK", f"Required"])
                case 0:
                    ext_table.append([f"{enabled_color}", f"{ext[0]}", ext[1], "OK", f"{enabled}"])
                case 1:
                    ext_table.append(["red", f"{ext[0]}", ext[1], "Missing root script", f"{enabled}"])
                case 2:
                    ext_table.append(["red", f"{ext[0]}", f"Defined as {ext[1]}", "missing", f"{enabled}"])
                case _:
                    ext_table.append(["red", f"{ext[0]}", ext[1], "Unknown error", f"{enabled}"])
        ext_table_sorted = sorted(ext_table, key=lambda x: x[1])

        table = Table(show_header=True, show_edge=False, header_style="bold")
        table.add_column("Name")
        table.add_column("Path")
        table.add_column("Status")
        table.add_column("Enabled")

        for ext in ext_table_sorted:
            table.add_row(ext[1], ext[2], ext[3], ext[4], style=ext[0])
        console.print(table)


# extension helper class, basic functions for extensions
class CanvasBasic:
    @staticmethod
    def get_data(file):
        """get data from a json file

        Args:
            file (str): file path

        Returns:
            dict: data from the file
        """

        with open(file, "r") as f:
            return json.load(f)

    @staticmethod
    def save_data(file, data):
        """save data to a json file

        Args:
            file (str): file path
            data (dict): data to save
        """

        with open(file, "w") as f:
            json.dump(data, f, indent=4, separators=(",", ": "))

    @staticmethod
    def get_config_data():
        """get data from config.json

        Returns:
            dict: data from config.json
        """

        with open("config.json", "r") as f:
            return json.load(f)

    @staticmethod
    def save_config_data(data):
        """save data to config.json

        Args:
            data (dict): data to save
        """

        with open("config.json", "w") as f:
            json.dump(data, f, indent=4, separators=(",", ": "))

    @staticmethod
    def get_filepaths(extension_name):
        """get file paths from config.json for the extension

        Args:
            extension_name (str): name of the extension

        Returns:
            list: list of file paths
        """

        with open("config.json") as f:
            config_data = json.load(f)
            filepaths = []
            for ext in config_data.get('extensions', []):
                if ext['name'] == extension_name:
                    for file in ext['files']:
                        filepaths.append({f"{file}": f"{ext['path']}/{file}"})
        return filepaths
