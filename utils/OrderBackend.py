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
from discord import SelectOption, Button, ButtonStyle

import config
from utils.Utils import attachments


# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

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


def create_order_embed(order_id: str, details: dict) -> discord.Embed:
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


async def my_order(self, ctx):
    """
    Retrieves and displays the orders for the invoking user in an embed format.
    """
    # Retrieve emojis
    log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
    community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

    user_id = str(ctx.author.id)
    script_directory = Path(__file__).resolve().parent.parent
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
        embed = create_order_embed(order_id, details)
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


async def get_order(self, ctx, user_id: str):
    """
    Retrieves and displays the orders for the invoking user in an embed format.
    """
    # Retrieve emojis
    log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
    community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

    script_directory = Path(__file__).resolve().parent.parent
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
        embed = create_order_embed(order_id, details)
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


async def my_order_button(self, ctx, button):
    """
    Handles the display of a user's order based on the order ID from the button ID.
    """

    # Retrieve emojis
    function_tick = self.bot.get_emoji(config.EMOJIS["function_tick"])
    log_memberleave = self.bot.get_emoji(config.EMOJIS["log_memberleave"])
    function_time = self.bot.get_emoji(config.EMOJIS["function_time"])
    log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])

    order_id = button.custom_id.split(":")[1]

    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/orders.json"

    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = json.load(file)

    # Find the order by order ID
    order_details = filedata.get(order_id)

    # Check if the order details exist
    if not order_details:
        # Attachments
        _, _, footer_file = await attachments()

        embed = discord.Embed(
            description=f"{log_memberjoin} - The order has already been **cancelled**.\n- Order ID: `{order_id}`",
            color=config.EMBED_COLOR
        )
        embed.set_image(url="attachment://reelab_banner_blue.png")
        await ctx.respond(embed=embed, file=footer_file, hidden=True)
        return

    # Check if the user is the creator of the order
    if str(order_details['user_id']) == str(ctx.author.id):
        # Attachments
        _, _, footer_file = await attachments()

        # Create and send the embed with order details
        embed = create_order_embed(order_id, order_details)
        await ctx.respond(embed=embed, file=footer_file, hidden=True)
    else:
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            # Attachments
            _, _, footer_file = await attachments()

            # creates a list of buttons to be sent
            buttons = [
                Button(
                    style=ButtonStyle.grey,
                    emoji=function_time,
                    label="Status update",
                    custom_id=f"status_update:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=log_memberleave,
                    label="Delete order",
                    custom_id=f"delete_order:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=function_tick,
                    label="Confirm Payment",
                    custom_id=f"confirm_payment:{order_id}",
                )
            ]

            # Create and send the embed with order details
            embed = create_order_embed(order_id, order_details)
            await ctx.respond(embed=embed, components=[buttons], file=footer_file, hidden=True)
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)

