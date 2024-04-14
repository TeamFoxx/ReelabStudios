# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Developed by Foxx
# »› Copyright © 2024 Aurel Hoxha. All rights reserved.
# »› GitHub: https://github.com/TeamFoxx
# »› For support and inquiries, please contact hello@aurelhoxha.de
# »› Use of this program is subject to the terms of the All Rights Reserved License.
# »› A copy of the license can be found in the "LICENSE" file in the root directory of this project.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { imports } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

from cogs import *
from config import EMOJIS, EMBED_COLOR, HEADER_COLOR

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
user_data = {}
counting_file_path = "data/counting.json"


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


class BuyGraphic(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.order_product_channel_id = 1216178294458814526
        self.official_staff_id = 1216137762537996479

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

    @commands.Cog.on_select('^products$')
    async def graphic_products(self, interaction, select_menu):
        # Check if the selected value of the select menu is "order_discord_bot"
        if select_menu.values[0] == "order_graphics":
            # Import required modules
            from cogs.ProductPurchase import user_lang

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
            file_path = script_directory / "languages/order_graphic_language_file.json"

            # Load language data based on the user's language preference
            language = load_language_data(file_path, user_language)

            # Retrieve emojis
            log_membershipscreening = self.bot.get_emoji(EMOJIS["log_membershipscreening"])
            plant_plant = self.bot.get_emoji(EMOJIS["plant_plant"])

            # remove old message
            await self.send_processing_response(interaction)

            # Header over Bot message
            header = await self.header()

            # Create Discord bot selection description
            description = discord.Embed(
                description=language["order_graphics_description"].format(plant_plant=plant_plant),
                color=EMBED_COLOR,
            )
            description.set_image(url="attachment://reelab_banner_blue.png")
            description.set_footer(text="~ The official Reelab Studio Discord Bot")

            # Attachments
            banner_file, icon_file, footer_file = await self.attachments()

            # creates a list of buttons to be sent
            buttons = [
                Button(
                    style=ButtonStyle.green,
                    emoji=log_membershipscreening,
                    label=language["order_graphics_accept_tos"],
                    custom_id="graphic_accept_tos",
                )
            ]

            # Edit interaction with new embed and components
            await interaction.edit(embeds=[header, description],
                                   attachments=[banner_file, icon_file, footer_file],
                                   components=[buttons]
                                   )

    @commands.Cog.on_click("^graphic_accept_tos$")
    async def order_graphic_open_thread(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Define user language and load language data
        user_info = user_data.get(user.id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/order_graphic_language_file.json"
        language = load_language_data(file_path, user_language)

        # Log all user information that have been saved
        logging.info(f'{str(user.id)} - Graphic ordered by user: %s', user_info)

        # Get Order Product channel for thread creation
        channel = ctx.guild.get_channel(self.order_product_channel_id)

        # Get Official Staff role
        staff = ctx.guild.get_role(self.official_staff_id)

        # Retrieve emojis
        plant_plant = self.bot.get_emoji(EMOJIS["plant_plant"])
        function_cross = self.bot.get_emoji(EMOJIS["function_cross"])
        community_advisor = self.bot.get_emoji(EMOJIS["community_advisor"])

        # Load the current counting
        counting = load_counting()

        # Create a thread with a unique name based on the counting
        thread = await channel.create_thread(
            name=f"#{counting:04} | {user} | Graphics",
            reason=f"#{counting:04} | {user} | Graphics",
            private=True,
            invitable=True
        )

        # Increment and save the counting for future threads
        counting += 1
        save_counting(counting)

        # Remove old message
        await self.send_processing_response(ctx)

        # Header over Bot message
        header = await self.header()

        # Send summary in thread.
        description = discord.Embed(
            description=language["order_graphic_thread_message"].format(user=user.mention,
                                                                        plant_plant=plant_plant,
                                                                        community_advisor=community_advisor),
            color=EMBED_COLOR,
        )
        description.set_image(url="attachment://reelab_banner_blue.png")
        description.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await self.attachments()

        # Send the bot summary message with buttons for pricing information and closing the order
        await thread.send(language["order_graphic_thread_ping_message"].format(user=user.mention, staff=staff.mention))
        await thread.send(embeds=[header, description],
                          files=[banner_file, icon_file, footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=plant_plant,
                                  label=language["order_graphic_thread_price_button"],
                                  custom_id="graphic_pricing_information",
                              ),
                              Button(
                                  style=ButtonStyle.grey,
                                  emoji=function_cross,
                                  label=language["order_graphic_thread_close_button"],
                                  custom_id="close_graphic_order",
                              )
                          ]]
                          )

        # Send summary in thread.
        user_message = discord.Embed(
            description=language["order_graphic_user_message"].format(thread=thread.mention),
            color=EMBED_COLOR,
        )
        user_message.set_image(url="attachment://reelab_banner_blue.png")
        user_message.set_footer(text="~ The official Reelab Studio Discord Bot")

        # Attachments
        banner_file, icon_file, footer_file = await self.attachments()

        # Edit the message with updated embed and components
        await ctx.edit(embeds=[header, user_message],
                       attachments=[banner_file, icon_file, footer_file],
                       )

    @commands.Cog.on_click("^graphic_pricing_information$")
    async def graphic_pricing_information(self, ctx: discord.ComponentInteraction, button):
        # Extract user ID from the interaction context
        user = ctx.author

        # Define user language and load language data
        user_info = user_data.get(user.id, {})
        user_language = user_info.get('user_language', 'en')
        script_directory = Path(__file__).resolve().parent.parent
        file_path = script_directory / "languages/order_graphic_language_file.json"
        language = load_language_data(file_path, user_language)

        # Log pricing information
        logging.info(f'{str(user.id)} - Pricing information called by: %s', user.name)

        # Retrieve emojis
        plantbig_plant = self.bot.get_emoji(EMOJIS["plantbig_plant"])
        log_memberjoin = self.bot.get_emoji(EMOJIS["log_memberjoin"])
        community_admin = self.bot.get_emoji(EMOJIS["community_admin"])

        # Send pricing information in chat.
        response_message = discord.Embed(
            color=EMBED_COLOR,
            description=language["order_graphic_pricing_information"].format(plantbig_plant=plantbig_plant,
                                                                             log_memberjoin=log_memberjoin,
                                                                             community_admin=community_admin)
        )
        await ctx.respond(embed=response_message, hidden=True)

    @commands.Cog.on_click("^close_graphic_order$")
    async def order_graphic_close_thread(self, ctx: discord.ComponentInteraction, button):
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
            color=EMBED_COLOR,
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
    reelab_bot.add_cog(BuyGraphic(reelab_bot))
