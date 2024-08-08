import lightbulb

from canvas_basic import CanvasBasic

# plugin setup
loader = lightbulb.Loader()
group = lightbulb.Group("player", "play music and all that")

loader.command(group)

config_data = CanvasBasic.get_config_data()
admin_role_id = config_data['admin_role_id']
default_embed_color = config_data['default_color']
filepaths = CanvasBasic.get_filepaths("MusicPlayer")

