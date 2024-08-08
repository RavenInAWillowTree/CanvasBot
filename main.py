import json
import os

import hikari
import lightbulb
from rich.console import Console

from canvas_basic import CanvasBasic
from canvas_basic import CanvasBootstrap as Helper

console = Console()

config_data = CanvasBasic.get_config_data()

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

# initial prints
console.print(f"""-*---*-------*---*-
[bold cyan]{config_data['displayName']}[/bold cyan]
Made with [bold blue]CanvasBot[/bold blue] and [red]❤[/red] by [cyan]</[/cyan]Hyjaxaru[cyan]>[/cyan]
-*---*-------*---*-\n""")

# show extensions
Helper.display_extension_table(config_data)

# options menu
while True:
    try:
        console.print("""
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
                console.print("Running bot...")
                break
            case 2:
                config_data['displayName'] = Helper.change_display_name(config_data['displayName'])
            case 3:
                Helper.extension_info(config_data)
            case 4:
                config_data = Helper.toggle_extension(config_data)
            case 5:  # quit
                exit()
            case _:
                console.print("Please choose from one of the options listed")

        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4, separators=(",", ": "))

    except ValueError:
        print("Please input a number")
        continue


# load extensions
@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    for ext in config_data['extensions']:
        try:
            if ext['enabled']:
                path = Helper.convert_path(ext['path'], ext['root_script'])
                await client.load_extensions(path)
            else:
                console.print(f"[yellow]Extension '{ext['name']}' disabled, skipped")
        except Exception as e:
            console.print(f"[red]Extension '{ext['name']}' broken or could not be loaded, skipped")
            console.print(f"[red]{e}")

    # start the bot
    await client.start()

# run the bot
bot.subscribe(hikari.StartingEvent, client.start)
bot.run()
