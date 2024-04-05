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
user_data = {}

# emojis
EMOJIS = {
    "community_developer": 1217203400593117256,
    "community_admin": 1217203398802280631,
    "community_advisor": 1217203395434385438,
    "plantbig_plant": 1217203467777474640,
    "log_timeoutremoved": 1217203449654018128,
    "function_tick": 1217203424425152582,
    "function_cross": 1217203796065648691,
    "community_owner": 1217203408516284516,
    "log_membershipscreening": 1217203998659055797,
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


def calculate_price(user_amount_pricing: int, user_id: int) -> str:
    """
    Calculates the price based on the user's amount pricing and updates user data accordingly.
    Returns the calculated price as a string.
    """
    user_info = user_data.get(user_id, {})
    if user_amount_pricing == 1:
        price = "1.50€"  # Standard price for less than 1000 users
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "> 1k"
    elif user_amount_pricing == 2:
        price = "2.00€"  # Price for 1000-2499 users
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "1k-2.5k"
    elif user_amount_pricing == 3:
        price = "2.50€"  # Price for 2500-4999 users
        user_info["user_amount_pricing"] = price
        user_info["bot_users"] = "2.5k-5k"
    elif user_amount_pricing == 4:
        price = "3.00€"  # Price for 5000 or more users
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
        return f"{int(price)}€"  # Check if the price is an integer or a float with two decimal places
    else:
        return f"{price:.2f}€"


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BuyDiscordBot(commands.Cog):
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

    @commands.Cog.on_select('^language_select_options$')
    async def language_selection(self, interaction, select_menu):
        user_id = interaction.author.id
        logging.info(f'{str(user_id)} - Selected Language to proceed purchase.')

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(EMOJIS["plantbig_plant"])
        community_advisor = self.bot.get_emoji(1217203395434385438)
        community_member = self.bot.get_emoji(1217203405316030595)
        community_eventhost = self.bot.get_emoji(1217203402237280488)

        # Get the selected language from the interaction
        selected_language = select_menu.values[0]

        # Define user language based on the selected language
        if selected_language == 'DE':
            user_language = 'de'
        elif selected_language == 'TR':
            user_language = 'tr'
        elif selected_language == 'FR':
            user_language = 'fr'
        elif selected_language == 'IT':
            user_language = 'it'
        elif selected_language == 'JA':
            user_language = 'ja'
        elif selected_language == 'ZH':
            user_language = 'zh'
        else:
            user_language = 'en'

        # Store user_language to user_data
        user_info = user_data.get(user_id, {})
        user_info["user_language"] = user_language
        user_data[user_id] = user_info

        # Load language data
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        buy_message = discord.Embed(
            colour=EMBED_COLOR,
            description=language["language_selection_description"].format(plantbig_plant=plantbig_plant)
        )
        buy_message.set_author(name="www.reelab.studio", url="https://reelab.studio/", icon_url="attachment://reelab_logo_white.png")
        buy_message.set_image(url="attachment://reelab_banner_white.gif")
        buy_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await self.attachments()

        await interaction.edit(embed=buy_message,
                              attachments=[banner_file, icon_file],
                              components=[[
                                  SelectMenu(
                                      placeholder=language["language_selection_options_placeholder"],
                                      options=[
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
                                      ],
                                      custom_id='products',
                                      max_values=1
                                  )]])

    @commands.Cog.on_select('^products$')
    async def discord_bot_products(self, interaction, select_menu):
        user_id = interaction.author.id
        logging.info(f'{str(user_id)} - Select Discord bot function called.')

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        community_developer = self.bot.get_emoji(EMOJIS["community_developer"])
        community_admin = self.bot.get_emoji(EMOJIS["community_admin"])
        plantbig_plant = self.bot.get_emoji(EMOJIS["plantbig_plant"])

        # Check if the selected value of the select menu is "order_discord_bot"
        if select_menu.values[0] == "order_discord_bot":

            # Remove old message
            await self.send_processing_response(interaction)

            # Create header
            header = await self.header()

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["discord_bot_products_description"].format(plantbig_plant=plantbig_plant, community_admin=community_admin),
                color=EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Load attachments
            banner_file, icon_file, footer_file = await self.attachments()

            # Add options to the select menu
            select_options = [
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

            # Create the "I want a personalized bot" button
            personalized_bot_button = Button(
                style=ButtonStyle.green,
                emoji="🚀",
                label=language["discord_personalized_bot_label"],
                custom_id="personalized_bot",
                disabled=False
            )

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header, description],
                                   attachments=[banner_file, icon_file, footer_file],
                                   components=[[bot_select_menu], [personalized_bot_button]])

    @commands.Cog.on_select('^select_bot_options$')
    async def order_bot_step_1(self, interaction, select_menu):
        bot_type_mapping = {
            "modmail_bot": "Modmail Bot",
            "music_bot": "Music Bot",
            "admin_bot": "Admin Bot",
            "tempvoice_bot": "TempVoice Bot",
            "studies_bot": "Studies Bot"
        }

        user_id = interaction.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        community_advisor = self.bot.get_emoji(EMOJIS["community_advisor"])
        community_developer = self.bot.get_emoji(EMOJIS["community_developer"])

        # Getting user ID to fetch stored information
        user_id = interaction.author.id
        selected_value = select_menu.values[0]
        bot_type = bot_type_mapping.get(selected_value)

        # Storing bot type to the user ID
        if bot_type:
            user_info = user_data.get(user_id, {})
            user_info["bot_type"] = bot_type
            user_data[user_id] = user_info

        # Log the selected bot type
        logging.info(f'{str(user_id)} - Bot type selected by user: %s', bot_type)

        # remove old message
        await self.send_processing_response(interaction)

        # Header over Bot message
        header = await self.header()

        # Create Discord bot selection description
        description = discord.Embed(
            description=language["discord_order_bot_step_1_description"].format(community_developer=community_developer),
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await self.attachments()

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
                               attachments=[banner_file, icon_file, footer_file],
                               components=[buttons]
                               )

    @commands.Cog.on_click('^users:(\d+)$')
    async def order_bot_part_2(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        user_amount_pricing = int(button.custom_id.split(":")[1])

        # Extract user ID from the interaction context
        user_id = ctx.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        log_timeoutremoved = self.bot.get_emoji(EMOJIS["log_timeoutremoved"])
        community_developer = self.bot.get_emoji(EMOJIS["community_developer"])

        # Calculate the price based on the hosting duration and user ID
        preis = calculate_price(user_amount_pricing, user_id)

        # Convert the price to a numeric value for further processing
        preis_numeric = float(preis.replace("€", "").replace(",", "."))

        # Format the price for single month hosting
        price_single_month = format_price(preis_numeric)

        # Format the prices for multiple month hosting
        price_3_months = format_price(preis_numeric * 3)
        price_6_months = format_price(preis_numeric * 6)
        price_12_months = format_price(preis_numeric * 12)

        # Log the user amount price
        logging.info(f'{str(user_id)} - User selected user amount pricing: %s', price_single_month)

        # remove old message
        await self.send_processing_response(ctx)

        # Header over Bot message
        header = await self.header()

        # Discord bot selection.
        description = discord.Embed(
            description=language["discord_order_bot_step_2_description"].format(community_developer=community_developer),
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await self.attachments()

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
                       attachments=[banner_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^months:(\d+)$')
    async def order_bot_part_3(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        hosting_duration = int(button.custom_id.split(":")[1])

        # Extract user ID from the interaction context
        user_id = ctx.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        function_tick = self.bot.get_emoji(1217203424425152582)
        function_cross = self.bot.get_emoji(1217203796065648691)
        community_developer = self.bot.get_emoji(1217203400593117256)

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_data.get(user_id, {})

        # Update user information with the selected hosting duration
        user_info["hosting_duration"] = hosting_duration

        # Update user data in the database
        user_data[user_id] = user_info

        # Log the hosting duration
        logging.info(f'{str(user_id)} - User selected hosting duration: %s', hosting_duration)

        # Remove old message
        await self.send_processing_response(ctx)

        # Create header
        header = await self.header()

        # About Me Pack message
        description = discord.Embed(
            description=language["discord_order_bot_step_3_description"].format(community_developer=community_developer),
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_thumbnail(url="attachment://about_me_pack.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load About Me Pack thumbnail
        about_me_pack_path = "./pictures/about_me_pack.png"
        about_me_pack_file = discord.File(about_me_pack_path, filename="about_me_pack.png")

        # Load other attachments
        banner_file, icon_file, footer_file = await self.attachments()

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
                       attachments=[banner_file, icon_file, footer_file, about_me_pack_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click('^about_me_pack_(yes|no)$')
    async def order_bot_part_4(self, ctx: discord.ComponentInteraction, button):
        # Extract the selection made by the user from the button's custom ID
        about_me_pack = button.custom_id.split("_")[-1]

        # Extract user ID from the interaction context
        user_id = ctx.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        community_developer = self.bot.get_emoji(1217203400593117256)
        community_owner = self.bot.get_emoji(1217203408516284516)

        # Retrieve user data from the database or initialize an empty dictionary if not found
        user_info = user_data.get(user_id, {})

        # Update user information with the selected about me pack
        user_info["about_me_pack"] = about_me_pack

        # Update user data in the database
        user_data[user_id] = user_info

        # Log not-/selected about me pack
        logging.info(f'{str(user_id)} - User selected About Me Pack: %s', about_me_pack)

        # Remove the old message
        await self.send_processing_response(ctx)

        # Create a header for the bot message
        header = await self.header()

        # Create the bot message
        description = discord.Embed(
            description=language["discord_order_bot_step_4_description"].format(community_developer=community_developer),
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Load attachments
        banner_file, icon_file, footer_file = await self.attachments()

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
                       attachments=[banner_file, icon_file, footer_file],
                       components=[buttons]
                       )

    @commands.Cog.on_click("^configure_bot$")
    async def order_bot_part_4_modal(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user_id = ctx.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve user data if available, otherwise set default values
        user_info = user_data.get(user_id, {})
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
        user_id = ctx.author.id

        # Define user language and load language data
        user_info = user_data.get(user_id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/buy_product_languages.json"
        language = load_language_data(file_path, user_language)

        # Retrieve emojis
        log_membershipscreening = self.bot.get_emoji(1217203998659055797)
        community_developer = self.bot.get_emoji(1217203400593117256)
        plant_plant = self.bot.get_emoji(1217204087884611665)

        # Get bot name and status entered by the user
        bot_name = ctx.get_field('bot_name').value or None
        bot_status = ctx.get_field('bot_status').value or None

        # Update user data with bot name and status
        user_info = user_data.get(user_id, {})
        user_info["bot_name"] = bot_name
        user_info["bot_status"] = bot_status
        user_data[user_id] = user_info

        # Determine hosting duration ending
        hosting_duration_month = "month" if user_info.get('hosting_duration', 'Not entered') == 1 else "months"

        # Determine about me pack status and cost
        about_me_pack_status = 'Selected' if user_info.get('about_me_pack') == 'yes' else 'Not selected'
        about_me_pack_total_cost = 0.50 * int(user_info.get('hosting_duration', 1))
        about_me_pack_cost_text = f" (Cost: {format_price(about_me_pack_total_cost)})" if about_me_pack_status == 'Selected' else ""
        price_about_me_pack = about_me_pack_total_cost if about_me_pack_status == 'Selected' else 0

        # Calculate total price
        total_price = price_about_me_pack + (float(user_info.get('user_amount_pricing', '0').replace('€', '').replace(',', '.')) * int(user_info.get('hosting_duration', '1')))
        total_price_formatted = f"{total_price:.2f}€"

        # Get all user information for the further embed
        bot_type = user_info.get('bot_type', 'Not entered')
        bot_users = user_info.get('bot_users', 'Not entered')
        bot_user_pricing = user_info.get('user_amount_pricing', 'Not entered')
        bot_hosting_duration = user_info.get('hosting_duration', 'Not entered')

        # Remove old message
        await self.send_processing_response(ctx)

        # Header over Bot message
        header = await self.header()

        # Log all user information that have been saved
        logging.info(f'{str(user_id)} - Bot summary created by user: %s', user_info)

        formatted_description = language["discord_order_bot_step_5_description"].format(
            community_developer=community_developer,
            bot_type=bot_type,
            bot_name=bot_name,
            bot_status=bot_status,
            bot_users=bot_users,
            about_me_pack_status=about_me_pack_status,
            about_me_pack_cost_text=about_me_pack_cost_text,
            bot_user_pricing=bot_user_pricing,
            bot_hosting_duration=bot_hosting_duration,
            hosting_duration_month=hosting_duration_month,
            total_price_formatted=total_price_formatted,
            plant_plant=plant_plant
        )

        # Discord bot selection.
        description = discord.Embed(
            description=formatted_description,
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await self.attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header, description],
                       attachments=[banner_file, icon_file, footer_file],
                       components=[[
                           Button(
                               style=ButtonStyle.green,
                               emoji=log_membershipscreening,
                               label=language["discord_order_bot_step_5_accept_rules_lable"],
                               custom_id="about_me_pack:yes",
                           )
                       ]]
                       )

        # Delete user data after processing
        del user_data[user_id]


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(BuyDiscordBot(reelab_bot))
