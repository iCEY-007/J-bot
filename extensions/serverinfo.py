from datetime import datetime

import hikari
import lightbulb

info_plugin = lightbulb.Plugin("info")

@info_plugin.command
@lightbulb.command("serverinfo", description="Get info on the server.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
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

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)