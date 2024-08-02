from colorama import Fore, Style
from tabulate import tabulate
import lightbulb
import json
import os


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
        # list extensions
        extension_list = os.listdir("extensions")
        extension_table = []
        for extension in config_data['extensions']:
            name, enabled = extension['name'], extension['enabled']
            if extension['name'] in extension_list:
                if os.path.exists(f"extensions/{extension['name']}/main.py"):
                    if extension['enabled']:
                        extension_table.append([f"{Fore.GREEN}{name}", "valid", f"{enabled}{Fore.RESET}"])
                    else:
                        extension_table.append([f"{Fore.YELLOW}{name}", "valid", f"{enabled}{Fore.RESET}"])
                else:
                    extension_table.append([f"{Fore.RED}{name}", "missing main.py", f"{enabled}{Fore.RESET}"])
            else:
                extension_table.append([f"{Fore.RED}{name}", "defined but missing", f"{enabled}{Fore.RESET}"])
        print(f"Extensions:\n{tabulate(extension_table, headers=['Name', 'Status', 'Enabled'])}\n")

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
            print("Select a valid option")
            continue
        else:
            return config_data


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
    choice = 0
    try:
        print("""
Select a function:
(1): Run Bot
(2): Change Display Name
(3): Change Token
(4): Enable/Disable Extension""")
        choice = int(input(""))

        match choice:
            case 1:  # stop loop and run bot
                break
            case 2:
                config_data['displayName'] = change_display(config_data['displayName'])
            case 3:
                config_data['token'] = change_token(config_data['token'])
            case 4:
                config_data = toggle_extension(config_data)
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
