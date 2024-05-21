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
from discord import Button, ButtonStyle, SelectOption, SelectMenu
from discord.ext import commands

import config
from main import reelab
from utils.orders import Order
from utils.utils import header, attachments


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def load_language_data_discord_bot(file_path: Path, user_language: str) -> dict:
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

class ProductPurchase(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="order-a-product",
        description='Send the "buy a product" Message to this chat.',
        default_required_permissions=discord.Permissions(administrator=True)
    )
    async def buy_product(self, ctx):
        # Retrieve emojis
        community_planner = self.bot.get_emoji(config.EMOJIS["community_planner"])
        community_member = self.bot.get_emoji(config.EMOJIS["community_member"])
        community_eventhost = self.bot.get_emoji(config.EMOJIS["community_eventhost"])
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])
        community_developer = self.bot.get_emoji(config.EMOJIS["community_developer"])

        # Create header
        header_embed = await header()

        # Embedded message to be sent
        buy_product_msg = discord.Embed(
            description=f"# {plantbig_plant} Transforming Ideas into Digital Reality\n"
                        f"> Whether it's for branding or community building, our services are tailored to transform your ideas into digital reality. **Explore our offerings below.**\n\n"
                        f"⏤\n"
                        f"## Our most popular products\n"
                        f"**{community_member} __Discord Bots__**\n"
                        f"- ModMail Bot\n"
                        f"- 24/7 Music Bot\n"
                        f"- Administration Bot\n"
                        f"- TempVoice Bot\n"
                        f"- Work & Studies Bot\n\n"
                        f"**{community_eventhost} __Static Websites__**\n"
                        f"- Minecraft website\n"
                        f"- Community website\n\n"
                        f"⏤\n"
                        f"## Prefer something more individual?\n"
                        f" **{community_developer} __Personalised products__**\n"
                        f"- Discord Bot\n"
                        f"- Websites\n"
                        f"- Graphics (Logo, Banner, etc.)\n"
                        f"- Hosting of your product\n\n"
                        f"⏤\n"
                        f"## {community_planner} Bundle & Sales\n"
                        f"> **Interested in bundling services for extra savings?** Explore our dedicated <#1217192999549800640> Channel for exclusive offers!\n"
                        f"- Don't miss out on these amazing deals! Grab yours now and elevate your community. :rocket:\n\n"
                        f"⏤\n"
                        f"- :shopping_cart: **Ready to purchase?** Just klick the button below.\n"
                        f"- Need assistance or have questions? Feel free to ask our staff members in the server!\n\n"
                        f"**Note:** Our current payment methods include PayPal, credit/debit card, Discord Nitro boosts, and promotional offers.",
            color=config.EMBED_COLOR,
        )
        buy_product_msg.set_image(url="attachment://reelab_banner_blue.png")

        # Creates a list of buttons to be sent
        buttons = [
            Button(
                style=ButtonStyle.green,
                emoji="🛍️",
                label="Explore all Products",
                custom_id="order_product",
                disabled=False
            ),
            Button(
                style=ButtonStyle.grey,
                emoji="🌍",
                label="Purchase in Your Language",
                custom_id="language_selection",
                disabled=False
            )
        ]

        # Load attachments
        banner_file, icon_file, footer_file = await attachments()

        # Edit interaction with new embed and components
        await ctx.respond(embeds=[header_embed, buy_product_msg],
                          files=[banner_file, icon_file, footer_file],
                          components=[buttons])

    # Order product section.
    @commands.Cog.on_click('^order_product$')
    async def order_product(self, ctx: discord.ComponentInteraction, button):
        # Create order
        order = Order(user_id=ctx.author.id, user_name=ctx.author.name, status="Configuration Pending")
        reelab.orders.append(order)

        # Retrieve emojis
        community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])
        community_member = self.bot.get_emoji(config.EMOJIS["community_member"])
        community_eventhost = self.bot.get_emoji(config.EMOJIS["community_eventhost"])
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])

        # Embedded message to be sent
        buy_message = discord.Embed(
            colour=config.EMBED_COLOR,
            description=f"## {plantbig_plant} Turn dreams into reality!\n"
                        f"> We, the **Reelab Team**, are thrilled about your decision to purchase a product. "
                        f"Please select from the options below in the dropdown menu to proceed with your purchase or to access customer support."
        )

        buy_message.set_author(name="www.reelab.studio", url="https://reelab.studio/",
                               icon_url="attachment://reelab_logo_white.png")
        buy_message.set_image(url="attachment://reelab_banner_white.gif")
        buy_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await attachments()

        # Add options to the select menu
        select_options = [
            SelectOption(
                label='Order Discord Bot',
                description="Enhance your server with a Discord bot.",
                emoji=community_member,
                value=f'order_discord_bot:{order.order_id}'
            ),
            SelectOption(
                label='Order Website',
                description="Establish your online presence with a sleek site.",
                emoji=community_member,
                value=f'order_website:{order.order_id}'
            ),
            SelectOption(
                label='Order Graphics',
                description="Enhance your brand with custom graphics.",
                emoji=community_member,
                value=f'order_graphics:{order.order_id}'
            ),
            SelectOption(
                label='Order Bundle',
                description="Unlock savings by bundling services.",
                emoji=community_eventhost,
                value=f'order_bundle:{order.order_id}'
            ),
            SelectOption(
                label='Get Customer Support',
                description="Get timely help from our support team.",
                emoji=community_advisor,
                value=f'customer_support:{order.order_id}'
            )
        ]

        # Create select menu
        select_menu = SelectMenu(
            placeholder='Explore your options...',
            options=select_options,
            custom_id='products',
            max_values=1
        )

        # Edit interaction with new embed and components
        await ctx.respond(embed=buy_message,
                          hidden=True,
                          files=[banner_file, icon_file],
                          components=[[select_menu]])

    @commands.Cog.on_click('^language_selection$')
    async def language_selection(self, ctx: discord.ComponentInteraction, button):
        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])

        # Embedded message to be sent
        select_language_message = discord.Embed(
            colour=config.EMBED_COLOR,
            description=f"## {plantbig_plant} Select your preferred language for your purchase.\n"
                        f"> We, the **Reelab Team**, are thrilled about your decision to purchase a product. "
                        f"We offer multi-language shopping to ensure a better experience and to overcome language barriers."
        )

        select_language_message.set_author(name="www.reelab.studio", url="https://reelab.studio/",
                                           icon_url="attachment://reelab_logo_white.png")
        select_language_message.set_image(url="attachment://reelab_banner_white.gif")
        select_language_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await attachments()

        # Add options to the select menu
        select_options = [
            SelectOption(
                label='Deutsch',
                description="Wenn du deutsch bist , ist dies die Sprache, die du verwendest.",
                emoji='🇩🇪',
                value='DE'
            ),
            SelectOption(
                label='Türkçe',
                description="Eğer Türkçe konuşuyorsanız, bu dili seçmelisiniz.",
                emoji='🇹🇷',
                value='TR'
            ),
            SelectOption(
                label='Français',
                description="Si vous parlez français, c'est la langue que vous souhaitez utiliser.",
                emoji='🇫🇷',
                value='FR'
            ),
            SelectOption(
                label='Italiano',
                description="Se parli italiano, questa è la lingua che desideri utilizzare.",
                emoji='🇮🇹',
                value='IT'
            ),
            SelectOption(
                label='日本語',
                description="日本語を話す方は、この言語を選択してください。",
                emoji='🇯🇵',
                value='JA'
            ),
            SelectOption(
                label='中文',
                description="如果您会说中文，这就是您想要使用的语言。",
                emoji='🇨🇳',
                value='ZH'
            ),
            SelectOption(
                label='한국어',
                description="한국어를 구사하는 경우 이 언어를 선택하세요.",
                emoji='🇰🇷',
                value='KO'
            )
        ]

        # Create select menu
        select_menu = SelectMenu(
            placeholder='Select your language...',
            options=select_options,
            custom_id='language_select_options',
            max_values=1
        )

        # Edit interaction with new embed and components
        await ctx.respond(embed=select_language_message,
                          hidden=True,
                          files=[banner_file, icon_file],
                          components=[[select_menu]])

    @commands.Cog.on_select('^language_select_options$')
    async def language_selection_confirmed(self, interaction, select_menu):
        user = interaction.author

        # Log the selected bot type
        logging.info(f'{str(user.id)} - Selected Language to proceed purchase.')

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(config.EMOJIS["plantbig_plant"])
        community_advisor = self.bot.get_emoji(config.EMOJIS["community_advisor"])
        community_member = self.bot.get_emoji(config.EMOJIS["community_member"])
        community_eventhost = self.bot.get_emoji(config.EMOJIS["community_eventhost"])

        # Get the selected language from the interaction
        selected_language = select_menu.values[0]

        # Define user language based on the selected language
        if selected_language in ['DE', 'TR', 'FR', 'IT', 'JA', 'ZH', 'KO']:
            user_language = selected_language.lower()
        else:
            user_language = 'en'

        # Create order with selected user language
        order = Order(user_id=user.id, user_name=user.name, user_language=user_language)
        reelab.orders.append(order)

        # Load language data
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/languages/products_language_file.json"
        language = load_language_data_discord_bot(file_path, user_language)

        # Embedded message to be sent
        buy_message = discord.Embed(
            colour=config.EMBED_COLOR,
            description=language["language_selection_description"].format(plantbig_plant=plantbig_plant)
        )
        buy_message.set_author(name="www.reelab.studio", url="https://reelab.studio/",
                               icon_url="attachment://reelab_logo_white.png")
        buy_message.set_image(url="attachment://reelab_banner_white.gif")
        buy_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await attachments()

        # Add options to the select menu
        select_options = [
            SelectOption(
                label=language["language_selection_order_bot_lable"],
                description=language["language_selection_order_bot_description"],
                emoji=community_member,
                value=f'order_discord_bot:{order.order_id}'
            ),
            SelectOption(
                label=language["language_selection_order_website_lable"],
                description=language["language_selection_order_website_description"],
                emoji=community_member,
                value='order_website'
            ),
            SelectOption(
                label=language["language_selection_order_graphic_lable"],
                description=language["language_selection_order_graphic_description"],
                emoji=community_member,
                value='order_graphics'
            ),
            SelectOption(
                label=language["language_selection_order_bundle_lable"],
                description=language["language_selection_order_bundle_description"],
                emoji=community_eventhost,
                value='order_bundle'
            ),
            SelectOption(
                label=language["language_selection_customer_support_lable"],
                description=language["language_selection_customer_support_description"],
                emoji=community_advisor,
                value='customer_support'
            )
        ]

        # Add the select menu
        bot_select_menu = SelectMenu(
            placeholder=language["language_selection_options_placeholder"],
            options=select_options,
            custom_id='products',
            max_values=1
        )

        # Edit interaction with new embed and components
        await interaction.edit(embed=buy_message,
                               attachments=[banner_file, icon_file],
                               components=[[bot_select_menu]])


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(ProductPurchase(reelab_bot))
