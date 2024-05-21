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
from main import reelab
from utils.utils import attachments, processing_response, load_language_data_discord_bot

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

counting_file_path = "data/counting.json"


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def calculate_price(user_amount_pricing: int) -> dict:
    """
    Calculates the price based on the user's amount pricing and updates user data accordingly.
    Returns the calculated price as a string.
    """
    amount = {1: "> 1k", 2: "1k-2.5k", 3: "2.5k-5k", 4: "< 5k"}
    price = {1: config.discord_bot_user_based_pricing_1, 2: config.discord_bot_user_based_pricing_2,
             3: config.discord_bot_user_based_pricing_3, 4: config.discord_bot_user_based_pricing_4}
    return {"bot_users": amount.get(user_amount_pricing, "Unknown"),
            "user_amount_pricing": price.get(user_amount_pricing, 0)}


def format_price(price):
    """
    Formats the given price to display as a string with Euro symbol.
    Returns the formatted price string.
    """
    if isinstance(price, int) or price.is_integer():
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
        selected = select_menu.values[0].split(":")

        # Check if the selected value of the select menu is "order_discord_bot"
        if selected[0] == "order_discord_bot":
            order_id = selected[1]
            order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

            # Load language data based on the user's language preference
            language = load_language_data_discord_bot(order.user_language)

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
            header_path = "./data/pictures/choose_your_bot_type_white.png"
            header_file = discord.File(header_path, filename="choose_your_bot_type_white.png")

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["discord_bot_products_description"].format(plantbig_plant=plantbig_plant,
                                                                                community_admin=community_admin),
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
                custom_id=f'select_bot_options:{order_id}',
                max_values=1
            )

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header, description],
                                   attachments=[header_file, icon_file, footer_file],
                                   components=[[bot_select_menu]])

    @commands.Cog.on_select('^select_bot_options:(.*)$')
    async def order_bot_step_1(self, interaction, select_menu):
        order_id = select_menu.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        bot_type_mapping = {
            "modmail_bot": "Modmail Bot",
            "music_bot": "Music Bot",
            "admin_bot": "Admin Bot",
            "tempvoice_bot": "TempVoice Bot",
            "studies_bot": "Studies Bot"
        }

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
            header_path = "./data/pictures/building_bot_whitebackground.png"
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
                    custom_id=f"personalized_bot_accept_tos:{order_id}",
                )
            ]

            # Edit interaction with new embed and components
            return await interaction.edit(embeds=[header, description_personalized],
                                          attachments=[header_file, icon_file, footer_file],
                                          components=[buttons_personalized]
                                          )

        # Getting user ID to fetch stored information
        selected_value = select_menu.values[0]
        bot_type = bot_type_mapping.get(selected_value)

        order.products["discord_bot"] = {
            "type": bot_type,  # Type of the bot, e.g., "Studies Bot"
            "bot_users": 0,  # Number of bot users, e.g., "> 1k"
            "user_amount_pricing": 0,  # Pricing per user
            "setup_fees": 0,  # Setup fee
            "hosting_duration": 0,  # Hosting duration in months
            "about_me_pack": None,  # Whether an 'About Me' pack is included
            "bot_name": "",  # Name of the bot
            "bot_status": "",  # Status of the bot
            "total_price": 0,  # Total price
            "start_date": "Awaiting Payment",  # Start date, initially as "Awaiting Payment" or a specific date
            "expire_date": "Pending Activation"  # Expiry date
        }

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
        header_path = "./data/pictures/bot_config_steps/config-step_1-5.png"
        header_file = discord.File(header_path, filename="config-step_1-5.png")

        # Create Discord bot selection description
        description = discord.Embed(
            description=language["discord_order_bot_step_1_description"].format(
                community_developer=community_developer),
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
                custom_id=f"users:1:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_2_lable"],
                custom_id=f"users:2:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_3_lable"],
                custom_id=f"users:3:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=community_advisor,
                label=language["discord_order_bot_step_1_user_amount_4_lable"],
                custom_id=f"users:4:{order_id}",
            )
        ]

        # Edit interaction with new embed and components
        await interaction.edit(embeds=[header, description],
                               attachments=[header_file, icon_file, footer_file],
                               components=[buttons]
                               )

    @commands.Cog.on_click('^users:(.*)$')
    async def order_bot_part_2(self, ctx: discord.ComponentInteraction, button):
        order_id = button.custom_id.split(":")[2]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Extract the selection made by the user from the button's custom ID
        user_amount_pricing = int(button.custom_id.split(":")[1])

        # Retrieve emojis
        log_timeoutremoved = self.bot.get_emoji(config.EMOJIS["log_timeoutremoved"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])

        # Calculate the price based on the hosting duration and user ID
        price_details = calculate_price(user_amount_pricing)

        # Convert the price to a numeric value for further processing
        user_amount_pricing = price_details.get("user_amount_pricing")
        bot_users = price_details.get("bot_users")

        order.products["discord_bot"]["bot_users"] = bot_users
        order.products["discord_bot"]["user_amount_pricing"] = user_amount_pricing

        # Format the price for single month hosting
        price_single_month = format_price(user_amount_pricing)

        # Format the prices for multiple month hosting
        price_3_months = format_price(user_amount_pricing * 3)
        price_6_months = format_price(user_amount_pricing * 6)
        price_12_months = format_price(user_amount_pricing * 12)

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
        header_path = "./data/pictures/bot_config_steps/config-step_2-5.png"
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
                custom_id=f"months:1:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_2_lable"]} - {price_3_months}',
                custom_id=f"months:3:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_3_lable"]} - {price_6_months}',
                custom_id=f"months:6:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=log_timeoutremoved,
                label=f'{language["discord_order_bot_step_2_hosting_duration_4_lable"]} - {price_12_months}',
                custom_id=f"months:12:{order_id}",
            )
        ]

        # Edit interaction with new embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^months:(.*)$')
    async def order_bot_part_3(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        hosting_duration = int(button.custom_id.split(":")[1])

        order_id = button.custom_id.split(":")[2]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Retrieve emojis
        function_tick = self.bot.get_emoji(config.EMOJIS["function_tick"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])

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

        # Update user information with the selected hosting duration
        order.products["discord_bot"]["hosting_duration"] = hosting_duration
        order.products["discord_bot"]["setup_fees"] = setup_fees

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
        header_path = "./data/pictures/bot_config_steps/config-step_3-5.png"
        header_file = discord.File(header_path, filename="config-step_3-5.png")

        # About Me Pack message
        description = discord.Embed(
            description=language["discord_order_bot_step_3_description"].format(
                community_developer=community_developer),
            color=config.EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_thumbnail(url="attachment://about_me_pack.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load About Me Pack thumbnail
        about_me_pack_path = "./data/pictures/about_me_pack.png"
        about_me_pack_file = discord.File(about_me_pack_path, filename="about_me_pack.png")

        # Load other attachments
        banner_file, icon_file, footer_file = await attachments()

        # Creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.grey,
                emoji=function_tick,
                label=language["discord_order_bot_step_3_about_me_pack_1_lable"],
                custom_id=f"about_me_pack:yes:{order_id}",
            ),
            Button(
                style=ButtonStyle.grey,
                emoji=function_cross,
                label=language["discord_order_bot_step_3_about_me_pack_2_lable"],
                custom_id=f"about_me_pack:no:{order_id}",
            )
        ]

        # Edit interaction with new embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file, about_me_pack_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^about_me_pack:(.*)$')
    async def order_bot_part_4(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        about_me_pack = button.custom_id.split(":")[1]

        order_id = button.custom_id.split(":")[2]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Retrieve emojis
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        community_owner = self.bot.get_emoji(config.EMOJIS["community_owner"])

        # Update user information with the selected hosting duration
        order.products["discord_bot"]["about_me_pack"] = about_me_pack

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
        header_path = "./data/pictures/bot_config_steps/config-step_4-5.png"
        header_file = discord.File(header_path, filename="config-step_4-5.png")

        # Create the bot message
        description = discord.Embed(
            description=language["discord_order_bot_step_4_description"].format(
                community_developer=community_developer),
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
                custom_id=f"configure_bot:{order_id}",
            )
        ]

        # Edit the message with the updated embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[header_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click("^configure_bot:(.*)$")
    async def order_bot_part_4_modal(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        order_id = button.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Retrieve user data if available, otherwise set default values
        bot_type = order.products.get('discord_bot').get('type')

        # Define the modal with input fields for bot name and status
        modal = Modal(
            title=language["discord_order_bot_step_4_configure_modal_title"],
            custom_id=f'bot_details:{order_id}',
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

    @commands.Cog.on_submit('^bot_details:(.*)$')
    async def order_bot_part_5(self, ctx: discord.ModalSubmitInteraction):
        # Extract the selection made by the user from the button's custom ID
        order_id = ctx.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Retrieve emojis
        log_membershipscreening = self.bot.get_emoji(config.EMOJIS["log_membershipscreening"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])

        # Get bot name and status entered by the user
        bot_name = ctx.get_field('bot_name').value or None
        bot_status = ctx.get_field('bot_status').value or None

        # Update user information
        order.products["discord_bot"]["bot_name"] = bot_name
        order.products["discord_bot"]["bot_status"] = bot_status

        # Get Order details for further respond.
        hosting_duration = order.products.get('discord_bot').get('hosting_duration')
        about_me_pack = order.products.get('discord_bot').get('about_me_pack')
        setup_fees = order.products.get('discord_bot').get('setup_fees')
        user_amount_pricing = order.products.get('discord_bot').get('user_amount_pricing')
        bot_type = order.products.get('discord_bot').get('type')
        bot_users = order.products.get('discord_bot').get('bot_users')

        # Determine hosting duration ending
        hosting_duration_month = "month" if hosting_duration == 1 else "months"

        # Determine about me pack status and cost
        about_me_pack_status = 'Selected' if about_me_pack == 'yes' else 'Not selected'
        about_me_pack_total_cost = 0.50 * int(hosting_duration)
        about_me_pack_cost_text = f" (Cost: {format_price(about_me_pack_total_cost)})" if about_me_pack_status == 'Selected' else ""
        price_about_me_pack = about_me_pack_total_cost if about_me_pack_status == 'Selected' else 0

        # Determine setup_fees
        setup_fees = setup_fees
        if setup_fees == 0:
            setup_fees_formatted = "No fees"
        else:
            setup_fees_formatted = f"{setup_fees:.2f}€"

        # format user_amount_pricing
        user_amount_pricing_formatted = f"{user_amount_pricing:.2f}€"

        # Calculate total price
        total_price = setup_fees + price_about_me_pack + (user_amount_pricing * int(hosting_duration))
        total_price_formatted = f"{total_price:.2f}€"

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
        header_path = "./data/pictures/bot_config_steps/config-step_final.png"
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
            bot_user_pricing=user_amount_pricing_formatted,
            bot_hosting_duration=hosting_duration,
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
                               custom_id=f"pre_made_bot_accept_tos:{order_id}",
                           )
                       ]]
                       )

    @commands.Cog.on_click("^pre_made_bot_accept_tos:(.*)$")
    async def order_pre_made_bot_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        order_id = button.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Change order status
        order.status = "Pending Payment"

        # Get user
        user = ctx.author

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Get Order Product channel for thread creation and Staff role
        channel = ctx.guild.get_channel(self.order_product_channel_id)
        staff = ctx.guild.get_role(self.official_staff_id)

        # Retrieve emojis
        plant_plant = self.bot.get_emoji(config.EMOJIS["plant_plant"])
        promo = self.bot.get_emoji(config.EMOJIS["promo"])
        function_cross = self.bot.get_emoji(config.EMOJIS["function_cross"])

        # Get Order details for further respond.
        hosting_duration = order.products.get('discord_bot').get('hosting_duration')
        about_me_pack = order.products.get('discord_bot').get('about_me_pack')
        setup_fees = order.products.get('discord_bot').get('setup_fees')
        user_amount_pricing = order.products.get('discord_bot').get('user_amount_pricing')
        bot_type = order.products.get('discord_bot').get('type')
        bot_name = order.products.get('discord_bot').get('bot_name')
        bot_status = order.products.get('discord_bot').get('bot_status')
        bot_users = order.products.get('discord_bot').get('bot_users')

        # Determine hosting duration ending
        hosting_duration_month = "month" if hosting_duration == 1 else "months"

        # Determine setup_fees
        setup_fees = setup_fees
        if setup_fees == 0:
            setup_fees_formatted = "No fees"
        else:
            setup_fees_formatted = f"{setup_fees:.2f}€"

        # format user_amount_pricing
        user_amount_pricing_formatted = f"{user_amount_pricing:.2f}€"

        # Determine about me pack status and cost
        about_me_pack_status = 'Selected' if about_me_pack == 'yes' else 'Not selected'
        about_me_pack_total_cost = 0.50 * int(hosting_duration)
        about_me_pack_cost_text = f" (Cost: {format_price(about_me_pack_total_cost)})" if about_me_pack_status == 'Selected' else ""
        price_about_me_pack = about_me_pack_total_cost if about_me_pack_status == 'Selected' else 0

        # Calculate total price
        total_price = setup_fees + price_about_me_pack + (user_amount_pricing * int(hosting_duration))
        total_price_formatted = f"{total_price:.2f}€"

        # Update user information
        order.products["discord_bot"]["total_price"] = total_price

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
            bot_user_pricing=user_amount_pricing_formatted,
            bot_hosting_duration=hosting_duration,
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
        header_path = "./data/pictures/bot_server_working_whitebackground.png"
        header_file = discord.File(header_path, filename="bot_server_working_whitebackground.png")

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(
            language["discord_order_bot_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[thread_header, description],
                          files=[header_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.blurple,
                                  emoji=promo,
                                  label=language["discord_order_bot_thread_code_button"],
                                  custom_id=f"discord_bot_discount_code:{order_id}",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["discord_order_bot_thread_price_button"],
                                  custom_id=f"discord_bot_pricing_information:{order_id}",
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

        # Load Order into json file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"
        with open(file_path, 'r+', encoding='utf-8') as file:
            # Read the existing data
            filedata = json.load(file)

            # Update the data
            filedata[order.order_id] = order.__dict__

            # Reset file position to the beginning
            file.seek(0)

            # Write the modified data
            json.dump(filedata, file)

            # Truncate the file to the new size
            file.truncate()

    @commands.Cog.on_click("^personalized_bot_accept_tos:(.*)$")
    async def order_personalized_bot_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        order_id = button.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Add bot type to order
        order.products["discord_bot"] = {
            "type": 'Personalized Bot',
        }
        order.status = "Pending Payment"

        # Get user
        user = ctx.author

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Get Order Product channel and Staff role
        channel = ctx.guild.get_channel(self.order_product_channel_id)
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
        header_path = "./data/pictures/bot_server_working_whitebackground.png"
        header_file = discord.File(header_path, filename="bot_server_working_whitebackground.png")

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(
            language["discord_order_bot_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[thread_header, description],
                          files=[header_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.blurple,
                                  emoji=promo,
                                  label=language["discord_order_bot_thread_code_button"],
                                  custom_id=f"discord_bot_discount_code:{order_id}",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["discord_order_bot_thread_price_button"],
                                  custom_id=f"discord_bot_pricing_information:{order_id}",
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

        # Load Order into json file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"
        with open(file_path, 'r+', encoding='utf-8') as file:
            # Read the existing data
            filedata = json.load(file)

            # Update the data
            filedata[order.order_id] = order.__dict__

            # Reset file position to the beginning
            file.seek(0)

            # Write the modified data
            json.dump(filedata, file)

            # Truncate the file to the new size
            file.truncate()

    @commands.Cog.on_click("^discord_bot_pricing_information:(.*)$")
    async def order_bot_pricing_information(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        order_id = button.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
        community_admin = self.bot.get_emoji(config.EMOJIS["community_admin"])

        # Send pricing information in chat.
        response_message = discord.Embed(
            color=config.EMBED_COLOR,
            description=language["discord_order_bot_pricing_information"].format(plantbig_plant=plantbig_plant,
                                                                                 log_memberjoin=log_memberjoin,
                                                                                 community_admin=community_admin)
        )
        await ctx.respond(embed=response_message, hidden=True)

    @commands.Cog.on_click("^discord_bot_discount_code:(.*)$")
    async def order_bot_discount_code(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        order_id = button.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

        # Define the modal with input fields for bot name and status
        modal = Modal(
            title=language["discord_order_bot_discount_code_modal_title"],
            custom_id=f'bot_discount_code:{order_id}',
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

    @commands.Cog.on_submit('^bot_discount_code:(.*)$')
    async def order_bot_submit_discount_code(self, ctx: discord.ModalSubmitInteraction):
        # Extract the selection made by the user from the button's custom ID
        order_id = ctx.custom_id.split(":")[1]
        order = list(filter(lambda o: o.order_id == order_id, reelab.orders))[0]

        # Load selected language
        language = load_language_data_discord_bot(order.user_language)

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


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(BuyDiscordBot(reelab_bot))
