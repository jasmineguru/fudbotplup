import discord
import random
from data import dishes
from env import TOKEN

bot = discord.Client()


@bot.event
async def on_ready():
    print("BotPlup is up and running~")


@bot.event
async def on_message(msg):
    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    if msg.content == "ping":
        # Get latency of bot
        latency = bot.latency
        # Send re with latency to user
        await msg.channel.send("pong 🏓" + " \n" + "latency = " + str(latency.__round__(3)) + "ms")

    elif msg.content == "who are you":
        await msg.channel.send("P l u p I am! 👋")

    elif msg.content.lower() == "!guess":
        rng = random.randint(0, 12)
        i = 0
        lst = list(dishes.keys())  # access dict by index by accessing dict.keys

        desc = lst[rng]  # store key to var selecting key/value pair based on randomized option
        identity = dishes[desc]

        print(desc, identity)
        # await msg.channel.send(desc)  # print out key info (question prompt) + add embed if time later
        emb = discord.Embed(title="Can you guess this dish's country of origin?")
        emb.set_image(url=desc)
        emb.set_footer(text="Note: Your guess must start with the prefix \"!\"")
        await msg.channel.send(embed=emb)

        i = 0
        while i < 3:  # iterate through 3 attempts
            def check(mg):
                # check whether input is of a valid type
                return isinstance(mg.content.lower(), str) and mg.content.startswith("!")
            mg = await bot.wait_for("message", check=check)  # take in user response and store to temp variable

            # compare variable to value of key/value pair
            if mg.content.lower()[1:] == identity:
                i = 4  # increment to exit loop
                await msg.channel.send("Correct!")  # if match -> correct guess
            else:
                i += 1  # increment to iterate once more
                # else -> incorrect guess
                await msg.channel.send("Incorrect, try again? You have " + str(3 - i) + " attempts remaining")

        if i == 3:  # Case for when user used all 3 attempts
            await msg.channel.send("Unfortunate, you ran out of guesses, the answer was ||`" + identity + "`||")

bot.run(TOKEN)  # access from .env file later
