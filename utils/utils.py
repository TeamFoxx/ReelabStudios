# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Developed by Foxx
# »› Copyright © 2024 Aurel Hoxha. All rights reserved.
# »› GitHub: https://github.com/TeamFoxx
# »› For support and inquiries, please contact info@aurelhoxha.de
# »› Use of this program is subject to the terms the terms of the MIT licence.
# »› A copy of the license can be found in the "LICENSE" file in the root directory of this project.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { imports } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
import json
import logging
from pathlib import Path

import discord
import config


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='../bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ⏤ { text functions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

async def processing_response(interaction):
    """
    Sends a processing response to the interaction by editing it with a loading message.
    """
    website_embed = discord.Embed(colour=0x2b2d31)
    website_embed.set_author(
        name="Your request is currently being processed, depending on your network this could take a few seconds.",
        url="https://reelab.studio/",
        icon_url="attachment://reelab_logo_white.png"
    )

    icon_path = "./data/pictures/reelab_logo_white.png"
    icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

    await interaction.edit(embed=website_embed, attachments=[icon_file], components=[])


async def header():
    """
    Creates and returns an embed for the header with the Reelab Studio information.
    """
    header = discord.Embed(colour=config.HEADER_COLOR)
    header.set_author(
        name="www.reelab.studio",
        url="https://reelab.studio/",
        icon_url="attachment://reelab_logo_white.png"
    )
    header.set_image(
        url="attachment://reelab_banner_white.gif"
    )
    return header


async def attachments():
    """
    Prepares and returns the attachments for the Reelab Studio message.
    """
    banner_path = "./data/pictures/reelab_banner_white.gif"
    banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

    icon_path = "./data/pictures/reelab_logo_white.png"
    icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

    footer_path = "./data/pictures/reelab_banner_blue.png"
    footer_file = discord.File(footer_path, filename="reelab_banner_blue.png")

    return banner_file, icon_file, footer_file


# ⏤ { language functions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def load_language_data(user_language: str) -> dict:
    """
    Loads the language data from the specified file and selects the language based on user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/order_discord_bot_language_file.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            if user_language in language_data:
                return language_data[user_language]
            else:
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        logging.error(f"Language file '{file_path}' not found.")
        return {}

