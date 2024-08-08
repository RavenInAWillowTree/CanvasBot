import lightbulb
from hikari import File

from canvas_basic import CanvasBasic

# extension setup
loader = lightbulb.Loader()
group = lightbulb.Group("canvas-manager", "canvas-bot management, all from within discord")

loader.command(group)

config_data = CanvasBasic.get_config_data()
admin_role_id = config_data['admin_role_id']
default_embed_color = config_data['default_color']


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
