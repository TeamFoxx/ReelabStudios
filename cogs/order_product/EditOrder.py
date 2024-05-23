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
from pathlib import Path

import discord
from discord.ext import commands

import config
from utils.OrderBackend import my_order_button


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class EditOrder(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_click('^myorder:(.*)$')
    async def my_order_thread_button(self, ctx, button):
        await my_order_button(self, ctx, button)

    # Order product section.
    @commands.Cog.on_click('^delete_order:(.*)$')
    async def delete_order(self, ctx: discord.ComponentInteraction, button):
        """
        Deletes an order from the JSON file based on the order ID.
        """
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            order_id = button.custom_id.split(":")[1]

            # Retrieve emojis
            log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])

            script_directory = Path(__file__).resolve().parent.parent.parent
            file_path = script_directory / "data/orders.json"

            with open(file_path, 'r+', encoding='utf-8') as file:
                # Read the existing data
                filedata = json.load(file)

                # Check if the order exists
                if order_id in filedata:
                    # Remove the order
                    del filedata[order_id]

                    # Write the updated data back to the file
                    file.seek(0)
                    file.truncate()
                    json.dump(filedata, file, indent=4)

                    # Acknowledge the interaction and inform the user
                    embed = discord.Embed(
                        description=f"{log_memberjoin} - Order `{order_id}` has been **deleted successfully**.",
                        color=config.EMBED_COLOR)
                    embed.set_image(url="attachment://reelab_banner_blue.png")

                    await ctx.edit(embed=embed, components=[])
                else:
                    # Acknowledge the interaction and inform the user that the order was not found
                    embed = discord.Embed(description=f"{log_memberjoin} - Order `{order_id}` **not found**.",
                                          color=config.EMBED_COLOR)
                    embed.set_image(url="attachment://reelab_banner_blue.png")
                    await ctx.edit(embed=embed, components=[])
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(EditOrder(reelab_bot))
