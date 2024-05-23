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
from utils.OrderBackend import my_order, get_order, create_order_embed
from utils.Utils import attachments


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class GetOrder(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="myorders",
        description="Retrieve and display your order details.",
        guild_ids=[1216127716970070128]
    )
    async def my_orders(self, ctx):
        """
        Command to retrieve and display the invoking user's order details.
        """
        # Call the function to fetch and display the user's orders
        await my_order(self, ctx)

    @commands.Cog.slash_command(
        name="getorder",
        description="Retrieve and display other user order details.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128]
    )
    async def get_orders(self, ctx, user_id: str):
        """
        Command to retrieve and display another user's order details.
        """
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            # Check if the user has permission to use the command
            await get_order(self, ctx, user_id)  # Call the function to fetch and display the specified user's orders
        else:
            # Respond with a permission error message if the user is not authorized
            await ctx.respond("You do not have permission to use this command.", hidden=True)

    @commands.Cog.on_select('^orders_select$')
    async def order_select(self, interaction, select_menu):
        """
        Handles the select menu interaction to display the selected order details.
        """
        selected_order_id = select_menu.values[0].split(":")[1]

        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        selected_order_details = filedata[selected_order_id]

        # Attachments
        _, _, footer_file = await attachments()

        embed = create_order_embed(selected_order_id, selected_order_details)
        await interaction.edit(embed=embed, attachments=[footer_file])


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(GetOrder(reelab_bot))
