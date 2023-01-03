from datetime import datetime
from typing import Optional

import hikari
import lightbulb

info_plugin = lightbulb.Plugin("info")

@info_plugin.command
@lightbulb.command("info", "Find all the info plugins here!")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def info_group(ctx: lightbulb.Context):
    pass

@info_group.child
@lightbulb.command("server", description="Get info on the server.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def serverinfo(ctx: lightbulb.Context) -> None:
    if not (guild := ctx.get_guild()):
        await ctx.respond("This command may only be used in servers.")
        return
    
    created_at = int(guild.created_at.timestamp())
    owner = await guild.fetch_owner()


    embed = (
        hikari.Embed(
        title=f"Server Info - {guild.name}",
        description=f"ID - `{guild.id}`",
        timestamp=datetime.now().astimezone(),
        color=0x990000
        )
        .set_footer(
            text=f"Requested by {ctx.author.username}", 
            icon=ctx.author.avatar_url
        )
        .add_field(
            "Server created on", 
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)", 
            inline=True
        )
        .add_field(
            "Server owner",
            f"{owner.mention}",
            inline=True
        )
        .set_thumbnail(guild.icon_url)
    )

    await ctx.respond(embed=embed)
    
@info_group.child
@lightbulb.option(
    "target", "The user to get information about.", hikari.User, required=False
)
@lightbulb.command("user", "Get info on a server member.", pass_options=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def userinfo(ctx: lightbulb.Context, target: Optional[hikari.User] = None) -> None:
    if not (guild := ctx.get_guild()):
        await ctx.respond("This command may only be used in servers.")
        return

    target = target or ctx.author
    target = ctx.bot.cache.get_member(guild, target)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone
    roles = sorted(
        roles, key=lambda role: role.position, reverse=True
    )  # sort them by position, then reverse the order to go from top role down
    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.author.username}",
            icon=ctx.author.display_avatar_url,
        )
        .set_thumbnail(target.avatar_url)
        .add_field(
            "Bot?",
            "Yes" if target.is_bot else "No",
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)