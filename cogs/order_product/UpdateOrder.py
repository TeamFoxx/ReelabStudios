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
from discord import Modal, TextInput, ButtonStyle, Button
from discord.ext import commands

import config
from utils.OrderBackend import create_order_embed, my_order_button_selectmenu


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class UpdateOrder(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

        # Define templates for different product types to display relevant details /
        # IMPORTANT: Change in utils/OrderBackend >> create_order_embed as well.
        self.product_templates = {
            'discord_bot': [
                ('Configuration', ['bot_name', 'bot_status', 'bot_users', 'about_me_pack']),
                ('Pricing', ['setup_fees', 'total_price']),
                ('Hosting / Administration', ['hosting_duration', 'start_date', 'expire_date']),
                ('Paid', ['payment_method', 'transaction_id']),
                ('Further Information', ['Info:', 'Note:', 'Warning:'])
            ],
            'website': [
                ('Domain Details', ['domain']),
                ('Pricing', ['total_price']),
                ('Hosting / Administration', ['hosting_duration', 'start_date', 'expire_date']),
                ('Paid', ['payment_method', 'transaction_id']),
                ('Further Information', ['Info:', 'Note:', 'Warning:'])
            ],
            'graphic': [
                ('Details', ['graphic_type', 'dimensions', 'file_format']),
                ('Pricing', ['total_price']),
                ('Delivery', ['delivery_date']),
                ('Paid', ['payment_method', 'transaction_id']),
                ('Further Information', ['Info:', 'Note:', 'Warning:'])
            ]
            # Add more templates for other product types as needed
        }

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.on_click('^order_update:(.*)$')
    async def update_order(self, ctx: discord.ComponentInteraction, button):
        """
        Slash command to update order details. This command retrieves the order by its ID and
        displays an embed with buttons for each section (e.g., Configuration, Pricing, Hosting).
        """
        # Retrieve emojis
        community_manager = self.bot.get_emoji(config.EMOJIS["community_manager"])

        order_id = button.custom_id.split(":")[1]

        # Define the path to the orders JSON file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        # Load the orders data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Find the order by order ID
        order = filedata.get(order_id)

        if not order:
            await ctx.respond(f"Order with ID {order_id} not found.", hidden=True)
            return

        product_type = list(order['products'].keys())[0]
        template = self.product_templates.get(product_type, [])

        buttons = [
            Button(
                style=ButtonStyle.grey,
                label=section_name,
                emoji=community_manager,
                custom_id=f"update_order:{order_id}:{section_name.replace(' ', '_')}"
            ) for section_name, _ in template
        ]

        embed = create_order_embed(order_id, order)
        await ctx.edit(embed=embed, components=[buttons])

    @commands.Cog.on_click('^update_order:(.*):(.*)$')
    async def update_order_modal(self, ctx: discord.ComponentInteraction, button):
        """
        Event handler for button clicks. Opens a modal for updating order details
        when a section button is clicked.
        """
        order_id, section = button.custom_id.split(":")[1:3]
        section = section.replace('_', ' ')

        # Define the path to the orders JSON file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        # Load the orders data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Find the order by order ID
        order = filedata.get(order_id)
        product_type = list(order['products'].keys())[0]
        template = self.product_templates.get(product_type, [])

        modal_components = []
        for section_name, keys in template:
            if section_name == section:
                modal_components = [
                    TextInput(
                        label=key.replace('_', ' ').capitalize(),
                        custom_id=key,
                        value=f"{order['products'][product_type].get(key, '')}",
                        required=False,
                        style=1,
                        max_length=120,
                    ) for key in keys
                ]
                break

        # Überprüfen, ob modal_components korrekt initialisiert wurde
        if not modal_components:
            await ctx.respond("Error creating modal components.", hidden=True)
            return

        modal = Modal(
            title=f"Update {section} for Order",
            custom_id=f'update_order_submit:{order_id}:{section.replace(" ", "_")}',
            components=[modal_components]
        )

        await ctx.respond_with_modal(modal)

    @commands.Cog.on_submit('^update_order_submit:(.*):(.*)$')
    async def update_order_submit(self, ctx: discord.ModalSubmitInteraction):
        """
        Event handler for modal submissions. Updates the order details in the JSON file
        when the modal is submitted.
        """
        order_id, section = ctx.custom_id.split(":")[1:3]
        section = section.replace('_', ' ')

        # Define the path to the orders JSON file
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        # Load the orders data from the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Find the order by order ID
        order = filedata.get(order_id)
        product_type = list(order['products'].keys())[0]

        # Update the order details with the values from the modal
        for field in ctx.fields:
            field_value = ctx.get_field(field.custom_id).value
            if field_value is not None:
                try:
                    field_value = float(field_value) if '.' in field_value else int(field_value)
                except ValueError:
                    pass
                order['products'][product_type][field.custom_id] = field_value

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(filedata, file, ensure_ascii=False, indent=4)

        await my_order_button_selectmenu(self, ctx)

        embed = discord.Embed(
            description=f"The **{section}** for order ID `{order_id}` has been **updated**.",
            color=config.EMBED_COLOR
        )
        embed.set_image(url="attachment://reelab_banner_blue.png")

        await ctx.respond(embed=embed, hidden=True)


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(UpdateOrder(reelab_bot))
