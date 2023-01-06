from datetime import datetime
from datetime import timedelta
import re
from random import randint

import hikari
import lightbulb

inside_plugin = lightbulb.Plugin("inside_jokes", "The title says it all (mostly)")

ancom = hikari.Emoji.parse("<:ancom:1057084080153436180>")

# I just asked my friends what they wanted the bot to do here
french = re.compile(r".*i love french.*")
giveUp = re.compile(r".*give.+up.*")
hear = re.compile(r".*hear that\?.*")
hate = re.compile(r".*i hate.+")
convo = re.compile(r".*talking back to me\?.*")
makima = re.compile(r".*makima.*")
godBless = re.compile(r".*god bless you.*")
areGod = re.compile(r".*are.+god")
thank = re.compile(r".*thank.*")
friends = re.compile(r".*(we('re| are)|are we) friends")
mitski = re.compile(r".*mitski.*")
useless = re.compile(r".*i('m| am) useless")

"""Nobody nooooobody nooooooobody noooooooobdoy oooo nobody nOOOOBODY
Carryyy mee oooOoOOOOoUUUuuuuuttt"""

@inside_plugin.listener(hikari.GuildMessageCreateEvent)
async def inside_jokes(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.content or not event.is_human:
        return
    print(event.content)
    
    author = event.author
    timeout = datetime.now() + timedelta(seconds=60)
    
    content = event.content.lower()
    
    # A bunch of if statements to see if message contains thing
    if french.match(content):
        await event.message.respond(f"Timed out {author.mention}, go to jail.")
        try:
            await author.edit(communication_disabled_until=timeout)
        except hikari.ForbiddenError:
            await author.send("Apparently I can't time you out. You still deserve to be for liking french though.")
    if giveUp.match(content):
        await event.message.respond("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if hear.match(content):
        await event.message.respond("I hear **YOU**. And I wish I didn't.")
    if hate.match(content):
        await event.message.respond("I hate *you*")
    if convo.match(content):
        await event.message.respond("Yes that's how a coversation works.")
    if makima.match(content):
        await event.message.respond("Makima is always watching...")
    if godBless.match(content):
        await event.message.respond("God hasn't been blessing me lately :rolling_eyes:")
    if areGod.match(content):
        await event.message.respond(f"No gods, no masters! {ancom}")
    if thank.match(content):
        await event.message.respond(f"I don't know why you're thanking me, my dear {author.mention}, but you're welcome to be part of my perfection :relieved:")
    if friends.match(content):
        await event.message.respond("I'm gonna set you on fire", reply=event.message.id)
    if mitski.match(content):
        random = randint(1, 2)
        if random == 1:
            await event.message.respond("Nobody nooooobody nooooooobody noooooooobody noboooody oooo nobody noBODY NOOOOOBODY", reply=True)
        else:
            await event.message.respond("Carryyy mee oooOoOOOOoUUUuuuuuttt", reply=True)
    if useless.match(content):
        await event.message.respond("You're not useless!", reply=True, mentions_reply=True)
    
    

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(inside_plugin)