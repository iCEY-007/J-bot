import hikari
import lightbulb
from PIL import Image

image_plugin = lightbulb.Plugin("image", "does stuff to images")

@image_plugin.command()
@lightbulb.command("image", "do fun stuff to images")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def image() -> None:
    pass

