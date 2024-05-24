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
from discord import Modal, TextInput
from discord.ext import commands

import config
from utils.OrderBackend import my_order_button


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class EditOrder(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_click('^myorder:(.*)$')
    async def my_order_thread_button(self, ctx, button):
        await my_order_button(self, ctx, button)

    @commands.Cog.on_click('^status_update:(.*)$')
    async def status_update(self, ctx: discord.ComponentInteraction, button):
        """
        Deletes an order from the JSON file based on the order ID.
        """

        # Retrieve emojis
        function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            order_id = button.custom_id.split(":")[1]

            # Define the path to the orders JSON file
            script_directory = Path(__file__).resolve().parent.parent.parent
            file_path = script_directory / "data/orders.json"

            # Load the orders data from the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                filedata = json.load(file)

            # Find the order by order ID
            order = filedata.get(order_id)

            if order:
                # Define the modal with input fields for bot name and status
                modal = Modal(
                    title=f"Update {order['user_name']}'s Order",
                    custom_id=f'order_status_update:{order_id}',
                    components=[
                        [
                            TextInput(
                                label="Change Order Status",
                                custom_id='order_status',
                                placeholder=f"{order['status']}",
                                required=True,
                                style=1,
                                max_length=120,
                            )
                        ]
                    ]
                )

                # Respond to the interaction with the modal
                await ctx.respond_with_modal(modal)
            else:
                embed = discord.Embed(description=f"{function_emergency} - Order `{order_id}` **not found**.",
                                      color=config.EMBED_COLOR)
                embed.set_image(url="attachment://reelab_banner_blue.png")
                await ctx.edit(embed=embed, components=[])
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)

    @commands.Cog.on_submit('^order_status_update:(.*)$')
    async def status_update_submit(self, ctx: discord.ModalSubmitInteraction):
        """
        Handles the submission of the status update modal.
        """
        # Retrieve emojis
        function_time = self.bot.get_emoji(config.EMOJIS["function_time"])
        function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

        # Extract the order ID from the modal's custom ID
        order_id = ctx.custom_id.split(":")[1]

        # Get the entered value from the modal submission
        order_status = str(ctx.get_field('order_status').value)

        # Define the path to the orders JSON file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        # Load the orders data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Find the order by order ID
        order = filedata.get(order_id)

        if order:
            # Update the order status
            order['status'] = order_status

            # Save the updated order data back to the JSON file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(filedata, file, ensure_ascii=False, indent=4)

            # Send an embed to confirm the status update
            embed = discord.Embed(
                description=f"{function_time} - The **status** for order ID `{order_id}` has been **updated** to `{order_status}`.",
                color=config.EMBED_COLOR
            )
            embed.set_image(url="attachment://reelab_banner_blue.png")

            await ctx.edit(embed=embed, components=[])
        else:
            embed = discord.Embed(description=f"{function_emergency} - Order `{order_id}` **not found**.",
                                  color=config.EMBED_COLOR)
            embed.set_image(url="attachment://reelab_banner_blue.png")
            await ctx.edit(embed=embed, components=[])

    @commands.Cog.on_click('^confirm_payment:(.*)$')
    async def confirm_payment(self, ctx: discord.ComponentInteraction, button):
        # Retrieve emojis
        function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            order_id = button.custom_id.split(":")[1]

            # Define the path to the orders JSON file
            script_directory = Path(__file__).resolve().parent.parent.parent
            file_path = script_directory / "data/orders.json"

            # Load the orders data from the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                filedata = json.load(file)

            # Find the order by order ID
            order = filedata.get(order_id)

            if order:
                # Define the modal with input fields for bot name and status
                modal = Modal(
                    title=f"Update {order['user_name']}'s Order",
                    custom_id=f'order_status_update:{order_id}',
                    components=[
                        [
                            TextInput(
                                label="Change Order Status",
                                custom_id='order_status',
                                placeholder=f"{order['status']}",
                                required=True,
                                style=1,
                                max_length=120,
                            )
                        ]
                    ]
                )

                # Respond to the interaction with the modal
                await ctx.respond_with_modal(modal)
            else:
                embed = discord.Embed(description=f"{function_emergency} - Order `{order_id}` **not found**.",
                                      color=config.EMBED_COLOR)
                embed.set_image(url="attachment://reelab_banner_blue.png")
                await ctx.edit(embed=embed, components=[])
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)

    @commands.Cog.on_click('^delete_order:(.*)$')
    async def delete_order(self, ctx: discord.ComponentInteraction, button):
        """
        Deletes an order from the JSON file based on the order ID.
        """
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            order_id = button.custom_id.split(":")[1]

            # Retrieve emojis
            log_memberleave = self.bot.get_emoji(config.EMOJIS["log_memberleave"])
            function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

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
                        description=f"{log_memberleave} - **Order** `{order_id}` has been **deleted** successfully.",
                        color=config.EMBED_COLOR)
                    embed.set_image(url="attachment://reelab_banner_blue.png")

                    await ctx.edit(embed=embed, components=[])
                else:
                    # Acknowledge the interaction and inform the user that the order was not found
                    embed = discord.Embed(description=f"{function_emergency} - Order `{order_id}` **not found**.",
                                          color=config.EMBED_COLOR)
                    embed.set_image(url="attachment://reelab_banner_blue.png")
                    await ctx.edit(embed=embed, components=[])
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(EditOrder(reelab_bot))
