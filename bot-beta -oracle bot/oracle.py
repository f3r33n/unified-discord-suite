import os
import asyncio
from dotenv import load_dotenv
import discord
import random
import time

from cohere_client import ask_oracle, oracle_observe

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN not found in .env")

# --------------------------------------------------
# DISCORD INTENTS
# --------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

# --------------------------------------------------
# CREATE CLIENT
# --------------------------------------------------

client = discord.Client(intents=intents)

# --------------------------------------------------
# ORACLE SETTINGS
# --------------------------------------------------

ROOM_NAME = "ROOM404"

MOODS = [
    "neutral",
    "helpful",
    "stable"
]

current_mood = random.choice(MOODS)

# --------------------------------------------------
# MEMORY
# --------------------------------------------------

recent_messages = []
last_random_message = 0
last_message = ""

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

async def oracle_say(channel, text):

    print("\n" + "=" * 50)
    print("ORACLE_SAY CALLED")
    print(repr(text))
    print("=" * 50 + "\n")

    async with channel.typing():
        await asyncio.sleep(random.uniform(0.1, 0.5))

    await channel.send(text)

# --------------------------------------------------
# STARTUP EVENT
# --------------------------------------------------

@client.event
async def on_ready():

    print("-" * 50)
    print(f"Logged in as: {client.user}")
    print(f"Current Mood: {current_mood}")
    print("Oracle is operational.")
    print("-" * 50)

# --------------------------------------------------
# MESSAGE EVENT
# --------------------------------------------------

@client.event
async def on_message(message):

    # Ignore bots
    if message.author == client.user:
        return

    msg = message.content.strip()
    msg_lower = msg.lower()
    

    print(
        f"[{message.author}] "
        f"in #{message.channel}: "
        f"{msg}"
    )
      




    # Store conversation history

    # store last message and include random value for debugging/context
    recent_messages.append(
        f"{message.author.display_name}: {msg}"
    )

    if len(recent_messages) > 11:
        recent_messages.pop(0)

    try:

        # Oracle only wakes when mentioned

        if (
            client.user in message.mentions
            or "oracle" in msg_lower
        ):

            print("ORACLE ACTIVATED")

            cleaned_message = msg

            cleaned_message = cleaned_message.replace(
                f"<@{client.user.id}>",
                ""
            )

            cleaned_message = cleaned_message.replace(
                f"<@!{client.user.id}>",
                ""
            )

            cleaned_message = cleaned_message.replace(
                "oracle",
                "",
                
            )

            cleaned_message = cleaned_message.strip().lower()

            # Empty mention

            if cleaned_message == "":

                await oracle_say(
                    message.channel,
                    random.choice([
                        "Yes?",
                        "I'm listening.",
                        "What would you like to know?",
                        "Go ahead.",
                        "How can I help?"
                    ])
                )

                return

            # Greeting detection

            GREETING_MESSAGES = [
                "hi",
                "hello",
                "hey",
                "greetings",
                "sup"
            ]

            if cleaned_message in GREETING_MESSAGES:
                await oracle_say(
                    message.channel,
                    random.choice([
                        "Hello.",
                        "Greetings.",
                        "Hey there.",
                        "Good to see you.",
                        "Hello. What can I help you with?"
                    ])
                )

                return

            # --------------------------------------------------
            # AI BLOCK
            # --------------------------------------------------

            try:

                print(f"REQUEST: {cleaned_message}")

                conversation_context = "\n".join(
                    recent_messages[-10:]
                )

                print("COHERE REQUEST MADE")

                response = ask_oracle(
                    cleaned_message,
                    conversation_context=conversation_context
                )

                print("COHERE SUCCESS")
                print(f"RESPONSE: {repr(response)}")

            except Exception as e:

                print(f"COHERE ERROR: {e}")

                response = random.choice([
                    "I'm having trouble processing that right now.",
                    "Something went wrong. Try again.",
                    "Oracle appears temporarily distracted.",
                    "I lost my train of thought. Ask again.",
                    "The response archives are currently unavailable."
                ])

            print(f"SENDING: {repr(response)}")

            await oracle_say(
                message.channel,
                response
            )

            print("MESSAGE SENT")
            return

        else:
            global last_random_message
            current_time = time.time()
            # possible random observation
            rand_val = random.random()
            if (
                current_time - last_random_message > 45
                and rand_val < 0.60
            ):
                last_random_message = current_time
                observation = oracle_observe(
                    conversation_context="\n".join(recent_messages)
                )
                # record oracle random observation in memory
                recent_messages.append(f"ORACLE (random): {observation}")
                await oracle_say(message.channel, observation)
    except Exception as e:

        print(f"ERROR: {e}")

# --------------------------------------------------
# RUN BOT
# --------------------------------------------------

client.run(TOKEN)