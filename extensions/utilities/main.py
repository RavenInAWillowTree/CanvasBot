import hikari
from hikari import *
import lightbulb

# plugin setup
plugin = lightbulb.Plugin("utilities")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
