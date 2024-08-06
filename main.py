from colorama import Fore, Style
from tabulate import tabulate
import hikari
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
                    ext_table.append([f"{Fore.RED}{ext[0]}", "missing main.py", f"{enabled}{Fore.RESET}"])
                case 2:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "defined but missing", f"{enabled}{Fore.RESET}"])
                case 3:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "undefined extension", f"{enabled}{Fore.RESET}"])
                case _:
                    ext_table.append([f"{Fore.RED}{ext[0]}", "unknown error", f"{enabled}{Fore.RESET}"])
        print(f"Extensions:\n{tabulate(ext_table, headers=['Name', 'Status', 'Enabled'])}\n")

        # get plugin to toggle
        selected = input("Select extension to toggle (or q to cancel):\n")
        found = False

        # quit and non-optional extensions
        if selected == "q":
            print("Cancelled...")
            return config_data
        elif "_Canvas" in selected:
            print("you cannot disable core Canvas extensions")
            continue

        # toggle extension
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
    # get extensions both defined and in files
    ext_list = []
    # state:
    #   0: valid and functional!
    #   1: missing main.py
    #   2: missing but defined in config.json
    #   3: found but not defined in config.json
    ext_list_dir = os.listdir("extensions")
    ext_list_def = config_data['extensions']
    # first check extensions defined in the config file
    for ext in ext_list_def:
        name, enabled = ext['name'], ext['enabled']
        if os.path.exists(f"extensions/{name}"):
            if os.path.exists(f"extensions/{name}/main.py"):
                state = 0
            else:
                state = 1
        else:
            state = 2
        ext_list.append([name, state, enabled])
    # check the extensions director for any undefined
    for ix, ext in enumerate(ext_list_dir):
        found = False
        for saved in ext_list:
            if ext == saved[0]:
                found = True
                break
        if not found:
            ext_list.append([ext, 3, False])
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
(3): Enable/Disable Extension
(4): Quit""")
        choice = int(input(""))

        match choice:
            case 1:  # stop loop and run bot
                print("Running bot...")
                break
            case 2:
                config_data['displayName'] = change_display(config_data['displayName'])
            case 3:
                config_data = toggle_extension(config_data)
            case 4:  # quit
                exit()
            case _:
                print("Please choose from one of the options listed")

        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4, separators=(",", ": "))

    except ValueError:
        print("Please input a number")
        continue

# set up the bot
bot = hikari.GatewayBot(
    token=os.environ['TOKEN'],
    logs={
        "version": 1,
        "incremental": True,
        "loggers": {
            "hikari": {"level": "INFO"},
            "hikari.ratelimits": {"level": "INFO"},
            "lightbulb": {"level": "INFO"},
        },
    }
)

client = lightbulb.client_from_app(bot)


# load extensions
@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    for extension in config_data['extensions']:
        try:
            if extension['enabled']:
                await client.load_extensions(f"extensions.{extension['name']}.main")
            else:
                print(f"{Fore.YELLOW}Extension '{extension['name']}' disabled, skipped{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Extension '{extension['name']}' broken or could not be loaded, skipped"
                  f"\n\t{e}{Fore.RESET}")

    # start the bot
    await client.start()

# run the bot
bot.subscribe(hikari.StartingEvent, client.start)
bot.run()
