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

import discord
from discord import Button, ButtonStyle
from discord.ext import commands

import config
from main import reelab
from utils.Utils import header, attachments, processing_response, load_language_data_order_bundle


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class BuyBundle(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_select('^products$')
    async def order_bundle(self, interaction, select_menu):
        selected = select_menu.values[0].split(":")

        # Check if the selected value of the select menu is "order_discord_bot"
        if selected[0] == "order_bundle":
            order_id = selected[1]
            order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

            # Load language data based on the user's language preference
            language = load_language_data_order_bundle(order.user_language)

            # Retrieve emojis
            community_planner = self.bot.get_emoji(config.EMOJIS["community_planner"])
            community_member = self.bot.get_emoji(config.EMOJIS["community_member"])
            community_eventhost = self.bot.get_emoji(config.EMOJIS["community_eventhost"])
            community_admin = self.bot.get_emoji(config.EMOJIS["community_admin"])

            # remove old message
            await processing_response(interaction)

            # Header over Bot message
            header_embed = await header()

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["description"].format(community_planner=community_planner,
                                                           community_member=community_member,
                                                           community_eventhost=community_eventhost,
                                                           community_admin=community_admin),
                color=config.EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await attachments()

            # creates a list of buttons to be sent
            buttons = [
                Button(
                    style=ButtonStyle.url,
                    emoji="🌐",
                    label="www.reelab.studio",
                    url="https://reelab.studio/"
                )
            ]

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header_embed, description],
                                   attachments=[banner_file, icon_file, footer_file],
                                   components=[buttons]
                                   )


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(BuyBundle(reelab_bot))
