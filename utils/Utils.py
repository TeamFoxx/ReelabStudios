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
    # Create an embed with a specific color
    website_embed = discord.Embed(colour=0x2b2d31)

    # Set the author of the embed with a message and a link to the website
    website_embed.set_author(
        name="Your request is currently being processed, depending on your network this could take a few seconds.",
        url="https://reelab.studio/",
        icon_url="attachment://reelab_logo_white.png"
    )

    # Define the path to the logo image
    icon_path = "./data/pictures/reelab_logo_white.png"

    # Create a discord file from the logo image
    icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

    # Edit the interaction response with the embed and the image attachment
    await interaction.edit(embed=website_embed, attachments=[icon_file], components=[])


async def header():
    """
    Creates and returns an embed for the header with the Reelab Studio information.
    """
    # Create a new embed with the specified color from the configuration
    header = discord.Embed(colour=config.HEADER_COLOR)

    # Set the author of the embed with the name, URL, and icon image
    header.set_author(
        name="www.reelab.studio",
        url="https://reelab.studio/",
        icon_url="attachment://reelab_logo_white.png"
    )

    # Set the image of the embed with the banner
    header.set_image(
        url="attachment://reelab_banner_white.gif"
    )

    # Return the created embed
    return header


async def attachments():
    """
    Prepares and returns the attachments for the Reelab Studio message.
    """
    # Define the file path for the banner image
    banner_path = "./data/pictures/reelab_banner_white.gif"
    # Create a Discord file object for the banner image
    banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

    # Define the file path for the icon image
    icon_path = "./data/pictures/reelab_logo_white.png"
    # Create a Discord file object for the icon image
    icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

    # Define the file path for the footer image
    footer_path = "./data/pictures/reelab_banner_blue.png"
    # Create a Discord file object for the footer image
    footer_file = discord.File(footer_path, filename="reelab_banner_blue.png")

    # Return the created Discord file objects for the banner, icon, and footer images
    return banner_file, icon_file, footer_file


# ⏤ { language functions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def load_language_data_product_overview(user_language: str) -> dict:
    """
    Loads the language data for the Discord bot from the specified file based on the user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    # Define the directory and file path for the language data
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/products_language_file.json"
    print(file_path)

    try:
        # Open and load the language data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            # Check if the specified user_language is available
            if user_language in language_data:
                return language_data[user_language]
            else:
                # If user_language is not found, print a warning and return an empty dictionary
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        # Log an error if the language file is not found
        logging.error(f"Language file '{file_path}' not found.")
        return {}


def load_language_data_discord_bot(user_language: str) -> dict:
    """
    Loads the language data for the Discord bot from the specified file based on the user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    # Define the directory and file path for the language data
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/order_discord_bot_language_file.json"
    print(file_path)

    try:
        # Open and load the language data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            # Check if the specified user_language is available
            if user_language in language_data:
                return language_data[user_language]
            else:
                # If user_language is not found, print a warning and return an empty dictionary
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        # Log an error if the language file is not found
        logging.error(f"Language file '{file_path}' not found.")
        return {}


def load_language_data_website(user_language: str) -> dict:
    """
    Loads the language data for the website from the specified file based on the user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    # Define the directory and file path for the language data
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/order_website_language_file.json"

    try:
        # Open and load the language data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            # Check if the specified user_language is available
            if user_language in language_data:
                return language_data[user_language]
            else:
                # If user_language is not found, print a warning and return an empty dictionary
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        # Log an error if the language file is not found
        logging.error(f"Language file '{file_path}' not found.")
        return {}


def load_language_data_graphic(user_language: str) -> dict:
    """
    Loads the language data for graphic services from the specified file based on the user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    # Define the directory and file path for the language data
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/order_graphic_language_file.json"

    try:
        # Open and load the language data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            # Check if the specified user_language is available
            if user_language in language_data:
                return language_data[user_language]
            else:
                # If user_language is not found, print a warning and return an empty dictionary
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        # Log an error if the language file is not found
        logging.error(f"Language file '{file_path}' not found.")
        return {}


def load_language_data_customer_support(user_language: str) -> dict:
    """
    Loads the language data for customer support from the specified file based on the user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    # Define the directory and file path for the language data
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/languages/customer_support_language_file.json"

    try:
        # Open and load the language data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            # Check if the specified user_language is available
            if user_language in language_data:
                return language_data[user_language]
            else:
                # If user_language is not found, print a warning and return an empty dictionary
                print(f"Warning: Language code '{user_language}' not found. Falling back to English.")
                return {}
    except FileNotFoundError:
        # Log an error if the language file is not found
        logging.error(f"Language file '{file_path}' not found.")
        return {}
