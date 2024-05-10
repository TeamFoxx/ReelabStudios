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
from discord import Button, ButtonStyle, Modal, TextInput
from discord.ext import commands

import config
from utils import header, attachments, processing_response

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

user_data = {}
counting_file_path = "data/counting.json"


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
def load_language(user_id):
    # Define user language and load language data
    user_info = user_data.get(user_id, {})
    user_language = user_info.get('user_language', 'en')
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "languages/order_website_language_file.json"
    language = load_language_data(file_path, user_language)
    return language


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


def load_counting():
    """
    Loads the counting value from the file if it exists, otherwise returns 0.
    """
    try:
        with open(counting_file_path, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_counting(counting):
    """
    Saves the counting value to the file.
    """
    with open(counting_file_path, "w") as file:
        file.write(str(counting))


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BuyWebsite(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.order_product_channel_id = 1216178294458814526
        self.official_staff_id = 1216137762537996479

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_select('^products$')
    async def website_products(self, interaction, select_menu):
        # Check if the selected value of the select menu is "order_discord_bot"
        if select_menu.values[0] == "order_website":
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
            script_directory = Path(__file__).resolve().parent.parent
            file_path = script_directory / "languages/order_website_language_file.json"

            # Load language data based on the user's language preference
            language = load_language_data(file_path, user_language)

            # Retrieve emojis
            log_membershipscreening = self.bot.get_emoji(config.EMOJIS["log_membershipscreening"])
            plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])

            # remove old message
            await processing_response(interaction)

            # Header over Bot message
            header_embed = await header()

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["web_personalized_site_description"].format(plant_plant=plant_plant),
                color=config.EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await attachments()

            # creates a list of buttons to be sent
            buttons = [
                Button(
                    style=ButtonStyle.green,
                    emoji=log_membershipscreening,
                    label=language["order_website_accept_tos"],
                    custom_id="website_accept_tos",
                )
            ]

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header_embed, description],
                                   attachments=[banner_file, icon_file, footer_file],
                                   components=[buttons]
                                   )

    @commands.Cog.on_click("^website_accept_tos$")
    async def order_website_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Define user language and load language data
        user_info = user_data.get(user.id, {})

        # Load selected language
        language = load_language(user.id)

        # Log all user information that have been saved
        logging.info(f'{str(user.id)} - Website ordered by user: %s', user_info)

        # Get Order Product channel for thread creation
        channel = ctx.guild.get_channel(self.order_product_channel_id)

        # Get Official Staff role
        staff = ctx.guild.get_role(self.official_staff_id)

        # Retrieve emojis
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])
        community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])
        promo = self.bot.get_emoji(config.EMOJIS["promo"])

        # Load the current counting
        counting = load_counting()

        # Create a thread with a unique name based on the counting
        thread = await channel.create_thread(
            name=f"#{counting:04} | {user} | Website",
            reason=f"#{counting:04} | {user} | Website",
            private=True,
            invitable=True
        )

        # Increment and save the counting for future threads
        counting += 1
        save_counting(counting)

        # Remove old message
        await processing_response(ctx)

        # Header over Bot message
        header_embed = await header()

        # Send summary in thread.
        description = discord.Embed(
            description=language["order_website_personalized_thread_message"].format(user=user.mention,
                                                                                     plant_plant=plant_plant,
                                                                                     community_advisor=community_advisor),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(language["order_website_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[header_embed, description],
                          files=[banner_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.blurple,
                                  emoji=promo,
                                  label=language["order_website_thread_code_button"],
                                  custom_id="website_discount_code",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["order_website_thread_price_button"],
                                  custom_id="website_pricing_information",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=function_cross,
                                  label=language["order_website_thread_close_button"],
                                  custom_id="close_website_order",
                              )
                          ]]
                          )

        # Send summary in thread.
        user_message = discord.Embed(
            description=language["order_website_user_message"].format(thread=thread.mention),
            color=config.EMBED_COLOR,
        )
        user_message.set_image(url="attachment://reelab_banner_blue.png")
        user_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header_embed, user_message],
                       attachments=[banner_file, icon_file, footer_file],
                       )

    @commands.Cog.on_click("^website_pricing_information$")
    async def website_pricing_information(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Log pricing information
        logging.info(f'{str(user.id)} - Pricing information called by: %s', user.name)

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
        community_admin = self.bot.get_emoji(config.EMOJIS["community_admin"])

        # Send pricing information in chat.
        response_message = discord.Embed(
            color=config.EMBED_COLOR,
            description=language["order_website_pricing_information"].format(plantbig_plant=plantbig_plant,
                                                                             log_memberjoin=log_memberjoin,
                                                                             community_admin=community_admin)
        )
        await ctx.respond(embed=response_message, hidden=True)

    @commands.Cog.on_click("^website_discount_code$")
    async def website_discount_code(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Log pricing information
        logging.info(f'{str(user.id)} - Pricing information called by: %s', user.name)

        # Define the modal with input fields for bot name and status
        modal = Modal(
            title=language["order_website_discount_code_modal_title"],
            custom_id=f'website_discount_code',
            components=[
                [
                    TextInput(
                        label=language["order_website_discount_code_modal_name_lable"],
                        custom_id='code',
                        required=True,
                        style=1,
                        max_length=28,
                    )
                ]
            ]
        )

        # Respond to the interaction with the modal
        await ctx.respond_with_modal(modal)

    @commands.Cog.on_submit('^website_discount_code$')
    async def website_submit_discount_code(self, ctx: discord.ModalSubmitInteraction):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        promo = self.bot.get_emoji(config.EMOJIS["promo"])

        # Get bot name and status entered by the user
        code = ctx.get_field('code').value or None

        # Check if the entered code exists in the discount codes dictionary
        if code in config.DISCOUNT_CODES:
            discount_value = config.DISCOUNT_CODES[code]

            if discount_value == 0:
                # Send a message indicating the value of the discount code
                discount_code_message = discord.Embed(
                    color=config.EMBED_COLOR,
                    description=language["order_website_discount_code_valid_value_0"].format(promo=promo,
                                                                                             code=code)
                )
                await ctx.respond(embed=discount_code_message, hidden=False)
            else:
                # Send a message indicating the value of the discount code
                discount_code_message = discord.Embed(
                    color=config.EMBED_COLOR,
                    description=language["order_website_discount_code_valid_value"].format(promo=promo,
                                                                                           code=code,
                                                                                           discount_value=discount_value)
                )
                await ctx.respond(embed=discount_code_message, hidden=False)

        else:
            # Send a message indicating that the code does not exist
            discount_code_message = discord.Embed(
                color=config.EMBED_COLOR,
                description=language["order_website_discount_code_not_valid"]
            )
            await ctx.respond(embed=discount_code_message, hidden=True)

    @commands.Cog.on_click("^close_website_order$")
    async def order_website_close_thread(self, ctx: discord.ComponentInteraction, button):
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
    reelab_bot.add_cog(BuyWebsite(reelab_bot))
