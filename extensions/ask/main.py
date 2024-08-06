import json
import lightbulb
from hikari import Embed, Color, File

# plugin setup
loader = lightbulb.Loader()
group = lightbulb.Group("ask", "ask me anything")
settings = group.subgroup("settings", "ask command settings")

loader.command(group)

with open("config.json") as f:
    jdata = json.load(f)
    admin_role_id = jdata['admin_role_id']
    default_embed_color = jdata['default_color']


# ask a question, get a response
@group.register
class AskQuestion(
    lightbulb.SlashCommand,
    name="question",
    description="ask me anything"
):
    key = lightbulb.string("key", "question key", default="showList")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        # load json data
        with open("extensions/ask/data.json", "r", encoding="utf-8") as f:
            jdata = json.load(f)

        # show list of all keys if no key is given
        if self.key == "showList":
            body = "**Keys:**\n"
            for item in jdata['saved'].keys():
                body += f"{item}\n"

            message = Embed(
                title=jdata['required']['help_header'],
                description=body,
                color=Color.from_hex_code(default_embed_color)
            )
            await ctx.respond(message)

        elif self.key in jdata['saved'].keys():
            await ctx.respond(jdata['saved'][self.key])

        else:
            await ctx.respond(jdata['required']['key_404'])


# add or change a
@settings.register
class SettingsEdit(
    lightbulb.SlashCommand,
    name="edit",
    description="edit or add a response",
):
    key = lightbulb.string("key", "question key")
    value = lightbulb.string("response", "response to key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open("extensions/ask/data.json", "r", encoding='utf-8') as f:
                jdata = json.load(f)

            new_data = {self.key: self.value}
            jdata['saved'].update(new_data)

            with open("extensions/ask/data.json", "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except:
            await ctx.respond(jdata['required']['edit_failed'])
        else:
            await ctx.respond(jdata['required']['edit_success'])


# remove a response
@settings.register
class SettingsRemove(
    lightbulb.SlashCommand,
    name="remove",
    description="remove a response",
):
    key = lightbulb.string("key", "question key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open("extensions/ask/data.json", "r", encoding='utf-8') as f:
                jdata = json.load(f)

            del jdata['required'][self.key]

            with open("extensions/ask/data.json", "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except:
            await ctx.respond(jdata['required']['remove_failed'])
        else:
            await ctx.respond(jdata['required']['remove_success'])


# show data.json
@settings.register
class SettingsShowConfig(
    lightbulb.SlashCommand,
    name="show-config",
    description="display ask command json data",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(File('extensions/ask/data.json'))
