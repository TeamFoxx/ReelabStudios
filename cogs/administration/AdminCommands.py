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
import logging
import os
from datetime import datetime

import discord
import psutil
from discord.ext import commands

import config
from utils.Utils import attachments


# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

class AdminCommands(commands.Cog):
    def __init__(self, reelab):
        self.bot: commands.Bot = reelab
        self.start_time = datetime.now()

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="restart",
        description="Restart the bot.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128]
    )
    async def restart_bot(self, ctx):
        """
        Handles the bot restart command. Only accessible by administrators.
        Logs the restart event, responds to the user, and restarts the bot.
        """
        # Get the user who issued the command
        user = ctx.author

        # Log the restart event with user ID
        logging.warning(f'{str(user.id)} - Performed a bot restart.')

        # Send a response to the user indicating that the bot is restarting
        await ctx.respond("The bot is restarting...", hidden=True)

        # Close the bot connection
        await self.bot.close()

        # Restart the bot by executing the main script
        os.system("python main.py")

    @commands.Cog.slash_command(
        name="metrics",
        description="Show the bot's metrics.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128]
    )
    async def show_metrics(self, ctx):
        """
        Handles the bot's metrics command. Displays the bot's performance metrics including latency,
        CPU usage, memory usage, disk usage, and uptime.
        """

        # Check Server - Bot latency
        latency = round(self.bot.latency * 1000)

        # Get CPU usage using psutil
        cpu_percent = psutil.cpu_percent()

        # Get memory usage
        mem_stats = psutil.virtual_memory()
        total_memory = mem_stats.total
        used_memory = mem_stats.used
        memory_usage = (used_memory / total_memory) * 100
        memory_total_gb = total_memory / (1024 ** 3)
        memory_used_gb = used_memory / (1024 ** 3)

        # Get disk usage
        disk_stats = psutil.disk_usage('/')
        total_disk = disk_stats.total
        used_disk = disk_stats.used
        disk_usage = (used_disk / total_disk) * 100
        disk_total_gb = total_disk / (1024 ** 3)
        disk_used_gb = used_disk / (1024 ** 3)

        # Get bot's specific resource usage
        bot_process = psutil.Process(os.getpid())
        bot_memory = bot_process.memory_info().rss
        bot_memory_mb = bot_memory / (1024 ** 2)

        # Calculate uptime
        now = datetime.now()
        uptime = now - self.start_time

        # Format uptime as days, hours, minutes, and seconds
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = ""
        if days:
            uptime_str += f"{days} day{'s' if days > 1 else ''}, "
        if hours:
            uptime_str += f"{hours} hour{'s' if hours > 1 else ''}, "
        if minutes:
            uptime_str += f"{minutes} minute{'s' if minutes > 1 else ''}, "
        uptime_str += f"{seconds} second{'s' if seconds != 1 else ''}"

        # Create an embed for metrics
        metrics_embed = discord.Embed(
            title="Bot Metrics",
            color=config.EMBED_COLOR
        )
        metrics_embed.add_field(name="Uptime", value=f"```fix\n{uptime_str}\n```", inline=False)
        metrics_embed.add_field(name="Bot Memory Usage", value=f"```fix\n{bot_memory_mb:.2f}MB\n```", inline=True)
        metrics_embed.add_field(name="Bot CPU Usage", value=f"```fix\n{cpu_percent:.2f}%\n```", inline=True)
        metrics_embed.add_field(name="Server Latency", value=f"```fix\n{latency}ms\n```", inline=True)
        metrics_embed.add_field(name="Memory Usage",
                                value=f"```fix\n{memory_usage:.2f}% ({memory_used_gb:.2f}GB/{memory_total_gb:.2f}GB)\n```",
                                inline=False)
        metrics_embed.add_field(name="Disk Usage",
                                value=f"```fix\n{disk_usage:.2f}% ({disk_used_gb:.2f}GB/{disk_total_gb:.2f}GB)\n```",
                                inline=False)
        metrics_embed.set_image(url="attachment://reelab_banner_blue.png")

        # Header message
        header = discord.Embed(
            title="Bot Metrics",
            color=config.EMBED_COLOR
        )
        header.set_image(url="attachment://bot_server_working_whitebackground.png")

        # Attachments
        _, _, footer_file = await attachments()

        bot_server_working_path = "./data/pictures/bot_server_working_whitebackground.png"
        bot_server_working_file = discord.File(bot_server_working_path,
                                               filename="bot_server_working_whitebackground.png")

        # Sending the metrics embed as a response
        await ctx.respond(embeds=[header, metrics_embed],
                          files=[bot_server_working_file, footer_file],
                          hidden=True)

    @commands.Cog.slash_command(
        name="info",
        description="Show general information about the bot.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128]
    )
    async def bot_info(self, ctx):
        """
        Handles the bot's info command. Displays general information about the bot and its configuration.
        """
        # Bot information
        bot_name = ctx.bot.user.name
        bot_id = ctx.bot.user.id

        # Bot information embed
        bot_embed = discord.Embed(
            title="Bot Information",
            color=config.EMBED_COLOR
        )
        bot_embed.add_field(name="Bot Version", value=f"```fix\n{config.version}\n```", inline=True)
        bot_embed.add_field(name="Name", value=f"```fix\n{bot_name}\n```", inline=True)
        bot_embed.add_field(name="ID", value=f"```fix\n{bot_id}\n```", inline=True)
        bot_embed.add_field(name="Supported Languages", value=f"```fix\n{config.supported_languages}\n```", inline=True)
        bot_embed.set_image(url="attachment://bot_server_working_transparent.png")

        # Config information embed
        config_embed = discord.Embed(
            title="Config",
            color=config.EMBED_COLOR
        )
        config_embed.add_field(name="EMBED_COLOR", value=f"```fix\n#{config.EMBED_COLOR:06x}\n```", inline=False)
        config_embed.add_field(name="HEADER_COLOR", value=f"```fix\n#{config.HEADER_COLOR:06x}\n```", inline=False)
        config_embed.add_field(name="Discord Bot User-Based Pricing",
                               value=f"```ini\n"
                                     f"Less than 1000 users: [{config.discord_bot_user_based_pricing_1}]\n"
                                     f"1000-2499 users: [{config.discord_bot_user_based_pricing_2}]\n"
                                     f"2500-4999 users: [{config.discord_bot_user_based_pricing_3}]\n"
                                     f"5000 or more users: [{config.discord_bot_user_based_pricing_4}]\n"
                                     f"```",
                               inline=False)
        config_embed.add_field(name="Setup Fees",
                               value=f"```ini\n"
                                     f"Setup Fee for 1 Month: [{config.setup_fee_1_month:.2f}€]\n"
                                     f"Setup Fee for 3 Months: [{config.setup_fee_3_month:.2f}€]\n"
                                     f"Setup Fee for 6 Months: [{config.setup_fee_6_month:.2f}€]\n"
                                     f"Setup Fee for 12 Months: [{config.setup_fee_12_month:.2f}€]\n"
                                     f"```",
                               inline=False)
        config_embed.add_field(name="Discount Codes", value=f"```fix\n{config.DISCOUNT_CODES}\n```", inline=False)
        config_embed.set_image(url="attachment://reelab_banner_blue.png")

        # Attachments
        banner_file, icon_file, footer_file = await attachments()

        bot_server_working_path = "./data/pictures/bot_server_working_transparent.png"
        bot_server_working_file = discord.File(bot_server_working_path, filename="bot_server_working_transparent.png")

        # Sending the embeds as a response
        await ctx.respond(embeds=[bot_embed, config_embed],
                          files=[footer_file, bot_server_working_file],
                          hidden=True)


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(AdminCommands(reelab_bot))
