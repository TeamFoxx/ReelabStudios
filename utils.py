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

import logging
import discord
import config


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ⏤ { functions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

async def processing_response(interaction: discord.ComponentInteraction):
    """
    Sends a processing response to the interaction by editing it with a loading message.
    """
    website_embed = discord.Embed(colour=0x2b2d31)
    website_embed.set_author(
        name="Your request is currently being processed, depending on your network this could take a few seconds.",
        url="https://reelab.studio/",
        icon_url="attachment://reelab_logo_white.png"
    )

    icon_path = "./pictures/reelab_logo_white.png"
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
    banner_path = "./pictures/reelab_banner_white.gif"
    banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

    icon_path = "./pictures/reelab_logo_white.png"
    icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

    footer_path = "./pictures/reelab_banner_blue.png"
    footer_file = discord.File(footer_path, filename="reelab_banner_blue.png")

    return banner_file, icon_file, footer_file
