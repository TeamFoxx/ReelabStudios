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

class UtilityDonation(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="support-us",
        description='Send the "Donation & Booster" Message to this chat.',
        default_required_permissions=discord.Permissions(administrator=True)
    )
    async def donation(self, ctx):
        paypal = self.bot.get_emoji(1216828302098956299)

        donation_head = discord.Embed(colour=0x2b2d31)
        donation_head.set_author(name="The official Reelab Studio Discord Server", url="https://reelab.studio/",
                                 icon_url="attachment://reelab_logo_white.png")
        donation_head.set_image(url="attachment://reelab_banner_white.gif")

        booster_msg = discord.Embed(
            description=f"# Boost the server\n"
                        f"> Boosting our server helps us enhance the experience for everyone in the community. "
                        f"Your support enables us to unlock additional features and perks that benefit all members. "
                        f"Plus, we want to show our appreciation to our loyal boosters!\n\n"
                        f"- Users who have been boosting the server for **over a month** will receive a **5% discount** on their next purchase.\n"
                        f"- Those with **3 months** will get a **10% discount**.\n"
                        f"- Users with **6 months** of boosting will enjoy a generous **20% discount** on their next purchase.\n\n"
                        f"» __Please note that the discounts **do not count for bundles.**__\n\n"
                        f"> 🏡 Thank you for considering boosting our server and for being a valued member of our community!\n\n"
                        f"<@&1216502189594382377> - This role will be yours during your booster subscription.",
            color=0xce63c0,
        )
        booster_msg.set_image(url="attachment://reelab_banner_pink.png")

        donation_msg = discord.Embed(
            description=f"# PayPal Donators\n"
                        f"> Your donation allows us to move forward with our projects and continually improve our services. "
                        f"Remember that your donation not only supports our services, "
                        f"but also the tools and resources we use to create world-class products and graphics.\n\n"
                        f"<@&1216849547922243795> - This role will be yours for life.",
            color=0x48689b,
        )
        donation_msg.set_image(url="attachment://reelab_banner_blue.png")

        banner_path = "./pictures/reelab_banner_white.gif"
        banner_file = discord.File(banner_path, filename="reelab_banner_white.gif")

        icon_path = "./pictures/reelab_logo_white.png"
        icon_file = discord.File(icon_path, filename="reelab_logo_white.png")

        footer_path = "./pictures/reelab_banner_blue.png"
        footer_file = discord.File(footer_path, filename="reelab_banner_blue.png")

        pink_footer_path = "./pictures/reelab_banner_pink.png"
        pink_footer_file = discord.File(pink_footer_path, filename="reelab_banner_pink.png")

        await ctx.respond(embeds=[donation_head, booster_msg, donation_msg],
                          files=[footer_file, banner_file, icon_file, pink_footer_file],
                          components=[[
                              Button(
                                  style=ButtonStyle.link,
                                  emoji=f"{paypal}",
                                  label="Donate using PayPal",
                                  url="https://www.paypal.com/donate/?hosted_button_id=H26RV4GY6UFCG"
                              )
                          ]]
                          )


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(UtilityDonation(reelab_bot))
