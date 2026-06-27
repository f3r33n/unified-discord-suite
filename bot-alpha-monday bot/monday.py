import os
import random
import asyncio
import discord
import time
from dotenv import load_dotenv
from cohere_client import ask_monday
# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")

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
# MONDAY SETTINGS
# --------------------------------------------------

ROOM_NAME = "ROOM404"

MOODS = [
    "observant",
    "annoyed",
    "neutral",
    "investigative"
]

CURRENT_MOOD = random.choice(MOODS)

# Stores recent conversation history
recent_messages = []
last_random_message = 0

# --------------------------------------------------
# RESPONSE DATABASE
# --------------------------------------------------

GREETINGS = [
    "Another wanderer enters ROOM404.",
    "Greetings, wanderer.",
    "Your arrival has been recorded.",
    "The archive acknowledges your presence."
]

STATUS_RESPONSES = [
    "Systems operational. Reality remains stable.",
    "No critical incidents detected.",
    "ROOM404 remains under observation.",
    "Archive integrity acceptable."
]

GREETING_MESSAGES = [
    "hi",
    "hello",
    "hey",
    "greetings",
    "sup",
    "yo"
]

THANK_RESPONSES = [
    "You're welcome, wanderer.",
    "Acknowledged.",
    "Your gratitude has been archived."
]

UNKNOWN_RESPONSES = [
    "The archive contains no record of that.",
    "Query rejected by ROOM404.",
    "Information unavailable.",
    "That file appears corrupted.",
    "Access denied, wanderer."
]

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

async def monday_say(channel, text):

    print("\n" + "=" * 50)
    print("MONDAY_SAY CALLED")
    print(repr(text))
    print("=" * 50 + "\n")

    async with channel.typing():
        await asyncio.sleep(random.uniform(0.1, 0.7))

    await channel.send(text)

# --------------------------------------------------
# STARTUP EVENT
# --------------------------------------------------

@client.event
async def on_ready():

    print("-" * 50)
    print(f"Logged in as: {client.user}")
    print(f"Current mood: {CURRENT_MOOD}")
    print("Monday is operational.")
    print("-" * 50)

# --------------------------------------------------
# MESSAGE EVENT
# --------------------------------------------------

@client.event
async def on_message(message):

    # Ignore all bots (including self)
    if message.author.bot:
        return

    msg = message.content.strip()
    msg_lower = msg.lower()

    print(
        f"[{message.author}] "
        f"in #{message.channel}: "
        f"{msg}"
    )

    # ----------------------------------------------
    # STORE LAST 11 MESSAGES
    # Useful later for cohere context
    # ----------------------------------------------

    recent_messages.append(
        f"{message.author.display_name}: {msg}"
    )

    if len(recent_messages) > 11:
        recent_messages.pop(0)

    try:

        # ------------------------------------------
        # DIRECT MENTION DETECTED
        # ------------------------------------------

        if (
            client.user in message.mentions
            or "monday" in msg_lower
            or "Monday" in msg
        ):
            print("MONDAY ACTIVATED")

            # Remove mention text
            cleaned_message = msg

            cleaned_message = cleaned_message.replace(
                f"<@{client.user.id}>",
                ""
            )

            cleaned_message = cleaned_message.replace(
                f"<@!{client.user.id}>",
                ""
            )
            # Remove "monday" if user typed it naturally
            cleaned_message = cleaned_message.replace(
                "monday",
                "",
                1
            )

            cleaned_message = cleaned_message.strip().lower()

            # Empty mention

            if cleaned_message == "":
                await monday_say(
                    message.channel,
                    random.choice([
                        "Yes, wanderer?",
                        "You called?",
                        "I am listening.",
                        "State your query."
                    ])
                )
                return
            # Greetings

            GREETING_MESSAGES = [
                "hi",
                "hello",
                "hey",
                "greetings",
                "sup",
                "yo"
            ]
            if cleaned_message in GREETING_MESSAGES:

                await monday_say(
                    message.channel,
                    random.choice(GREETINGS)
                )

                return
            # Status

            elif "status" in cleaned_message:

                await monday_say(
                    message.channel,
                    random.choice(STATUS_RESPONSES)
                )

            # Identity

            elif (
                "who are you" in cleaned_message
                or "whoareyou" in cleaned_message
            ):

                await monday_say(
                    message.channel,
                    f"I am Monday, caretaker of {ROOM_NAME}."
                )



            # Thank you

            elif "thank" in cleaned_message:

                await monday_say(
                    message.channel,
                    random.choice(THANK_RESPONSES)
                )

            else:

                print("MONDAY ACTIVATED")

                try:

                    print(f"REQUEST: {cleaned_message}")

                    conversation_context = "\n".join(recent_messages)
                    print("COHERE REQUEST MADE")
                    response = ask_monday(
                        cleaned_message,
                        conversation_context=conversation_context
                    )
                    print("COHERE SUCCESS")
                    print(f"RESPONSE: {repr(response)}")

                except Exception as e:

                    print(f"COHERE ERROR: {e}")

                    response = random.choice([
                        "The archive lost its train of thought.",
                        "ROOM404 misplaced that file.",
                        "Ask me again in a moment, wanderer.",
                        "Something rattled the servers."
                    ])

                print(f"SENDING: {repr(response)}")

                await monday_say(
                    message.channel,
                    response
                )

                print("MESSAGE SENT")

        # ------------------------------------------
        # NATURAL SERVER PRESENCE
        # ------------------------------------------

        else:
            global last_random_message
            current_time = time.time()
            # 300 seconds cooldown and 20% chance to respond naturally
            if (current_time - last_random_message > 20) and (random.random() < 0.70):
                last_random_message = current_time
                await monday_say(
                    message.channel,
                    random.choice([
                        "room404 has choosen to ignore this conversation.",
                        "Observation recorder, noone here seems to be qualified.",
                        "carry on- this should be intresting.",
                        "Reality remans stable, barely.",
                        "I have concerns.",
                        "Statistically speaking, somebody here is wrong.",
                        "I wish i hadn't heard that.",
                        "This conversation has been archived for future embarrassments."
                    ])
                )

    except Exception as e:

        print(f"ERROR: {e}")

# --------------------------------------------------
# RUN BOT
# --------------------------------------------------

client.run(TOKEN)