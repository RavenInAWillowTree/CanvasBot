import json
import lightbulb
from hikari import Embed, Color

# plugin setup
plugin = lightbulb.Plugin("ask")

with open("config.json") as f:
    jdata = json.load(f)
    admin_role_id = jdata['admin_role_id']
    default_embed_color = jdata['default_color']


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)


# main command group
@plugin.command
@lightbulb.command("ask", "ama group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def ask() -> None: pass


# ask admin tools command group
@plugin.command
@lightbulb.add_checks(lightbulb.has_roles(admin_role_id))
@lightbulb.command("ask_settings", "(admin) ask extension settings")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def ask_settings() -> None: pass


# ask a question, get a response
@ask.child
@lightbulb.option("key", "question key", required=False, default="showList")
@lightbulb.command("question", "ask me anything")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ask_question(ctx: lightbulb.Context) -> None:
    # load json data
    with open("extensions/ask/data.json", encoding="utf-8") as f:
        jdata = json.load(f)

    # show list of all keys if no key given
    if ctx.options.key == "showList":
        body = "**Options:**\n"
        for item in jdata['saved'].keys():
            body += f"{item}\n"

        message = Embed(
            title=jdata['builtin']['help_header'],
            description=body,
            color=Color.from_hex_code(default_embed_color),
        )
        await ctx.respond(message)

    elif ctx.options.key in jdata['saved'].keys():
        await ctx.respond(jdata['saved'][ctx.options.key])

    else:
        await ctx.respond(jdata['builtin']['key_404'])


# add or change a response
@ask_settings.child
@lightbulb.option("content", "question response")
@lightbulb.option("key", "question key")
@lightbulb.command("edit", "add or change a response")
@lightbulb.implements(lightbulb.SlashSubGroup)
async def ask_edit(ctx: lightbulb.Context) -> None:
    try:
        with open("extensions/ask/data.json", "r") as f:
            jdata = json.load(f)

        new_data = {ctx.options.key: ctx.options.content}
        jdata['saved'].update(new_data)

        with open("extensions/ask/data.json", "w") as f:
            json.dump(jdata, f, indent=4, separators=(",", ": "))
    except:
        await ctx.respond(jdata['builtin']['edit_failed'])
    else:
        await ctx.respond(jdata['builtin']['edit_success'])


# remove a response
@ask_settings.child
@lightbulb.option("key", "question key")
@lightbulb.command("remove", "remove a response")
@lightbulb.implements(lightbulb.SlashSubGroup)
async def ask_remove(ctx: lightbulb.Context) -> None:
    try:
        with open("extensions/ask/data.json", "r") as f:
            jdata = json.load(f)

        del jdata['saved'][ctx.options.key]

        with open("extensions/ask/data.json" "w") as f:
            json.dump(jdata, f, indent=4, separators=(",", ": "))
    except:
        await ctx.respond(jdata['builtin']['remove_failed'])
    else:
        await ctx.respond(jdata['builtin']['remove_success'])
