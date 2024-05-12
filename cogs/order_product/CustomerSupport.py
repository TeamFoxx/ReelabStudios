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
from discord import Button, ButtonStyle
from discord.ext import commands

import config
from utlis.utils import header, processing_response, attachments

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

user_data = {}


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def load_language_data(file_path: Path, user_language: str) -> dict:
    """
    Loads the language data from the specified file and selects the language based on user_language.
    Returns the language dictionary if found, otherwise returns an empty dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            language_data = json.load(file)
            if user_language in language_data:
                return language_data[user_language]
            else:
                logging.warning(f"Language '{user_language}' not found in language file.")
                return {}
    except FileNotFoundError:
        logging.error(f"Language file '{file_path}' not found.")
        return {}


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CustomerSupport(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.order_product_channel_id = 1216178294458814526
        self.official_staff_id = 1216137762537996479
        self.customer_support_id = 1216142380571295855

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_select('^products$')
    async def customer_support(self, interaction, select_menu):
        # Check if the selected value of the select menu is "order_discord_bot"
        if select_menu.values[0] == "customer_support":
            # Import required modules
            from cogs.order_product.ProductPurchase import user_lang

            # Get the user ID from the interaction
            user = interaction.author

            # Retrieve user language information from user_lang
            user_info = user_lang.get(user.id, {})

            # Get the language attribute from user_info, default to 'en' if not found
            user_language = user_info.get('language', 'en')

            # Retrieve user data from the database or initialize an empty dictionary if not found
            user_info = user_data.get(user.id, {})

            # Update user information with the user_language
            user_info["user_language"] = user_language

            # Delete user data after processing
            if user.id in user_lang:
                del user_lang[user.id]
            else:
                pass

            # Update user data in the database
            user_data[user.id] = user_info

            # Retrieve the user's language preference
            user_language = user_info.get('user_language', 'en')

            # Define the file path for language data
            script_directory = Path(__file__).resolve().parent.parent.parent
            file_path = script_directory / "languages/customer_support_language_file.json"

            # Load language data based on the user's language preference
            language = load_language_data(file_path, user_language)

            # Log all user information that have been saved
            logging.info(f'{str(user.id)} - Customer Support requested by user: %s', user_info)

            # Get Order Product channel for thread creation
            channel = interaction.guild.get_channel(self.order_product_channel_id)

            # Get Official Staff role
            staff = interaction.guild.get_role(self.official_staff_id)
            customer_support = interaction.guild.get_role(self.customer_support_id)

            # Retrieve emojis
            plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])
            function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])
            community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])

            # Create a thread with a unique name based on the counting
            thread = await channel.create_thread(
                name=f"{user} | Support",
                reason=f"{user} | Support",
                private=True,
                invitable=True
            )

            # Remove old message
            await processing_response(interaction)

            # Header over Bot message
            header_embed = await header()

            # Send summary in thread.
            description = discord.Embed(
                description=language["support_thread_message"].format(user=user.mention,
                                                                      plant_plant=plant_plant,
                                                                      community_advisor=community_advisor),
                color=config.EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await attachments()

            # Send the bot summary message with buttons for pricing information and closing the order
            await thread.send(language["support_thread_ping_message"].format(user=user.mention,
                                                                             staff=staff.mention,
                                                                             support=customer_support.mention))
            await thread.send(embeds=[header_embed, description],
                              files=[banner_file, icon_file, footer_file],
                              components=[[
                                  Button(
                                      style=ButtonStyle.grey,
                                      emoji=function_cross,
                                      label=language["support_thread_close_button"],
                                      custom_id="close_support_thread",
                                  )
                              ]]
                              )

            # Send summary in thread.
            user_message = discord.Embed(
                description=language["support_user_message"].format(thread=thread.mention),
                color=config.EMBED_COLOR,
            )
            user_message.set_image(url="attachment://reelab_banner_blue.png")
            user_message.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await attachments()

            # Edit the message with updated embed and components
            await interaction.edit(embeds=[header_embed, user_message],
                                   attachments=[banner_file, icon_file, footer_file],
                                   )

    @commands.Cog.on_click("^close_support_thread$")
    async def close_support_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Log thread closing
        logging.info(f'{str(user.id)} - the thread has been closed by: %s', user.name)

        # Get the current thread and its name
        thread = ctx.channel
        thread_name = thread.name

        # Update the thread name to indicate it's closed
        new_thread_name = f"{thread_name} | closed"

        # Prepare response message for closing the thread
        response_message = discord.Embed(
            color=config.EMBED_COLOR,
            description="Thread is being closed and archived."
        )
        await ctx.respond(embed=response_message, hidden=True)

        # Remove all members from the thread
        for member in thread.members:
            await thread.remove_member(member)

        # Edit the thread's name to reflect closure
        await thread.edit(name=new_thread_name)

        # Archive the thread
        await thread.edit(archived=True)

        # Delete user data after processing
        if user_data.get(user.id):
            del user_data[user.id]
        else:
            return


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(CustomerSupport(reelab_bot))
