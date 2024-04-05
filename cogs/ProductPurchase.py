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


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤
class ProductPurchase(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

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
                        f"- Need assistance or have questions? Feel free to ask our staff members in the server!\n",
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


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(ProductPurchase(reelab_bot))
