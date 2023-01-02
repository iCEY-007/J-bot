from typing import Optional
from random import randint
from constants import MAKER

import hikari
import lightbulb
import miru

fun_plugin = lightbulb.Plugin("fun")

@fun_plugin.command()
@lightbulb.command("fun", "All the entertainment commands that I have bothered implementing!")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def fun_group(ctx: lightbulb.Context) -> None:
    pass

@fun_group.child()
@lightbulb.option("max", "Highest number to roll. Defaults to 6.", int, required=False, default=6)
@lightbulb.option("min", "Lowest number to roll. Defaults to 0.", int, required=False, default=0)
@lightbulb.command("roll", "Rolls between the inputs!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def meme(ctx: lightbulb.Context, min: Optional[int] = 0, max: Optional[int] = 6):
    random = randint(min, max)
    
    embed = (
        hikari.Embed(color=0x0000FF)
        .add_field(f"{ctx.author.username} rolled a number between {min} and {max}!", f"They got {random}!")
    )

    await ctx.respond(embed=embed)

class AnimalView(miru.View):
    def __init__(self, author: hikari.User):
        self.author = author
        super().__init__(timeout=60)
    
    @miru.select(
        custom_id="animal_select",
        placeholder="Pick an animal :3",
        options=[
            miru.SelectOption("Dog", "dog", emoji="🐶"),
            miru.SelectOption("Cat", "cat", emoji="🐱"),
            miru.SelectOption("Panda", "panda", emoji="🐼"),
            miru.SelectOption("Fox", "fox", emoji="🦊"),
            miru.SelectOption("Red Panda", "red_panda", emoji="🐼"),
            miru.SelectOption("Koala", "koala", emoji="🐨"),
            miru.SelectOption("Bird", "bird", emoji="🐦"),
            miru.SelectOption("Racoon", "racoon", emoji="🦝"),
            miru.SelectOption("Kangaroo", "kangaroo", emoji="🦘"),
        ]
    )
    async def select_menu(self, select:miru.Select, ctx: miru.Context) -> None:
        animal = select.values[0]
        async with ctx.app.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(description=res["fact"], colour=0x3B9DFF)
                embed.set_image(res["image"])

                animal = animal.replace("_", " ")

                await ctx.edit_response(
                    f"Here's a {animal} for you! :3", embed=embed, components=[]
                )
            else:
                await ctx.edit_response(
                    f"API returned a {res.status} status :c", components=[]
                )
    async def on_timeout(self) -> None:
        await self.message.edit("The menu timed out :c", components=[])

    async def view_check(self, ctx: miru.Context) -> bool:
        return ctx.user.id == self.author.id

@fun_group.child
@lightbulb.command("animal", "Get a fact + picture of a cute animal :3")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def animal_subcommand(ctx: lightbulb.Context) -> None:
    view = AnimalView(ctx.author)
    resp = await ctx.respond(
        "Pick an animal from the dropdown :3", components=view.build()
    )
    msg = await resp.message()

    await view.start(msg)
    await view.wait()

@fun_group.child
@lightbulb.option("user", "Defaults to author.", hikari.User, required=False)
@lightbulb.command("isthisgod", "Checks if the user is God.", pass_options=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def is_god(ctx: lightbulb.Context, user: Optional[hikari.User]) -> None:
    target = user or ctx.author
    if target.id == MAKER:
        await ctx.respond("Yes.")
    else:
        await ctx.respond("No.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun_plugin)
