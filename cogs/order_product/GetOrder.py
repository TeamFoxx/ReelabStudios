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
from discord import SelectOption
from discord.ext import commands

import config
from utils.utils import attachments


# ⏤ { function definitions } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def format_value(key, value):
    """
    Applies specific formatting based on the key indicating the type of the value.
    """
    if key in ['setup_fees', 'total_price', 'user_amount_pricing']:
        # Format as a price with two decimal places and Euro sign
        return f"{value:.2f}€"
    elif key == 'hosting_duration':
        # Add 'month' or 'months' based on the value
        if value == 1:
            return f"{value} month"
        else:
            return f"{value} months"
    else:
        return value


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class GetOrder(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="myorders",
        description="Retrieve and display your order details.",
        guild_ids=[1216127716970070128]
    )
    async def my_orders(self, ctx):
        """
        Retrieves and displays the orders for the invoking user in an embed format.
        """
        # Retrieve emojis
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
        community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

        user_id = str(ctx.author.id)
        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Filter orders by user ID
        user_orders = {order_id: details for order_id, details in filedata.items() if
                       str(details['user_id']) == user_id}

        # Respond with a message if no orders found
        if not user_orders:
            embed = discord.Embed(description=f"{log_memberjoin} You do not yet have any orders.",
                                  color=config.EMBED_COLOR)
            embed.set_image(url="attachment://reelab_banner_blue.png")
            await ctx.respond(embed=embed, hidden=True)
            return

        # If only one order, directly display it
        if len(user_orders) == 1:
            # Attachments
            _, _, footer_file = await attachments()

            order_id, details = next(iter(user_orders.items()))
            embed = self.create_order_embed(order_id, details)
            await ctx.respond(embed=embed, file=footer_file, hidden=True)
            return

        # Create select menu options dynamically
        select_options = []
        for order_id, details in user_orders.items():
            product = next(iter(details['products'].values()))
            select_options.append(
                SelectOption(
                    label=product['type'],
                    description=f"Order ID: {order_id}",
                    emoji=community_member,
                    value=f'order:{order_id}'
                )
            )

        # Create select menu
        select_menu = discord.SelectMenu(
            placeholder='Select other order',
            custom_id='orders_select',
            disabled=False,
            options=select_options[:25]  # Discord limits select menus to 25 options
        )

        # Create action row for the select menu
        action_row = discord.ActionRow(select_menu)

        embed = discord.Embed(description=f"{log_memberjoin} Please select your order from the menu below:",
                              color=config.EMBED_COLOR)
        embed.set_image(url="attachment://reelab_banner_blue.png")

        # Attachments
        _, _, footer_file = await attachments()

        await ctx.respond(embed=embed, file=footer_file, components=[action_row], hidden=True)

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

        embed = self.create_order_embed(selected_order_id, selected_order_details)
        await interaction.edit(embed=embed, attachments=[footer_file])

    def create_order_embed(self, order_id: str, details: dict) -> discord.Embed:
        """
        Creates a Discord embed for a single order, dynamically handling different product types and separating details into categories.
        """
        embed = discord.Embed(title="Order Details", color=config.EMBED_COLOR)
        embed.add_field(name="Order ID", value=f"```fix\n{order_id}\n```", inline=False)
        embed.add_field(name="User ID", value=f"```fix\n{details.get('user_id', 'N/A')}\n```", inline=True)
        embed.add_field(name="User Name", value=f"```fix\n{details.get('user_name', 'N/A')}\n```", inline=True)
        embed.add_field(name="Status", value=f"```fix\n{details.get('status', 'N/A')}\n```", inline=False)

        embed.set_image(url="attachment://reelab_banner_blue.png")

        # Product templates for displaying relevant details based on the product type
        product_templates = {
            'discord_bot': [
                ('Configuration', ['bot_name', 'bot_status', 'bot_users', 'about_me_pack']),
                ('Pricing', ['setup_fees', 'total_price']),
                ('Administration', ['hosting_duration', 'start_date', 'expire_date'])
            ],
            'website': [
                ('Domain Details', ['domain', 'hosting_provider']),
                ('Pricing', ['hosting_duration', 'total_price']),
                ('Dates', ['start_date', 'expire_date'])
            ]
            # Add more templates for other product types as needed
        }

        products = details.get('products', {})
        for product_name, sections in products.items():
            product_type = products[product_name].get('type', 'N/A')  # Retrieve the type separately
            embed.add_field(name=f"{product_name.capitalize()} Details", value=f"- Type: `{product_type}`",
                            inline=False)  # Display type directly under product details
            template = product_templates.get(product_name, [])
            for section_name, keys in template:
                section_content = "\n".join(
                    f"- {key.replace('_', ' ').capitalize()}: `{format_value(key, products[product_name].get(key))}`"
                    for key in keys if key in products[product_name] and products[product_name][key]
                )
                # Only add the field if there is content to display
                if section_content.strip():
                    embed.add_field(name=section_name, value=section_content, inline=False)
                    # embed.add_field(name='\u200b', value='\u200b', inline=False)  # Add a spacer

        embed.set_footer(text="For support and inquiries, please contact info@reelab.studio")
        return embed

    @commands.Cog.slash_command(
        name="getorder",
        description="Retrieve and display other user order details.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128]
    )
    async def get_order(self, ctx, user_id: str):
        """
        Retrieves and displays the orders for the invoking user in an embed format.
        """
        # Retrieve emojis
        log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
        community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

        script_directory = Path(__file__).resolve().parent.parent.parent
        file_path = script_directory / "data/orders.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            filedata = json.load(file)

        # Filter orders by user ID
        user_orders = {order_id: details for order_id, details in filedata.items() if
                       str(details['user_id']) == user_id}

        # Respond with a message if no orders found
        if not user_orders:
            embed = discord.Embed(description=f"{log_memberjoin} No orders found for user ID {user_id}.",
                                  color=config.EMBED_COLOR)
            embed.set_image(url="attachment://reelab_banner_blue.png")
            await ctx.respond(embed=embed, hidden=True)
            return

        # If only one order, directly display it
        if len(user_orders) == 1:
            # Attachments
            _, _, footer_file = await attachments()

            order_id, details = next(iter(user_orders.items()))
            embed = self.create_order_embed(order_id, details)
            await ctx.respond(embed=embed, file=footer_file, hidden=True)
            return

        # Create select menu options dynamically
        select_options = []
        for order_id, details in user_orders.items():
            product = next(iter(details['products'].values()))
            select_options.append(
                SelectOption(
                    label=product['type'],
                    description=f"View details for {product['type']}",
                    emoji=community_member,
                    value=f'order:{order_id}'
                )
            )

        # Create select menu
        select_menu = discord.SelectMenu(
            placeholder='Select other order',
            custom_id='orders_select',
            disabled=False,
            options=select_options[:25]  # Discord limits select menus to 25 options
        )

        # Create action row for the select menu
        action_row = discord.ActionRow(select_menu)

        embed = discord.Embed(description=f"{log_memberjoin} Please select your order from the menu below:",
                              color=config.EMBED_COLOR)
        embed.set_image(url="attachment://reelab_banner_blue.png")

        # Attachments
        _, _, footer_file = await attachments()

        await ctx.respond(embed=embed, file=footer_file, components=[action_row], hidden=True)

    # Order product section.
    @commands.Cog.on_click('^delete_order:(.*)$')
    async def delete_order(self, ctx: discord.ComponentInteraction, button):
        """
        Deletes an order from the JSON file based on the order ID.
        """
        if ctx.author.id in config.developer or ctx.author.id == 599204513722662933:
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
    reelab_bot.add_cog(GetOrder(reelab_bot))
