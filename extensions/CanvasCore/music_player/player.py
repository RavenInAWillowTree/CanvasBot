import hikari
import lightbulb
import ongaku

from canvas_basic import CanvasBasic

# extension setup
loader = lightbulb.Loader()
group = lightbulb.Group("player", "play music and all that")

loader.command(group)

config_data = CanvasBasic.get_config_data()
admin_role_id = config_data['admin_role_id']
default_embed_color = config_data['default_color']
filepaths = CanvasBasic.get_filepaths("MusicPlayer")

client = lightbulb.Context.client
bot = client.app

# music player setup
ongaku_client = ongaku.Client(client)
ongaku_client.create_session(
    name="CanvasPlayer-session",
    host="127.0.0.1",
    password="youshallnotpass"
)


# play music
@group.register
class JoinVoice(
    name="play",
    description="play a song",
):
    query = lightbulb.string("query", "the song to play (must be a name, not a url)")

    @lightbulb.invoke
    async def join(self, ctx: lightbulb.Context) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "This command can only be used in a server",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.user.id)
        if voice_state is not voice_state.channel_id:
            await ctx.respond(
                "You are not in a voice channel",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        if self.query is None or not isinstance(self.query, str):
            await ctx.respond(
                "Please provide a song name",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)

        result = await ongaku_client.rest.load_track(self.query)

        if result is None:
            await ctx.respond(
                hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
                "No results found",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        if isinstance(result, ongaku.Playlist):
            track = result.tracks[0]
        elif isinstance(result, ongaku.Track):
            track = result
        else:
            track = result[0]

        embed = hikari.Embed(
            title=f"[{track.title}]({track.uri})",
            description=f"by: {track.info.author}",
        )

        try:
            player = ongaku_client.fetch_player(ctx.guild_id)
        except Exception:
            player = ongaku_client.create_player(ctx.guild_id)

        await player.play(track)

        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            embed=embed,
            flags=hikari.MessageFlag.EPHEMERAL
        )

