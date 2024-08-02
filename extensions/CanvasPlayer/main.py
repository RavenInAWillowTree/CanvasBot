import json
import typing
import ongaku
import lightbulb

# plugin setup
plugin = lightbulb.Plugin("canvas-player")

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
@lightbulb.option("query", "search query")
@lightbulb.command("play", "lavalink test play music")
@lightbulb.implements(lightbulb.SlashCommand)
async def playtest(ctx: lightbulb.Context) -> None:
    client = ongaku.Client(plugin.bot)

    # make sure the user is in a valid voice channel
    voice_state = plugin.bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond("You are not in a voice channel")
        return

    # fetch the track from the query string. (this just searches YouTube)
    result = await client.rest.load_track(f"ytsearch:{ctx.options.query}")

    # if the song is 'None' let user know it failed
    if result is None:
        await ctx.respond("No songs were found")
        return

    # create a player (or if it already exists, grab that one)
    player = client.create_player(ctx.guild_id)

    # add the playlist, track or search result to the player
    if isinstance(result, typing.Sequence):
        player.add(result[0])
    else:
        player.add(result)

    # tell the player to start playing the song
    await player.play()

    await ctx.respond(f"Playing {player.queue[0].info.title}")
