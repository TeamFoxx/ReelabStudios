# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Entwickelt von Foxx
# »› Copyright © 2024 Aurel Hoxha. Alle Rechte vorbehalten.
# »› GitHub: https://github.com/TeamFoxx
# »› Für Support und Anfragen kontaktieren Sie bitte hello@aurelhoxha.de
# »› Verwendung dieses Programms unterliegt den Bedingungen der MIT-Lizenz.
# »› Eine Kopie der Lizenz finden Sie in der Datei "LICENSE" im Hauptverzeichnis dieses Projekts.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { imports } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

from cogs import *

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

user_lang = {}

# emojis
EMOJIS = {
    "community_owner": 1217203408516284516,
    "community_admin": 1217203398802280631,
    "community_developer": 1217203400593117256,
    "community_advisor": 1217203395434385438,
    "community_member": 1217203405316030595,
    "community_eventhost": 1217203402237280488,
    "function_tick": 1217203424425152582,
    "function_cross": 1217203796065648691,
    "log_timeoutremoved": 1217203449654018128,
    "log_membershipscreening": 1217203998659055797,
    "log_memberjoin": 1217203966450860093,
    "plantbig_plant": 1217203467777474640,
    "plant_plant": 1217204087884611665
}

# embed-styles
EMBED_COLOR = 0x48689b
HEADER_COLOR = 0x2b2d31


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

class ProductPurchase(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    async def send_processing_response(self, interaction: discord.ComponentInteraction):
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

    async def header(self):
        """
        Creates and returns an embed for the header with the Reelab Studio information.
        """
        header = discord.Embed(colour=HEADER_COLOR)
        header.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )
        header.set_image(
            url="attachment://reelab_banner_white.gif"
        )
        return header

    async def attachments(self):
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

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="buy-a-product",
        description='Send the "buy a product" Message to this chat.',
        default_required_permissions=discord.Permissions(administrator=True)
    )
    async def buy_product(self, ctx):
        # Discord Emoji
        community_planner = self.bot.get_emoji(1217203741279653968)
        community_member = self.bot.get_emoji(1217203405316030595)
        community_eventhost = self.bot.get_emoji(1217203402237280488)
        plantbig_plant = self.bot.get_emoji(1217203467777474640)
        community_developer = self.bot.get_emoji(1217203400593117256)

        # Header of every Bot message
        header = discord.Embed(colour=0x2b2d31)
        header.set_author(name="The official Reelab Studio Discord Server", url="https://reelab.studio/",
                          icon_url="attachment://reelab_logo_white.png")
        header.set_image(url="attachment://reelab_banner_white.gif")

        banner_path = "./pictures/reelab_banner_white.gif"
        banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

        icon_path = "./pictures/reelab_logo_white.png"
        icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

        # Following message
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
            color=0x48689b,
        )
        buy_product_msg.set_author(name="www.reelab.studio", url="https://reelab.studio/")
        buy_product_msg.set_image(url="attachment://reelab_banner_blue.png")

        footer_path = "./pictures/reelab_banner_blue.png"
        footer_file = discord.File(footer_path, filename="reelab_banner_blue.png")

        await ctx.respond(embeds=[header, buy_product_msg],
                          files=[banner_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.green,
                                  emoji="🛍️",
                                  label="Order a Product",
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
                          ]]
                          )

    # Order product section.
    @commands.Cog.on_click('^order_product$')
    async def order_product(self, ctx: discord.ComponentInteraction, button):
        community_advisor = self.bot.get_emoji(1217203395434385438)
        community_member = self.bot.get_emoji(1217203405316030595)
        community_eventhost = self.bot.get_emoji(1217203402237280488)
        plantbig_plant = self.bot.get_emoji(1217203467777474640)

        buy_message = discord.Embed(
            colour=0x48689b,
            description=f"## {plantbig_plant} Turn dreams into reality!\n"
                        f"> We, the **Reelab Team**, are thrilled about your decision to purchase a product. "
                        f"Please select from the options below in the dropdown menu to proceed with your purchase or to access customer support."
        )

        buy_message.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )

        buy_message.set_image(
            url="attachment://reelab_banner_white.gif"
        )

        buy_message.set_footer(
            text="~ The official Reelab Studio Discord Bot"
        )

        banner_path = "./pictures/reelab_banner_white.gif"
        banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

        icon_path = "./pictures/reelab_logo_white.png"
        icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

        await ctx.respond(embed=buy_message,
                          hidden=True,
                          files=[banner_file, icon_file],
                          components=[[
                              SelectMenu(
                                  placeholder='Explore your options...',
                                  options=[
                                      SelectOption(
                                          label='Order Discord Bot',
                                          description="Enhance your server with a Discord bot.",
                                          emoji=community_member,
                                          value='order_discord_bot'
                                      ),
                                      SelectOption(
                                          label='Order Website',
                                          description="Establish your online presence with a sleek site.",
                                          emoji=community_member,
                                          value='order_website'
                                      ),
                                      SelectOption(
                                          label='Order Graphics',
                                          description="Enhance your brand with custom graphics.",
                                          emoji=community_member,
                                          value='order_graphics'
                                      ),
                                      SelectOption(
                                          label='Order Bundle',
                                          description="Unlock savings by bundling services.",
                                          emoji=community_eventhost,
                                          value='order_bundle'
                                      ),
                                      SelectOption(
                                          label='Get Customer Support',
                                          description="Get timely help from our support team.",
                                          emoji=community_advisor,
                                          value='customer_support'
                                      )
                                  ],
                                  custom_id='products',
                                  max_values=1
                              )]])

    @commands.Cog.on_click('^language_selection$')
    async def language_selection(self, ctx: discord.ComponentInteraction, button):
        plantbig_plant = self.bot.get_emoji(1217203467777474640)

        select_language_message = discord.Embed(
            colour=0x48689b,
            description=f"## {plantbig_plant} Select your preferred language for your purchase.\n"
                        f"> We, the **Reelab Team**, are thrilled about your decision to purchase a product. We offer multi-language shopping to ensure a better experience and to overcome language barriers."
        )

        select_language_message.set_author(
            name="www.reelab.studio",
            url="https://reelab.studio/",
            icon_url="attachment://reelab_logo_white.png"
        )

        select_language_message.set_image(
            url="attachment://reelab_banner_white.gif"
        )

        select_language_message.set_footer(
            text="~ The official Reelab Studio Discord Bot"
        )

        banner_path = "./pictures/reelab_banner_white.gif"
        banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

        icon_path = "./pictures/reelab_logo_white.png"
        icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

        await ctx.respond(embed=select_language_message,
                          hidden=True,
                          files=[banner_file, icon_file],
                          components=[[
                              SelectMenu(
                                  placeholder='Select your language...',
                                  options=[
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
                                      )
                                  ],
                                  custom_id='language_select_options',
                                  max_values=1
                              )]])

    @commands.Cog.on_select('^language_select_options$')
    async def language_selection_confirmed(self, interaction, select_menu):
        user_id = interaction.author.id

        # Log the selected bot type
        logging.info(f'{str(user_id)} - Selected Language to proceed purchase.')

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(EMOJIS["plantbig_plant"])
        community_advisor = self.bot.get_emoji(EMOJIS["community_advisor"])
        community_member = self.bot.get_emoji(EMOJIS["community_member"])
        community_eventhost = self.bot.get_emoji(EMOJIS["community_eventhost"])

        # Get the selected language from the interaction
        selected_language = select_menu.values[0]

        # Define user language based on the selected language
        if selected_language in ['DE', 'TR', 'FR', 'IT', 'JA', 'ZH']:
            user_language = selected_language.lower()
        else:
            user_language = 'en'

        print(user_language)

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_lang.get(user_id, {})

        # Update user information with the selected hosting duration
        user_info["language"] = user_language

        # Update user data in the database
        user_lang[user_id] = user_info

        user_language = user_info.get('language', 'en')
        print(user_language)

        # Load language data
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        buy_message = discord.Embed(
            colour=EMBED_COLOR,
            description=language["language_selection_description"].format(plantbig_plant=plantbig_plant)
        )
        buy_message.set_author(name="www.reelab.studio", url="https://reelab.studio/",
                               icon_url="attachment://reelab_logo_white.png")
        buy_message.set_image(url="attachment://reelab_banner_white.gif")
        buy_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await self.attachments()

        # Add options to the select menu
        select_options = [
            SelectOption(
                label=language["language_selection_order_bot_lable"],
                description=language["language_selection_order_bot_description"],
                emoji=community_member,
                value='order_discord_bot'
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
