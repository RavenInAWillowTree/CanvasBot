import lightbulb

# extension setup
loader = lightbulb.Loader()


# standard ping command
@loader.command
class Ping(
    lightbulb.SlashCommand,
    name="ping",
    description="a test command to ensure the bot is working"
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong")
