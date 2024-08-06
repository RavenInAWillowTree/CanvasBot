from hikari import Embed, Color, File
import lightbulb
import json

# extension setup
loader = lightbulb.Loader()
group = lightbulb.Group("canvas-manager", "canvas-bot management, all from within discord")

loader.command(group)

with open("config.json") as f:
    jdata = json.load(f)
    admin_role_id = jdata['admin_role_id']
    default_embed_color = jdata['default_color']


# show the main canvas config file
@group.register
class ShowConfig(
    lightbulb.SlashCommand,
    name="show-config",
    description="display the main canvas config file",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(File('config.json'))
