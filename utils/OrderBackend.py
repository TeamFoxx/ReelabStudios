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
    Formats the given value based on the key indicating the type of the value.

    Parameters:
    - key (str): The key indicating the type of the value (e.g., 'setup_fees', 'hosting_duration').
    - value: The value to be formatted.

    Returns:
    - str: The formatted value as a string.
    """

    # Check if the key indicates a price and format accordingly
    if key in ['setup_fees', 'total_price', 'user_amount_pricing']:
        # Format as a price with two decimal places and Euro sign
        return f"{value:.2f}€"

    # Check if the key indicates a hosting duration and format accordingly
    elif key == 'hosting_duration':
        # Add 'month' or 'months' based on the value
        return f"{value} month" if value == 1 else f"{value} months"

    # Return the value as is for other keys
    else:
        return value


def create_order_embed(order_id: str, details: dict) -> discord.Embed:
    """
    Creates a Discord embed for a single order, dynamically handling different product types
    and separating details into categories.

    Parameters:
    - order_id (str): The unique identifier for the order.
    - details (dict): The details of the order, including user information and product specifics.

    Returns:
    - discord.Embed: A Discord embed object with the order details formatted and categorized.
    """

    # Initialize the embed with the title "Order Details" and a color from the config
    embed = discord.Embed(title="Order Details", color=config.EMBED_COLOR)

    # Add fields for the basic order information
    embed.add_field(name="Order ID", value=f"```fix\n{order_id}\n```", inline=False)
    embed.add_field(name="User ID", value=f"```fix\n{details.get('user_id', 'N/A')}\n```", inline=True)
    embed.add_field(name="User Name", value=f"```fix\n{details.get('user_name', 'N/A')}\n```", inline=True)
    embed.add_field(name="Status", value=f"```fix\n{details.get('status', 'N/A')}\n```", inline=False)

    # Set the image for the embed using an attachment
    embed.set_image(url="attachment://reelab_banner_blue.png")

    # Define templates for different product types to display relevant details
    product_templates = {
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

    # Iterate over each product in the order details
    products = details.get('products', {})
    for product_name, sections in products.items():
        # Retrieve the product type separately
        product_type = products[product_name].get('type', 'N/A')
        # Add a field for the product name and type
        embed.add_field(name=f"{product_name.capitalize()} Details", value=f"- Type: `{product_type}`", inline=False)

        # Get the template for the current product
        template = product_templates.get(product_name, [])
        for section_name, keys in template:
            # Create content for each section of the template
            section_content = "\n".join(
                f"- {key.replace('_', ' ').capitalize()}: `{format_value(key, products[product_name].get(key))}`"
                for key in keys if key in products[product_name] and products[product_name][key]
            )
            # Only add the field if there is content to display
            if section_content.strip():
                embed.add_field(name=section_name, value=section_content, inline=False)

    # Set the footer of the embed
    embed.set_footer(text="For support and inquiries, please contact info@reelab.studio")

    return embed


async def my_order(self, ctx):
    """
    Retrieves and displays the orders for the invoking user in an embed format.

    Parameters:
    - self: The instance of the class.
    - ctx: The context of the command, providing information about the user and channel.

    Retrieves orders from a JSON file, filters them by the invoking user's ID,
    and displays them in an embed. If there are multiple orders, a select menu is presented.
    """

    # Retrieve emojis
    log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
    community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

    # Get the user ID of the invoking user
    user_id = str(ctx.author.id)

    # Define the path to the orders JSON file
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/orders.json"

    # Load the orders data from the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = json.load(file)

    # Filter orders by the invoking user's ID
    user_orders = {order_id: details for order_id, details in filedata.items() if
                   str(details['user_id']) == user_id}

    # Respond with a message if no orders are found
    if not user_orders:
        embed = discord.Embed(description=f"{log_memberjoin} You do not yet have any orders.",
                              color=config.EMBED_COLOR)
        embed.set_image(url="attachment://reelab_banner_blue.png")
        await ctx.respond(embed=embed, hidden=True)
        return

    # If only one order is found, directly display it
    if len(user_orders) == 1:
        # Attachments
        _, _, footer_file = await attachments()

        order_id, details = next(iter(user_orders.items()))
        embed = create_order_embed(order_id, details)
        await ctx.respond(embed=embed, file=footer_file, hidden=True)
        return

    # Create select menu options dynamically for multiple orders
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

    # Create the select menu with the order options
    select_menu = discord.SelectMenu(
        placeholder='Select other order',
        custom_id='orders_select',
        disabled=False,
        options=select_options[:25]  # Discord limits select menus to 25 options
    )

    # Create an action row for the select menu
    action_row = discord.ActionRow(select_menu)

    # Create an embed message prompting the user to select an order
    embed = discord.Embed(description=f"{log_memberjoin} Please select your order from the menu below:",
                          color=config.EMBED_COLOR)
    embed.set_image(url="attachment://reelab_banner_blue.png")

    # Attachments
    _, _, footer_file = await attachments()

    # Respond with the embed and the select menu
    await ctx.respond(embed=embed, file=footer_file, components=[action_row], hidden=True)


async def get_order(self, ctx, user_id: str):
    """
    Retrieves and displays the orders for a specified user in an embed format.

    Parameters:
    - self: The instance of the class.
    - ctx: The context of the command, providing information about the user and channel.
    - user_id: The ID of the user whose orders are to be retrieved.

    Retrieves orders from a JSON file, filters them by the specified user ID,
    and displays them in an embed. If there are multiple orders, a select menu is presented.
    """

    # Retrieve emojis
    log_memberjoin = self.bot.get_emoji(config.EMOJIS["log_memberjoin"])
    community_member = self.bot.get_emoji(config.EMOJIS["community_member"])

    # Define the path to the orders JSON file
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/orders.json"

    # Load the orders data from the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = json.load(file)

    # Filter orders by the specified user ID
    user_orders = {order_id: details for order_id, details in filedata.items() if
                   str(details['user_id']) == user_id}

    # Respond with a message if no orders are found
    if not user_orders:
        embed = discord.Embed(description=f"{log_memberjoin} No orders found for user ID {user_id}.",
                              color=config.EMBED_COLOR)
        embed.set_image(url="attachment://reelab_banner_blue.png")
        await ctx.respond(embed=embed, hidden=True)
        return

    # If only one order is found, directly display it
    if len(user_orders) == 1:
        # Attachments
        _, _, footer_file = await attachments()

        order_id, details = next(iter(user_orders.items()))
        embed = create_order_embed(order_id, details)
        await ctx.respond(embed=embed, file=footer_file, hidden=True)
        return

    # Create select menu options dynamically for multiple orders
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

    # Create the select menu with the order options
    select_menu = discord.SelectMenu(
        placeholder='Select other order',
        custom_id='orders_select',
        disabled=False,
        options=select_options[:25]  # Discord limits select menus to 25 options
    )

    # Create an action row for the select menu
    action_row = discord.ActionRow(select_menu)

    # Create an embed message prompting the user to select an order
    embed = discord.Embed(description=f"{log_memberjoin} Please select your order from the menu below:",
                          color=config.EMBED_COLOR)
    embed.set_image(url="attachment://reelab_banner_blue.png")

    # Attachments
    _, _, footer_file = await attachments()

    # Respond with the embed and the select menu
    await ctx.respond(embed=embed, file=footer_file, components=[action_row], hidden=True)


async def my_order_button(self, ctx, button):
    """
    Handles the display of a user's order based on the order ID from the button ID.
    """

    # Retrieve emojis
    function_tick = self.bot.get_emoji(config.EMOJIS["function_tick"])
    log_memberleave = self.bot.get_emoji(config.EMOJIS["log_memberleave"])
    function_time = self.bot.get_emoji(config.EMOJIS["function_time"])
    community_planner = self.bot.get_emoji(config.EMOJIS["community_planner"])
    function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

    # Extract the order ID from the button custom ID
    order_id = button.custom_id.split(":")[1]

    # Define the path to the orders JSON file
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/orders.json"

    # Load the orders data from the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = json.load(file)

    # Find the order by order ID
    order_details = filedata.get(order_id)

    # Check if the order details exist
    if not order_details:
        # Attachments
        _, _, footer_file = await attachments()

        # Create an embed message indicating the order has been cancelled
        embed = discord.Embed(
            description=f"{function_emergency} - The order has already been **cancelled**.\n- Order ID: `{order_id}`",
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
        # Check if the user has admin permissions
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            # Attachments
            _, _, footer_file = await attachments()

            # Create a list of admin action buttons
            buttons = [
                Button(
                    style=ButtonStyle.grey,
                    emoji=function_time,
                    label="Status update",
                    custom_id=f"status_update:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=community_planner,
                    label="Order update",
                    custom_id=f"order_update:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=log_memberleave,
                    label="Delete order",
                    custom_id=f"delete_order:{order_id}",
                ),
            ]

            # Create and send the embed with order details and admin action buttons
            embed = create_order_embed(order_id, order_details)
            await ctx.respond(embed=embed, components=[buttons], file=footer_file, hidden=True)
        else:
            # Respond with a permission error message
            await ctx.respond("You do not have permission to use this command.", hidden=True)


async def my_order_button_selectmenu(self, ctx):
    """
    Handles the display of a user's order based on the order ID from the button ID.
    """

    # Retrieve emojis
    log_memberleave = self.bot.get_emoji(config.EMOJIS["log_memberleave"])
    function_time = self.bot.get_emoji(config.EMOJIS["function_time"])
    community_planner = self.bot.get_emoji(config.EMOJIS["community_planner"])
    function_emergency = self.bot.get_emoji(config.EMOJIS["function_emergency"])

    # Extract the order ID from the button custom ID
    order_id = ctx.custom_id.split(":")[1]

    # Define the path to the orders JSON file
    script_directory = Path(__file__).resolve().parent.parent
    file_path = script_directory / "data/orders.json"

    # Load the orders data from the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        filedata = json.load(file)

    # Find the order by order ID
    order_details = filedata.get(order_id)

    # Check if the order details exist
    if not order_details:
        # Attachments
        _, _, footer_file = await attachments()

        # Create an embed message indicating the order has been cancelled
        embed = discord.Embed(
            description=f"{function_emergency} - The order has already been **cancelled**.\n- Order ID: `{order_id}`",
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
        # Check if the user has admin permissions
        if ctx.author.id in config.staff or ctx.author.id == 599204513722662933:
            # Attachments
            _, _, footer_file = await attachments()

            # Create a list of admin action buttons
            buttons = [
                Button(
                    style=ButtonStyle.grey,
                    emoji=function_time,
                    label="Status update",
                    custom_id=f"status_update:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=community_planner,
                    label="Order update",
                    custom_id=f"order_update:{order_id}",
                ),
                Button(
                    style=ButtonStyle.grey,
                    emoji=log_memberleave,
                    label="Delete order",
                    custom_id=f"delete_order:{order_id}",
                ),
            ]

            # Create and send the embed with order details and admin action buttons
            embed = create_order_embed(order_id, order_details)
            await ctx.edit(embed=embed, components=[buttons], attachments=[footer_file])
        else:
            # Respond with a permission error message
            await ctx.respond("You do not have permission to use this command.", hidden=True)
