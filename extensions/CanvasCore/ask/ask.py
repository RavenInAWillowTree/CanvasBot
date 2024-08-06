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

data_path = "extensions/CanvasCore/ask/data.json"


# show data.json
@ settings.register
class SettingsShowConfig(
    lightbulb.SlashCommand,
    name="show-config",
    description="display ask command json data",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(File('extensions/ask/data.json'))


# ask a non-user specific question, get a response
@group.register
class AskQuestion(
    lightbulb.SlashCommand,
    name="question",
    description="ask me anything"
):
    key = lightbulb.string("key", "non-user specific response", default=None)

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            # load json data
            with open(data_path, "r", encoding="utf-8") as f:
                jdata = json.load(f)

            # show list of all keys if no key is given
            if self.key is None:
                # non-user specific
                body = "**Keys:**\n"
                for item in jdata['saved'].keys():
                    body += f"{item}\n"

                # user specific
                body += "\n**Users:**\n"
                for item in jdata['users'].keys():
                    body += f"{item}\n"

                response = Embed(
                    title=jdata['required']['help_header'],
                    description=body,
                    color=Color.from_hex_code(default_embed_color)
                )

            elif self.key in jdata['saved'].keys():
                response = jdata['saved'][self.key]

            else:
                response = jdata['required']['question_key_404']
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['question_ask_failed'])
        else:
            await ctx.respond(response)


# ask a user specific question, get a response
@group.register
class AskAboutUser(
    lightbulb.SlashCommand,
    name="about",
    description="ask about a user"
):
    user = lightbulb.user("user", "user specific response")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            # load json data
            with open(data_path, "r", encoding="utf-8") as f:
                jdata = json.load(f)

            if str(self.user) in jdata['saved'].keys():
                response = jdata['saved'][str(self.user)]

            else:
                response = jdata['required']['user_key_404']
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['user_ask_failed'])
        else:
            await ctx.respond(response)


# add or change  non-user specific response
@settings.register
class SettingsAddNormal(
    lightbulb.SlashCommand,
    name="add-normal",
    description="add or edit a non-user specific response",
):
    key = lightbulb.string("key", "key for response")
    value = lightbulb.string("response", "response to key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open(data_path, "r", encoding='utf-8') as f:
                jdata = json.load(f)

            new_data = {self.key: self.value}
            jdata['saved'].update(new_data)

            with open(data_path, "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['question_add_failed'])
        else:
            await ctx.respond(jdata['required']['question_add_success'])


# add or change  non-user specific response
@settings.register
class SettingsAddUser(
    lightbulb.SlashCommand,
    name="add-user",
    description="add or edit a user specific response",
):
    user = lightbulb.user("user", "key for response")
    value = lightbulb.string("response", "response to key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open(data_path, "r", encoding='utf-8') as f:
                jdata = json.load(f)

            new_data = {str(self.user): self.value}
            jdata['saved'].update(new_data)

            with open(data_path, "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['user_add_failed'])
        else:
            await ctx.respond(jdata['required']['user_add_success'])


# remove a non-user specific response
@settings.register
class SettingsRemoveNormal(
    lightbulb.SlashCommand,
    name="remove-normal",
    description="remove a non-user specific response",
):
    key = lightbulb.string("key", "response key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open(data_path, "r", encoding='utf-8') as f:
                jdata = json.load(f)

            del jdata['saved'][self.key]

            with open(data_path, "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['question_remove_failed'])
        else:
            await ctx.respond(jdata['required']['question_remove_success'])


# remove a non-user specific response
@settings.register
class SettingsRemoveUser(
    lightbulb.SlashCommand,
    name="remove-user",
    description="remove a user specific response",
):
    user = lightbulb.user("user", "response key")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            with open(data_path, "r", encoding='utf-8') as f:
                jdata = json.load(f)

            del jdata['saved'][str(self.user)]

            with open(data_path, "w", encoding='utf-8') as f:
                json.dump(jdata, f, indent=4, separators=(",", ": "))
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['user_remove_failed'])
        else:
            await ctx.respond(jdata['required']['user_remove_success'])
