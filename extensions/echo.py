import lightbulb

echo_plugin = lightbulb.Plugin("misc")

@echo_plugin.command()
@lightbulb.option("message", "Message to echo.", str, required=True)
@lightbulb.command("echo", "Echoes a message.", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context, message: str) -> None:
    await ctx.respond(message)

@echo.set_error_handler
async def on_echo_error(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.errors.NotEnoughArguments):
        await event.context.respond("Give a message!!! :<")
        return True
    return False

def load(bot: lightbulb.BotApp):
    bot.add_plugin(echo_plugin)