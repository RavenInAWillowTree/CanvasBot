import lightbulb

# plugin setup
plugin = lightbulb.Plugin("built-in")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)


# standard ping command
@plugin.command
@lightbulb.command("ping", "standard ping test command")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond("Pong")
