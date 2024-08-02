from hikari import Embed, Color
import lightbulb
import json

# plugin setup
plugin = lightbulb.Plugin("canvas_manager")

with open("config.json") as f:
    jdata = json.load(f)
    admin_role_id = jdata['admin_role_id']
    default_embed_color = jdata['default_color']


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.add_plugin(plugin)


# CanvasManager core command group
@plugin.command
@lightbulb.add_checks(lightbulb.has_roles(admin_role_id))
@lightbulb.command("canvas_manager", "manage your canvas_bot")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def canvas_manager() -> None:
    pass


@canvas_manager.child
@lightbulb.command("show_config", "display canvas config json")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def show_config(ctx: lightbulb.Context):
    with open("config.json", "r") as f:
        config = json.load(f)
        body = json.dumps(config, indent=4)
    message = Embed(
        color=Color.from_hex_code(default_embed_color),
        title="# Canvas config.json",
        description=f"""```JSON
{body}
```"""
    )
    await ctx.respond(message)
