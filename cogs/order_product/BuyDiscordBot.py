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
from discord import SelectOption, SelectMenu, Button, ButtonStyle, Modal, TextInput
from discord.ext import commands

import config
from utils import attachments, processing_response

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
user_data = {}

counting_file_path = "data/counting.json"


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def load_language(user_id):
    # Define user language and load language data
    user_info = user_data.get(user_id, {})
    user_language = user_info.get('user_language', 'en')
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "languages/order_discord_bot_language_file.json"
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


def calculate_price(user_amount_pricing: int, user_id: int) -> str:
    """
    Calculates the price based on the user's amount pricing and updates user data accordingly.
    Returns the calculated price as a string.
    """
    user_info = user_data.get(user_id, {})
    if user_amount_pricing == 1:
        price = config.discord_bot_user_based_pricing_1
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "> 1k"
    elif user_amount_pricing == 2:
        price = config.discord_bot_user_based_pricing_2
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "1k-2.5k"
    elif user_amount_pricing == 3:
        price = config.discord_bot_user_based_pricing_3
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "2.5k-5k"
    elif user_amount_pricing == 4:
        price = config.discord_bot_user_based_pricing_4
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "< 5k"
    else:
        price = "Invalid user count"
    user_data[user_id] = user_info
    return price


def format_price(price):
    """
    Formats the given price to display as a string with Euro symbol.
    Returns the formatted price string.
    """
    if price.is_integer():
        return f"{int(price)}€"
    else:
        return f"{price:.2f}€"


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

logging.basicConfig(filename='bot.log', level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')


class BuyDiscordBot(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.order_product_channel_id = 1216178294458814526
        self.official_staff_id = 1216137762537996479

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_select('^products$')
    async def discord_bot_products(self, interaction, select_menu):
        # Check if the selected value of the select menu is "order_discord_bot"
        if select_menu.values[0] == "order_discord_bot":
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
            file_path = script_directory / "languages/order_discord_bot_language_file.json"

            # Load language data based on the user's language preference
            language = load_language_data(file_path, user_language)

            # Retrieve emojis
            community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
            community_admin = self.bot.get_emoji(config.EMOJIS["community_admin"])
            plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])

            # Remove old message
            await processing_response(interaction)

            # Header over Bot message
            header = discord.Embed(colour=config.HEADER_COLOR)
            header.set_author(
                name="www.reelab.studio",
                url="https://reelab.studio/",
                icon_url="attachment://reelab_logo_white.png"
            )
            header.set_image(
                url="attachment://choose_your_bot_type_white.png"
            )
            header_path = "./pictures/choose_your_bot_type_white.png"
            header_file = discord.File(header_path, filename="choose_your_bot_type_white.png")

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["discord_bot_products_description"].format(plantbig_plant=plantbig_plant, community_admin=community_admin),
                color=config.EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Load attachments
            banner_file, icon_file, footer_file = await attachments()

            # Add options to the select menu
            select_options = [
                SelectOption(
                    label=language["discord_personalized_bot_label"],
                    description=language["discord_personalized_bot_description"],
                    emoji=community_admin,
                    value='personalized_bot'
                ),
                SelectOption(
                    label=language["discord_modmail_bot_label"],
                    description=language["discord_modmail_bot_description"],
                    emoji=community_developer,
                    value='modmail_bot'
                ),
                SelectOption(
                    label=language["discord_music_bot_label"],
                    description=language["discord_music_bot_description"],
                    emoji=community_developer,
                    value='music_bot'
                ),
                SelectOption(
                    label=language["discord_admin_bot_label"],
                    description=language["discord_admin_bot_description"],
                    emoji=community_developer,
                    value='admin_bot'
                ),
                SelectOption(
                    label=language["discord_tempvoice_bot_label"],
                    description=language["discord_tempvoice_bot_description"],
                    emoji=community_developer,
                    value='tempvoice_bot'
                ),
                SelectOption(
                    label=language["discord_studies_bot_label"],
                    description=language["discord_studies_bot_description"],
                    emoji=community_developer,
                    value='studies_bot'
                )
            ]

            # Add the select menu
            bot_select_menu = SelectMenu(
                placeholder=language["discord_select_bot_options_placeholder"],
                options=select_options,
                custom_id='select_bot_options',
                max_values=1
            )

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header, description],
                                   attachments=[header_file, icon_file, footer_file],
                                   components=[[bot_select_menu]])

    @commands.Cog.on_select('^select_bot_options$')
    async def order_bot_step_1(self, interaction, select_menu):
        bot_type_mapping = {
            "modmail_bot": "Modmail Bot",
            "music_bot": "Music Bot",
            "admin_bot": "Admin Bot",
            "tempvoice_bot": "TempVoice Bot",
            "studies_bot": "Studies Bot"
        }

        user = interaction.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])
        log_membershipscreening = self.bot.get_emoji(config.EMOJIS["log_membershipscreening"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])

        # send message for personalized bot request.
        if select_menu.values[0] == "personalized_bot":
            # remove old message
            await processing_response(interaction)

            # Header over Bot message
            header = discord.Embed(colour=config.HEADER_COLOR)
            header.set_author(
                name="www.reelab.studio",
                url="https://reelab.studio/",
                icon_url="attachment://reelab_logo_white.png"
            )
            header.set_image(
                url="attachment://building_bot_whitebackground.png"
            )
            header_path = "./pictures/building_bot_whitebackground.png"
            header_file = discord.File(header_path, filename="building_bot_whitebackground.png")

            # Create Discord bot selection description
            description_personalized = discord.Embed(
                description=language["discord_order_personalized_bot_description"].format(plant_plant=plant_plant),
                color=config.EMBED_COLOR,
            )
            description_personalized.set_image(url="attachment://reelab_banner_blue.png")
            description_personalized.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await attachments()

            # creates a list of buttons to be sent
            buttons_personalized = [
                Button(
                    style=ButtonStyle.green,
                    emoji=log_membershipscreening,
                    label=language["discord_order_personalized_bot_lable"],
                    custom_id="personalized_bot_accept_tos",
                )
            ]

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header, description_personalized],
                                   attachments=[header_file, icon_file, footer_file],
                                   components=[buttons_personalized]
                                   )
            return

        # Getting user ID to fetch stored information
        user_id = interaction.author.id
        selected_value = select_menu.values[0]
        bot_type = bot_type_mapping.get(selected_value)

        # Storing bot type to the user ID
        if bot_type:
            user_info = user_data.get(user_id, {})
            user_info["bot_type"] = bot_type
            user_data[user_id] = user_info

        # remove old message
        await processing_response(interaction)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(
            url="attachment://config-step_1-5.png"
        )
        header_path = "./pictures/bot_config_steps/config-step_1-5.png"
        header_file = discord.File(header_path, filename="config-step_1-5.png")

        # Create Discord bot selection description
        description = discord.Embed(
            description=language["discord_order_bot_step_1_description"].format(community_developer=community_developer),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_1_lable"],
                custom_id="users:1",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_2_lable"],
                custom_id="users:2",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_3_lable"],
                custom_id="users:3",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_4_lable"],
                custom_id="users:4",
            )
        ]

        # Edit interaction with new embed and components
        await interaction.edit(embeds=[header, description],
                               attachments=[header_file, icon_file, footer_file],
                               components=[buttons]
                               )

    @commands.Cog.on_click('^users:(\d+)$')
    async def order_bot_part_2(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        user_amount_pricing = int(button.custom_id.split(":")[1])

        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        log_timeoutremoved = self.bot.get_emoji(config.EMOJIS["log_timeoutremoved"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])

        # Calculate the price based on the hosting duration and user ID
        price = calculate_price(user_amount_pricing, user.id)

        # Convert the price to a numeric value for further processing
        price_numeric = float(price.replace("€", "").replace(",", "."))

        # Format the price for single month hosting
        price_single_month = format_price(price_numeric)

        # Format the prices for multiple month hosting
        price_3_months = format_price(price_numeric * 3)
        price_6_months = format_price(price_numeric * 6)
        price_12_months = format_price(price_numeric * 12)

        # remove old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(
            url="attachment://config-step_2-5.png"
        )
        header_path = "./pictures/bot_config_steps/config-step_2-5.png"
        header_file = discord.File(header_path, filename="config-step_2-5.png")

        # Discord bot selection.
        description = discord.Embed(
            description=language["discord_order_bot_step_2_description"].format(community_developer=community_developer,
                                                                                log_memberjoin=log_memberjoin),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_1_lable"]} - {price_single_month}',
                custom_id="months:1",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_2_lable"]} - {price_3_months}',
                custom_id="months:3",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_3_lable"]} - {price_6_months}',
                custom_id="months:6",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_4_lable"]} - {price_12_months}',
                custom_id="months:12",
            )
        ]

        # Edit interaction with new embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^months:(\d+)$')
    async def order_bot_part_3(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        hosting_duration = int(button.custom_id.split(":")[1])

        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        function_tick = self.bot.get_emoji(config.EMOJIS["function_tick"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_data.get(user.id, {})

        # Update user information with the selected hosting duration
        user_info["hosting_duration"] = hosting_duration

        # Set default setup_fee
        setup_fees = 0

        # Define setup fees based on the selected hosting duration
        if hosting_duration == 1:
            setup_fees = config.setup_fee_1_month
        elif hosting_duration == 3:
            setup_fees = config.setup_fee_3_month
        elif hosting_duration == 6:
            setup_fees = config.setup_fee_6_month
        elif hosting_duration == 12:
            setup_fees = config.setup_fee_12_month

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_data.get(user.id, {})

        # Update user information with the selected hosting duration
        user_info["setup_fees"] = setup_fees

        # Remove old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(
            url="attachment://config-step_3-5.png"
        )
        header_path = "./pictures/bot_config_steps/config-step_3-5.png"
        header_file = discord.File(header_path, filename="config-step_3-5.png")

        # About Me Pack message
        description = discord.Embed(
            description=language["discord_order_bot_step_3_description"].format(community_developer=community_developer),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_thumbnail(url="attachment://about_me_pack.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load About Me Pack thumbnail
        about_me_pack_path = "./pictures/about_me_pack.png"
        about_me_pack_file = discord.File(about_me_pack_path, filename="about_me_pack.png")

        # Load other attachments
        banner_file, icon_file, footer_file = await attachments()

        # Creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.grey,
                emoji=function_tick,
                label=language["discord_order_bot_step_3_about_me_pack_1_lable"],
                custom_id="about_me_pack_yes",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=function_cross,
                label=language["discord_order_bot_step_3_about_me_pack_2_lable"],
                custom_id="about_me_pack_no",
            )
        ]

        # Edit interaction with new embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file, about_me_pack_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^about_me_pack_(yes|no)$')
    async def order_bot_part_4(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        about_me_pack = button.custom_id.split("_")[-1]

        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        community_owner = self.bot.get_emoji(config.EMOJIS["community_owner"])

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_data.get(user.id, {})

        # Update user information with the selected about me pack
        user_info["about_me_pack"] = about_me_pack

        # Update user data in the database
        user_data[user.id] = user_info

        # Remove the old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(
            url="attachment://config-step_4-5.png"
        )
        header_path = "./pictures/bot_config_steps/config-step_4-5.png"
        header_file = discord.File(header_path, filename="config-step_4-5.png")

        # Create the bot message
        description = discord.Embed(
            description=language["discord_order_bot_step_4_description"].format(community_developer=community_developer),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await attachments()

        # Creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.grey,
                emoji=community_owner,
                label=language["discord_order_bot_step_4_configure_lable"],
                custom_id="configure_bot",
            )
        ]

        # Edit the message with the updated embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click("^configure_bot$")
    async def order_bot_part_4_modal(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve user data if available, otherwise set default values
        user_info = user_data.get(user.id, {})
        bot_type = user_info.get('bot_type', 'Not entered')

        # Define the modal with input fields for bot name and status
        modal = Modal(
            title=language["discord_order_bot_step_4_configure_modal_title"],
            custom_id=f'bot_details',
            components=[
                [
                    TextInput(
                        label=language["discord_order_bot_step_4_configure_modal_name_lable"],
                        custom_id='bot_name',
                        placeholder=f"{bot_type}",
                        required=True,
                        style=1,
                        max_length=28,
                    ),
                    TextInput(
                        label=language["discord_order_bot_step_4_configure_modal_status_lable"],
                        custom_id='bot_status',
                        placeholder=language["discord_order_bot_step_4_configure_modal_status_placeholder"],
                        required=True,
                        style=1,
                        max_length=56,
                    )
                ]
            ]
        )

        # Respond to the interaction with the modal
        await ctx.respond_with_modal(modal)

    @commands.Cog.on_submit('^bot_details')
    async def order_bot_part_5(self, ctx: discord.ModalSubmitInteraction):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Retrieve emojis
        log_membershipscreening = self.bot.get_emoji(config.EMOJIS["log_membershipscreening"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])

        # Get bot name and status entered by the user
        bot_name = ctx.get_field('bot_name').value or None
        bot_status = ctx.get_field('bot_status').value or None

        # Update user data with bot name and status
        user_info = user_data.get(user.id, {})
        user_info["bot_name"] = bot_name
        user_info["bot_status"] = bot_status
        user_data[user.id] = user_info

        # Determine hosting duration ending
        hosting_duration_month = "month" if user_info.get('hosting_duration', 'Not entered') == 1 else "months"

        # Determine about me pack status and cost
        about_me_pack_status = 'Selected' if user_info.get('about_me_pack') == 'yes' else 'Not selected'
        about_me_pack_total_cost = 0.50 * int(user_info.get('hosting_duration', 1))
        about_me_pack_cost_text = f" (Cost: {format_price(about_me_pack_total_cost)})" if about_me_pack_status == 'Selected' else ""
        price_about_me_pack = about_me_pack_total_cost if about_me_pack_status == 'Selected' else 0

        # Determine setup_fees
        setup_fees = user_info.get('setup_fees', 0)
        if setup_fees == 0:
            setup_fees_formatted = "No fees"
        else:
            setup_fees_formatted = f"{setup_fees:.2f}€"

        # Calculate total price
        total_price = setup_fees + price_about_me_pack + (float(user_info.get('user_amount_pricing', '0').replace('€', '').replace(',', '.')) * int(user_info.get('hosting_duration', '1')))
        total_price_formatted = f"{total_price:.2f}€"

        # Get all user information for the further embed
        bot_type = user_info.get('bot_type', 'Not entered')
        bot_users = user_info.get('bot_users', 'Not entered')
        bot_user_pricing = user_info.get('user_amount_pricing', 'Not entered')
        bot_hosting_duration = user_info.get('hosting_duration', 'Not entered')

        # Remove old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(url="attachment://config-step_final.png")
        header_path = "./pictures/bot_config_steps/config-step_final.png"
        header_file = discord.File(header_path, filename="config-step_final.png")

        formatted_description = language["discord_order_bot_step_5_description"].format(
            community_developer=community_developer,
            bot_type=bot_type,
            bot_name=bot_name,
            bot_status=bot_status,
            bot_users=bot_users,
            about_me_pack_status=about_me_pack_status,
            about_me_pack_cost_text=about_me_pack_cost_text,
            setup_fees_formatted=setup_fees_formatted,
            bot_user_pricing=bot_user_pricing,
            bot_hosting_duration=bot_hosting_duration,
            hosting_duration_month=hosting_duration_month,
            total_price_formatted=total_price_formatted,
            plant_plant=plant_plant
        )

        # Discord bot selection.
        description = discord.Embed(
            description=formatted_description,
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file],
                       components=[[
                           Button(
                               style=ButtonStyle.green,
                               emoji=log_membershipscreening,
                               label=language["discord_order_bot_step_5_accept_rules_lable"],
                               custom_id="pre_made_bot_accept_tos",
                           )
                       ]]
                       )

    @commands.Cog.on_click("^pre_made_bot_accept_tos$")
    async def order_pre_made_bot_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Get user data
        user_info = user_data.get(user.id, {})

        # Load selected language
        language = load_language(user.id)

        # Get Order Product channel for thread creation
        channel = ctx.guild.get_channel(self.order_product_channel_id)

        # Get Official Staff role
        staff = ctx.guild.get_role(self.official_staff_id)

        # Retrieve emojis
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])
        promo = self.bot.get_emoji(config.EMOJIS["promo"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])

        # Determine hosting duration ending
        hosting_duration_month = "month" if user_info.get('hosting_duration', 'Not entered') == 1 else "months"

        # Determine setup_fees
        setup_fees = user_info.get('setup_fees', 0)
        if setup_fees == 0:
            setup_fees_formatted = "No fees"
        else:
            setup_fees_formatted = f"{setup_fees:.2f}€"

        # Determine about me pack status and cost
        about_me_pack_status = 'Selected' if user_info.get('about_me_pack') == 'yes' else 'Not selected'
        about_me_pack_total_cost = 0.50 * int(user_info.get('hosting_duration', 1))
        about_me_pack_cost_text = f" (Cost: {format_price(about_me_pack_total_cost)})" if about_me_pack_status == 'Selected' else ""
        price_about_me_pack = about_me_pack_total_cost if about_me_pack_status == 'Selected' else 0

        # Calculate total price
        total_price = setup_fees + price_about_me_pack + (float(user_info.get('user_amount_pricing', '0').replace('€', '').replace(',', '.')) * int(user_info.get('hosting_duration', '1')))
        total_price_formatted = f"{total_price:.2f}€"

        # Get all user information for the further embed
        bot_type = user_info.get('bot_type', 'Not entered')
        bot_name = user_info.get('bot_name', 'Not entered')
        bot_status = user_info.get('bot_status', 'Not entered')
        bot_users = user_info.get('bot_users', 'Not entered')
        bot_user_pricing = user_info.get('user_amount_pricing', 'Not entered')
        bot_hosting_duration = user_info.get('hosting_duration', 'Not entered')

        # Remove old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(url="attachment://reelab_banner_white.gif")

        # Header over thread message
        thread_header = discord.Embed(colour=config.HEADER_COLOR)
        thread_header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        thread_header.set_image(url="attachment://bot_server_working_whitebackground.png")

        # Format the bot description for embedding
        formatted_description = language["discord_order_bot_thread_message"].format(
            plant_plant=plant_plant,
            user=user.mention,
            bot_type=bot_type,
            bot_name=bot_name,
            bot_status=bot_status,
            bot_users=bot_users,
            about_me_pack_status=about_me_pack_status,
            about_me_pack_cost_text=about_me_pack_cost_text,
            setup_fees_formatted=setup_fees_formatted,
            bot_user_pricing=bot_user_pricing,
            bot_hosting_duration=bot_hosting_duration,
            hosting_duration_month=hosting_duration_month,
            total_price_formatted=total_price_formatted
        )

        # Load the current counting
        counting = load_counting()

        # Create a thread with a unique name based on the counting
        thread = await channel.create_thread(
            name=f"#{counting:04} | {user} | {bot_type}",
            reason=f"#{counting:04} | {user} | {bot_type}",
            private=True,
            invitable=True
        )

        # Increment and save the counting for future threads
        counting += 1
        save_counting(counting)

        # Send summary in thread.
        description = discord.Embed(
            description=formatted_description,
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()
        header_path = "./pictures/bot_server_working_whitebackground.png"
        header_file = discord.File(header_path, filename="bot_server_working_whitebackground.png")

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(language["discord_order_bot_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[thread_header, description],
                          files=[header_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.blurple,
                                  emoji=promo,
                                  label=language["discord_order_bot_thread_code_button"],
                                  custom_id="discord_bot_discount_code",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["discord_order_bot_thread_price_button"],
                                  custom_id="discord_bot_pricing_information",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=function_cross,
                                  label=language["discord_order_bot_thread_close_button"],
                                  custom_id="close_bot_order",
                              )
                          ]]
                          )
        # Send summary in thread.
        user_message = discord.Embed(
            description=language["discord_order_bot_user_message"].format(thread=thread.mention),
            color=config.EMBED_COLOR,
        )
        user_message.set_image(url="attachment://reelab_banner_blue.png")
        user_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header, user_message],
                       attachments=[banner_file, icon_file, footer_file],
                       )

        # Delete user data after processing
        del user_data[user.id]

    @commands.Cog.on_click("^personalized_bot_accept_tos$")
    async def order_personalized_bot_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Define user language and load language data
        user_info = user_data.get(user.id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/order_discord_bot_language_file.json"
        language = load_language_data(file_path, user_language)

        # Get Order Product channel for thread creation
        channel = ctx.guild.get_channel(self.order_product_channel_id)

        # Get Official Staff role
        staff = ctx.guild.get_role(self.official_staff_id)

        # Retrieve emojis
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])
        promo = self.bot.get_emoji(config.EMOJIS["promo"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])
        community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])

        # Load the current counting
        counting = load_counting()

        # Create a thread with a unique name based on the counting
        thread = await channel.create_thread(
            name=f"#{counting:04} | {user} | Personalized Bot",
            reason=f"#{counting:04} | {user} | Personalized Bot",
            private=True,
            invitable=True
        )

        # Increment and save the counting for future threads
        counting += 1
        save_counting(counting)

        # Remove old message
        await processing_response(ctx)

        # Header over Bot message
        header = discord.Embed(colour=config.HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(url="attachment://reelab_banner_white.gif")

        # Header over thread message
        thread_header = discord.Embed(colour=config.HEADER_COLOR)
        thread_header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        thread_header.set_image(url="attachment://bot_server_working_whitebackground.png")

        # Send summary in thread.
        description = discord.Embed(
            description=language["discord_order_bot_personalized_thread_message"].format(user=user.mention,
                                                                                         plant_plant=plant_plant,
                                                                                         community_advisor=community_advisor),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()
        header_path = "./pictures/bot_server_working_whitebackground.png"
        header_file = discord.File(header_path, filename="bot_server_working_whitebackground.png")

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(language["discord_order_bot_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[thread_header, description],
                          files=[header_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.blurple,
                                  emoji=promo,
                                  label=language["discord_order_bot_thread_code_button"],
                                  custom_id="discord_bot_discount_code",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["discord_order_bot_thread_price_button"],
                                  custom_id="discord_bot_pricing_information",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=function_cross,
                                  label=language["discord_order_bot_thread_close_button"],
                                  custom_id="close_bot_order",
                              )
                          ]]
                          )

        # Send summary in thread.
        user_message = discord.Embed(
            description=language["discord_order_bot_user_message"].format(thread=thread.mention),
            color=config.EMBED_COLOR,
        )
        user_message.set_image(url="attachment://reelab_banner_blue.png")
        user_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header, user_message],
                       attachments=[banner_file, icon_file, footer_file],
                       )

    @commands.Cog.on_click("^discord_bot_pricing_information$")
    async def order_bot_pricing_information(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Define user language and load language data
        user_info = user_data.get(user.id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/order_discord_bot_language_file.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
        community_admin = self.bot.get_emoji(config.EMOJIS["community_admin"])

        # Send pricing information in chat.
        response_message = discord.Embed(
            color=config.EMBED_COLOR,
            description=language["discord_order_bot_pricing_information"].format(plantbig_plant=plantbig_plant, log_memberjoin=log_memberjoin, community_admin=community_admin)
        )
        await ctx.respond(embed=response_message, hidden=True)

    @commands.Cog.on_click("^discord_bot_discount_code$")
    async def order_bot_discount_code(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Load selected language
        language = load_language(user.id)

        # Define the modal with input fields for bot name and status
        modal = Modal(
            title=language["discord_order_bot_discount_code_modal_title"],
            custom_id=f'bot_discount_code',
            components=[
                [
                    TextInput(
                        label=language["discord_order_bot_discount_code_modal_name_lable"],
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

    @commands.Cog.on_submit('^bot_discount_code$')
    async def order_bot_submit_discount_code(self, ctx: discord.ModalSubmitInteraction):
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
                    description=language["discord_order_bot_discount_code_valid_value_0"].format(promo=promo,
                                                                                                 code=code)
                )
                await ctx.respond(embed=discount_code_message, hidden=False)
            else:
                # Send a message indicating the value of the discount code
                discount_code_message = discord.Embed(
                    color=config.EMBED_COLOR,
                    description=language["discord_order_bot_discount_code_valid_value"].format(promo=promo,
                                                                                               code=code,
                                                                                               discount_value=discount_value)
                )
                await ctx.respond(embed=discount_code_message, hidden=False)

        else:
            # Send a message indicating that the code does not exist
            discount_code_message = discord.Embed(
                color=config.EMBED_COLOR,
                description=language["discord_order_bot_discount_code_not_valid"]
            )
            await ctx.respond(embed=discount_code_message, hidden=True)

    @commands.Cog.on_click("^close_bot_order$")
    async def order_bot_close_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

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
    reelab_bot.add_cog(BuyDiscordBot(reelab_bot))
