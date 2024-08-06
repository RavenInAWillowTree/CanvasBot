from colorama import Fore, Style
from tabulate import tabulate
import hikari
import lightbulb
import json
import os


def convert_path(path, root):
    # add the root script onto the end of path
    # since they are stored separately in the config
    combined = f"{path}/{root}"
    # strip the .py off the path
    new_path = combined.removesuffix('.py')
    # return path with all / replaced with .
    # so the path is compatible with lightbulb
    return new_path.replace("/", ".")


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
        # display a table of all extensions
        display_extension_table(config_data)
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


def extension_info(config_data):
    while True:
        # display a table of all extensions
        display_extension_table(config_data)
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
                enabled, enabled_color = "enabled" if enabled else "disabled", Fore.GREEN if enabled else Fore.YELLOW
                path = f"{ext['path']}/{ext['root_script']}"
                ext_info = f"""
{Style.BRIGHT}{Fore.CYAN}{name}:{Style.RESET_ALL} {enabled_color}{enabled}{Fore.RESET}
{desc}

{Fore.LIGHTBLACK_EX}Path: {path}{Fore.RESET}
"""
                print(ext_info)
                continue


def display_extension_table(config_data):
    # list all extensions
    ext_list = get_extensions(config_data)
    ext_table = []
    for ext in ext_list:
        enabled = "enabled" if ext[3] else "disabled"
        enabled_color = Fore.GREEN if ext[3] else Fore.YELLOW
        match ext[2]:
            case -1:
                ext_table.append([f"{Fore.CYAN}{ext[0]}", ext[1], "valid", f"required{Fore.RESET}"])
            case 0:
                ext_table.append([f"{enabled_color}{ext[0]}", ext[1], "valid", f"{enabled}{Fore.RESET}"])
            case 1:
                ext_table.append([f"{Fore.RED}{ext[0]}", ext[1], "missing root script", f"{enabled}{Fore.RESET}"])
            case 2:
                ext_table.append([f"{Fore.RED}{ext[0]}", f"defined as {ext[1]}", "missing", f"{enabled}{Fore.RESET}"])
            case _:
                ext_table.append([f"{Fore.RED}{ext[0]}", ext[1], "unknown error", f"{enabled}{Fore.RESET}"])
    ext_table_sorted = sorted(ext_table, key=lambda x: x[0])
    print(f"Extensions:\n{tabulate(ext_table_sorted, headers=['Name', 'Path', 'Status', 'Enabled'])}")


def get_extensions(config_data):
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


# ----- main script -----
with open("config.json", "r") as f:
    config_data = json.load(f)

# initial prints
print(f"""-*---*-------*---*-
{Style.BRIGHT}{config_data['displayName']}{Style.RESET_ALL}
Made with {Fore.BLUE}CanvasBot{Fore.RESET}
{Fore.CYAN}</{Fore.RESET}Hyjaxaru{Fore.CYAN}>{Fore.RESET} {Fore.RED}❤{Fore.RESET}
-*---*-------*---*-\n""")

# show extensions
display_extension_table(config_data)

# initial options menu
while True:
    try:
        print("""
Bot Options:
(1): Run Bot
(2): Change Display 
(3): Extension Info
(4): Enable/Disable Extensions
(5): Quit""")
        choice = int(input(""))
        print("")  # leave some space

        match choice:
            case 1:  # stop loop and run bot
                print("Running bot...")
                break
            case 2:
                config_data['displayName'] = change_display(config_data['displayName'])
            case 3:
                extension_info(config_data)
            case 4:
                config_data = toggle_extension(config_data)
            case 5 | "q":  # quit
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
                path = convert_path(extension['path'], extension['root_script'])
                await client.load_extensions(path)
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
