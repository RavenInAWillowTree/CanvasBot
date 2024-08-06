import json
import lightbulb

# plugin setup
loader = lightbulb.Loader()
group = lightbulb.Group("player", "play music and all that")

loader.command(group)

with open("config.json") as f:
    jdata = json.load(f)
    admin_role_id = jdata['admin_role_id']
    default_embed_color = jdata['default_color']
