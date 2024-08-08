from colorama import Fore, Style
from tabulate import tabulate
import json
import os


# CanvasBootstrap class, helps main.py
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

        print(f"Current display name: {bot_name}")
        new_bot_name = input("Enter new name (or q to cancel):\n")
        if new_bot_name == "q":
            print("Cancelled...")
            return bot_name
        else:
            print("New display name saved")
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
                print("Cancelled...")
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
                print("Select a valid extension")
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
                print("Cancelled...")
                return config_data

            # toggle extension
            for ext in config_data['extensions']:
                if ext['name'].lower() == selected.lower():
                    name, desc, enabled = ext['name'], ext['desc'], ext['enabled']
                    enabled, enabled_color = "Enabled" if enabled else "Disabled", Fore.GREEN if enabled else Fore.YELLOW
                    path = f"{ext['path']}/{ext['root_script']}"
                    ext_info = f"""
    {Style.BRIGHT}{Fore.CYAN}{name}:{Style.RESET_ALL} {enabled_color}{enabled}{Fore.RESET}
    {desc}
    {Fore.LIGHTBLACK_EX}Path: {path}{Fore.RESET}
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
            enabled_color = Fore.GREEN if ext[3] else Fore.YELLOW
            match ext[2]:
                case -1:
                    ext_table.append([f"{Fore.CYAN}{ext[0]}", ext[1], "OK", f"Required{Fore.RESET}"])
                case 0:
                    ext_table.append([f"{enabled_color}{ext[0]}", ext[1], "OK", f"{enabled}{Fore.RESET}"])
                case 1:
                    ext_table.append([f"{Fore.RED}{ext[0]}", ext[1], "Missing root script", f"{enabled}{Fore.RESET}"])
                case 2:
                    ext_table.append(
                        [f"{Fore.RED}{ext[0]}", f"Defined as {ext[1]}", "missing", f"{enabled}{Fore.RESET}"])
                case _:
                    ext_table.append([f"{Fore.RED}{ext[0]}", ext[1], "Unknown error", f"{enabled}{Fore.RESET}"])
        ext_table_sorted = sorted(ext_table, key=lambda x: x[0])
        print(f"Extensions:\n{tabulate(ext_table_sorted, headers=['Name', 'Path', 'Status', 'Enabled'])}")
