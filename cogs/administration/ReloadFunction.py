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

from pathlib import Path

import discord
from discord import SlashCommandOption as Option, SlashCommandOptionChoice as Choice
from discord.ext import commands

import config


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

# log = logging.getLogger(__name__)


class ReloadFunction(commands.Cog):
    def __init__(self, reelab):
        self.bot = reelab

    # ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.slash_command(
        name="reload",
        description="Reloads a specified cog to refresh changes or fix issues.",
        default_required_permissions=discord.Permissions(administrator=True),
        guild_ids=[1216127716970070128],
        options=[
            Option(
                name="cog",
                description="Specify the cog module to reload, e.g., 'mycog'.",
                option_type=str,
                autocomplete=True
            ),
            Option(
                name='sync-commands',
                description='Set to True to update slash commands if changes were made.',
                option_type=bool,
                required=False
            )
        ],
        connector={'sync-commands': 'sync_slash_commands'}
    )
    async def reload(self, ctx, cog: str, sync_slash_commands: bool = False):
        """
        Reloads a specified cog to refresh changes or fix issues.

        Args:
            ctx (commands.Context): The context of the command invocation.
            cog (str): The name of the cog to reload.
            sync_slash_commands (bool, optional): Whether to sync slash commands after reloading. Defaults to False.
        """
        # Check if the user has permission to reload cogs
        if ctx.author.id in config.developer or ctx.author.id == 599204513722662933:
            # Temporarily set the bot's sync commands setting
            before = getattr(self.bot, 'sync_commands_on_cog_reload', False)
            self.bot.sync_commands_on_cog_reload = sync_slash_commands
            await ctx.defer(hidden=True)

            try:
                # Reload the specified cog
                cog_path = Path('./cogs').rglob(f'{cog}.py')
                for path in cog_path:
                    extension = str(path).replace('/', '.').replace('\\', '.')[:-3]
                    self.bot.reload_extension(extension)
                await ctx.respond(
                    f"The Cog `{cog}` has been successfully reloaded"
                    f"{' and the slash-commands synced.' if sync_slash_commands else '.'}",
                    hidden=True
                )
            except commands.ExtensionNotLoaded:
                await ctx.respond(f"There is no extension with the name `{cog}` loaded.", hidden=True)
            except Exception as e:
                await ctx.respond(f"An error occurred: {e}", hidden=True)
            finally:
                # Restore the bot's original sync commands setting
                self.bot.sync_commands_on_cog_reload = before
        else:
            await ctx.respond("You do not have permission to use this command.", hidden=True)

    @reload.autocomplete_callback
    async def reload_cog_autocomplete(self, i, cog: str = None, sync_slash_commands: bool = False):
        """
        Provides autocomplete suggestions for the cog name.

        Args:
            i (discord.Interaction): The interaction object for the autocomplete.
            cog (str, optional): The partial name of the cog being typed. Defaults to None.
        """
        # Get a list of all available cogs
        all_cogs = [p.stem for p in Path('./cogs').rglob('*.py') if p.stem != '__init__']
        # Send autocomplete choices that match the partial cog name
        await i.send_choices([Choice(name, name) for name in all_cogs if name.startswith(cog or '')])


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(ReloadFunction(reelab_bot))
