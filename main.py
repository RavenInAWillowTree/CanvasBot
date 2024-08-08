import json
import os

import hikari
import lightbulb
from colorama import Fore, Style

from canvas_basic import CanvasBootstrap as Helper

with open("config.json", "r") as f:
    config_data = json.load(f)

# initial prints
print(f"""-*---*-------*---*-
{Style.BRIGHT}{config_data['displayName']}{Style.RESET_ALL}
Made with {Fore.BLUE}CanvasBot{Fore.RESET}
{Fore.CYAN}</{Fore.RESET}Hyjaxaru{Fore.CYAN}>{Fore.RESET} {Fore.RED}❤{Fore.RESET}
-*---*-------*---*-\n""")

# show extensions
Helper.display_extension_table(config_data)

# options menu
while True:
    try:
        print("""
Bot Options:
(1): Run Bot
(2): Change Display Name
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
                config_data['displayName'] = Helper.change_display_name(config_data['displayName'])
            case 3:
                Helper.extension_info(config_data)
            case 4:
                config_data = Helper.toggle_extension(config_data)
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
                path = Helper.convert_path(extension['root_script'])
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
