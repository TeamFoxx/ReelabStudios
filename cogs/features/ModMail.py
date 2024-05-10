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

import discord
from discord import Button, ButtonStyle
from discord.ext import commands

# ⏤ { configurations } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

name_visibility = {}


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.guild_id = 1216127716970070128
        self.mod_role_id = 1216137762537996479
        self.modmail_channel_id = 1216178727105462372

# ⏤ { codebase } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
            if message.guild:
                if message.channel.type not in [discord.ChannelType.public_thread, discord.ChannelType.private_thread]:
                    return
                if not message.channel.name.startswith("#"):
                    return
                channel_name_parts = message.channel.name.split(" | ")
                if not len(channel_name_parts) == 2:
                    return
                username = channel_name_parts[1]
                member = discord.utils.get(message.guild.members, name=username)
                if member:
                    if message.content.startswith('#'):
                        return
                    thread_id = message.channel.id
                    visibility = name_visibility.get(thread_id, "visible")
                    staff = message.author.name if visibility == "visible" else "Staff"
                    await member.send(f"{staff}: {message.content}")
                else:
                    thread_id = message.channel.id
                    channel = message.bot.get_channel(thread_id)
                    await channel.send(f"User not found!")
                return

            else:
                guild = self.bot.get_guild(self.guild_id)
                mod = guild.get_role(self.mod_role_id)
                channel = guild.get_channel(self.modmail_channel_id)

                user = message.author
                msg = message.content

                existing_threads = [t for t in channel.threads if t.name.endswith(f"| {user.name}")]
                if existing_threads:
                    thread = existing_threads[0]
                else:
                    existing_threads = [t for t in channel.threads if t.name.startswith("#") and t.archived]
                    counting = str(len(existing_threads)).zfill(4)

                    thread_name = f"#{counting} | {user.name}"
                    thread = await channel.create_thread(
                        name=thread_name,
                        reason="Modmail-Anfrage",
                        private=True,
                        invitable=True
                    )
                    await user.send(
                        "Your enquiry has been successfully forwarded to the team. Please wait for a reply.")

                    await thread.send(f"New Mail {mod.mention}")
                    thread_message = discord.Embed(
                        color=0x35417f,
                        description=f"## 📨 New Mail by {user.name}\n"
                                    f"- Use **#** in front of your messages for team information that you do not want to be sent to the user.\n"
                                    f"- To close the conversation and mail, click the button below. The user will not be able to post any more messages here. They will have to start a new thread.",
                    )
                    await thread.send(embed=thread_message,
                                      components=[[
                                          Button(
                                              style=ButtonStyle.grey,
                                              emoji="🔒",
                                              label="Close Mail",
                                              custom_id="close_mail",
                                          ),
                                          Button(
                                              style=ButtonStyle.grey,
                                              emoji="👁️",
                                              label="Toggle name visibility",
                                              custom_id="toggle_name_visibility",
                                          )
                                      ]]
                                      )

                await thread.send(f"**{user.name}:** {msg}")

        except Exception as e:
            print(f"Fehler beim Verarbeiten der Nachricht: {e}")

    @commands.Cog.on_click('^close_mail$')
    async def close_mail(self, ctx: discord.ComponentInteraction, button):
        thread = ctx.channel
        thread_name = thread.name
        new_thread_name = f"{thread_name} #closed"

        channel_name_parts = thread.name.split(" | ")
        if len(channel_name_parts) == 2:
            username = channel_name_parts[1]
            member = discord.utils.get(thread.guild.members, name=username)
            await member.send(
                "This ModMail conversation has just ended. Write again in this chat to open another mail.")

        response_message = discord.Embed(
            color=0x35417f,
            description="Thread is being closed and archived."
        )
        await ctx.respond(embed=response_message, hidden=True)

        for member in thread.members:
            await thread.remove_member(member)

        await thread.edit(name=new_thread_name)

        await thread.edit(archived=True)

        thread_id = thread.id
        if thread_id in name_visibility:
            del name_visibility[thread_id]

    @commands.Cog.on_click('^toggle_name_visibility$')
    async def toggle_name_visibility(self, ctx: discord.ComponentInteraction, button):
        thread_id = ctx.message.channel.id
        visibility = name_visibility.get(thread_id, "visible")

        if visibility == "visible":
            name_visibility[thread_id] = "not_visible"
            thread_message = discord.Embed(
                color=0x35417f,
                description=f"Staff visibility changed to **not visible**"
            )

        else:
            name_visibility[thread_id] = "visible"
            thread_message = discord.Embed(
                color=0x35417f,
                description=f"Staff visibility changed to **visible**"
            )

        await ctx.respond(embed=thread_message, hidden=True)


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

def setup(reelab_bot):
    reelab_bot.add_cog(ModMail(reelab_bot))
