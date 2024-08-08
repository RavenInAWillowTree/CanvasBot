import json

import lightbulb
from hikari import Embed, Color, File

from canvas_basic import CanvasBasic

# plugin setup
loader = lightbulb.Loader()
group = lightbulb.Group("ask", "ask me anything")
settings = group.subgroup("settings", "ask command settings")

loader.command(group)

config_data = CanvasBasic.get_config_data()
admin_role_id = config_data['admin_role_id']
default_embed_color = config_data['default_color']
filepaths = CanvasBasic.get_filepaths("Asker")


# show data.json
@ settings.register
class SettingsShowConfig(
    lightbulb.SlashCommand,
    name="show-config",
    description="display ask command json data",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(File(filepaths['data.json']))


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
            jdata = CanvasBasic.get_data(filepaths['data.json'])

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

            # get response for key if key is in saved
            elif self.key in jdata['saved'].keys():
                response = jdata['saved'][self.key]

            # if key is not in saved
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
            jdata = CanvasBasic.get_data(filepaths['data.json'])

            # get response for user if user is in saved
            if str(self.user) in jdata['saved'].keys():
                response = jdata['saved'][str(self.user)]

            # if user is not in saved
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
            # load json data
            jdata = CanvasBasic.get_data(filepaths['data.json'])

            # add new data to saved
            new_data = {self.key: self.value}
            jdata['saved'].update(new_data)

            # save data
            CanvasBasic.save_data(filepaths['data.json'], jdata)
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
            # load json data
            jdata = CanvasBasic.get_data(filepaths['data.json'])

            # add new data to saved
            new_data = {str(self.user): self.value}
            jdata['saved'].update(new_data)

            # save data
            CanvasBasic.save_data(filepaths['data.json'], jdata)
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
            # load json data
            jdata = CanvasBasic.get_data(filepaths['data.json'])

            # remove key from saved
            del jdata['saved'][self.key]

            # save data
            CanvasBasic.save_data(filepaths['data.json'], jdata)
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
            # load json data
            jdata = CanvasBasic.get_data(filepaths['data.json'])

            # remove key from saved
            del jdata['saved'][str(self.user)]

            # save data
            CanvasBasic.save_data(filepaths['data.json'], jdata)
        except Exception as e:
            print(e)
            await ctx.respond(jdata['required']['user_remove_failed'])
        else:
            await ctx.respond(jdata['required']['user_remove_success'])
