from colorama import Fore, Style
from tabulate import tabulate
import lightbulb
import json
import os
import ast


def change_display(display):
    print(f"Current display name: {display}")
    new_display = input("Enter new name (or q to cancel):\n")
    if new_display == "q":
        print("Cancelled...")
        return display
    else:
        print("New display name saved")
        return new_display


def change_token(token):
    if token == "":
        print("No token defined")
    else:
        print(f"Current token: {token}")
    new_token = input("Enter new token (or q to cancel):\n")
    if new_token == "q":
        print("Cancelled...")
        return token
    else:
        print("New token saved")
        return new_token


def toggle_extension(config_data):
    while True:
        # list all extensions
        ext_list = get_extensions(config_data)
        ext_table = []
        for ext in ext_list:
            enabled = "enabled" if ext[2] else "disabled"
            enabled_color = Fore.GREEN if ext[2] else Fore.YELLOW
            match ext[1]:
                case 0:
                    ext_table.append([f"{enabled_color}{ext[0]}", "valid", f"{enabled}{Fore.RESET}"])
                case 1:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "invalid plugin", f"{enabled}{Fore.RESET}"])
                case 2:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "missing main.py", f"{enabled}{Fore.RESET}"])
                case 3:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "defined but missing", f"{enabled}{Fore.RESET}"])
                case 4:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "undefined", f"{enabled}{Fore.RESET}"])
        print(f"Extensions:\n{tabulate(ext_table, headers=['Name', 'Status', 'Enabled'])}\n")
                    
        selected = input("Select extension to toggle (or q to cancel):\n")
        found = False
        if selected == "q":
            print("Cancelled...")
            return config_data

        for extension in config_data['extensions']:
            if extension['name'] == selected:
                extension['enabled'] = not extension['enabled']
                found = True
                break
        if not found:
            print("Select a valid extension")
            continue
        else:
            return config_data


def get_extensions(config_data):
    # find and categorise extensions by state
    # helper function
    def validate_plugin(name):
        load_found, unload_found = False, False
        with open(f"extensions/{name}/main.py", "r") as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name == "load":
                        load_found = True
                    if node.name == "unload":
                        unload_found = True
            if load_found and unload_found:
                return True
            else:
                return False

    # get extensions both defined and in files
    ext_list = []
    # state:
    #   0: valid and functional!
    #   1: missing load or unload function
    #   2: missing main.py
    #   3: missing but defined in config.json
    #   4: found but not defined in config.json
    ext_list_dir = os.listdir("extensions")
    ext_list_def = config_data['extensions']
    # first check extensions defined in the config file
    for ext in ext_list_def:
        name, enabled = ext['name'], ext['enabled']
        state = 0
        if os.path.exists(f"extensions/{name}"):
            if os.path.exists(f"extensions/{name}/main.py"):
                if validate_plugin(name):
                    state = 0
                else:
                    state = 1
            else:
                state = 2
        else:
            state = 3
        ext_list.append([name, state, enabled])
    # check the extensions director for any undefined
    for ix, ext in enumerate(ext_list_dir):
        found = False
        for saved in ext_list:
            if ext == saved[0]:
                found = True
                break
        if not found:
            ext_list.append([ext, 4, False])
    # return results
    return ext_list


# ----- main script -----
with open("config.json", "r") as f:
    config_data = json.load(f)

# initial prints
print(f"""-*---*-------*---*-
{Style.BRIGHT}{config_data['displayName']}{Style.RESET_ALL}
Made with {Fore.BLUE}CanvasBot{Fore.RESET}
{Fore.CYAN}</{Fore.RESET}Hyjaxaru{Fore.CYAN}>{Fore.RESET} {Fore.RED}❤{Fore.RESET}
-*---*-------*---*-""")

# initial options menu
while True:
    try:
        print("""
Bot Options:
(1): Run Bot
(2): Change Display Name
(3): Change Token
(4): Enable/Disable Extension
(5): Quit""")
        choice = int(input(""))

        match choice:
            case 1:  # stop loop and run bot
                print("Running bot...")
                break
            case 2:
                config_data['displayName'] = change_display(config_data['displayName'])
            case 3:
                config_data['token'] = change_token(config_data['token'])
            case 4:
                config_data = toggle_extension(config_data)
            case 5:  # quit
                exit()
            case _:
                print("Please choose from one of the options listed")

        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4, separators=(",", ": "))

    except ValueError:
        print("Please input a number")
        continue

# set up the bot
bot = lightbulb.BotApp(
    token=config_data['token'],
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "lightbulb": {"level": "DEBUG"},
        },
    },
    help_slash_command=True
)

# load extensions
for extension in config_data['extensions']:
    try:
        if extension['enabled']:
            bot.load_extensions(f"extensions.{extension['name']}.main")
            print(f"{Fore.GREEN}loaded extension '{extension['name']}'{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}extension '{extension['name']}' disabled, skipped{Fore.RESET}")
    except:
        print(f"{Fore.RED}extension '{extension['name']}' broken, skipped{Fore.RESET}")

# run the bot
bot.run()
