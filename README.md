**# CanvasBot

[Releases]: https://github.com/Hyjaxaru/CanvasBot/releases

[CanvasBootstrap]: #cvs-bootstrap
[CanvasManager]: #cvs-manager
[CanvasPlayer]: #cvs-Player
[Utils]: #utils
[Asker]: #asker

An easy-to-use discord bot platform made with Python and Hikari Lightbulb.

CanvasBot is designed to be controlled mainly from the Discord client, with minimal setup and CLI interaction.

The minimal CLI interaction needed is made easier by [CanvasBootstrap], a small interface to aid with bot setup and extension management. Most of its functions, however, are/will be available in Discord with [CanvasManager].

## Quick Start

1. Download the latest build of CanvasBot, found here: *[Releases]*
2. Set up a .env
3. Add your bot token as the environment variable `TOKEN`
4. Run `main.py` and you're done!

## Stock Features

### CanvasBootstrap <a name="cvs-bootstrap"></a>

The CLI interface. allows you to manage basic bot settings and extensions without starting the bot.

### CanvasManager <a name="cvs-manager"></a> 

The main backend of CanvasBot. Allows you to change settings and config data on-the-fly in the Discord client. In the future, you will be able to add and remove extensions this way, with automatic `config.json` updates.

> [!NOTE]
> This extension is required, and therefor cannot be disabled.

### Utils <a name="utils"></a>

A small collection of little utility commands, both slash and context menu commands.

### Asker <a name="asker"></a>

Allows you to set predetermined responses to question keys. Support for bot non-user and user specific responses.


## Developing Extensions

CanvasBot is built using `lightbulb v3` and keeps track of them in the `config.json`. An extension will not be loaded if it is not defined, or raises an error during load. Here is an example definition:

```json
{
    "name": "Extension Name",
    "desc": "Brief description of it's function",
    "path": "extensions/path/to/folder",
    "root_script": "main.py",
    "enabled": true
}
```

There is an optional parameter, `required`, that if present will stop the extension from being disabled. the value of `required` doesn't matter, it will work as long as it's present in the extension declaration.**

> [!IMPORTANT]
> The `required` parameter should not be used in your own extensions unless absolutely necessary.