# » Release date: March 2024
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Developed by Foxx
# »› Copyright © 2024 Aurel Hoxha. All rights reserved.
# »› GitHub: https://github.com/TeamFoxx
# »› For support and enquiries please contact hello@aurelhoxha.de
# »› Use of this program is subject to the terms of the MIT licence.
# »› A copy of the licence can be found in the file "LICENSE" in the root directory of this project.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { imports } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

from cogs import *

# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

reelab = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=commands.when_mentioned_or("."),
    sync_commands=True,
    auto_check_for_updates=True
)
reelab.remove_command("help")


# ⏤ { core } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

@reelab.event
async def on_ready():
    print(f"{Fore.GREEN}━━━ {Fore.WHITE}Ready Information {Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Logged in as {Fore.MAGENTA}{reelab.user}")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Developed with {Fore.RED}<3 {Fore.MAGENTA}by Foxx")
    print(f"{Fore.GREEN}»› {Fore.WHITE}For inquiries, reach out to {Fore.MAGENTA}hello@aurelhoxha.de")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Check out the code on {Fore.MAGENTA}GitHub: https://github.com/TeamFoxx")
    print(f"{Fore.GREEN}»› {Fore.WHITE}Join my {Fore.MAGENTA}Discord server: https://discord.gg/nQEwwyJ")

    activity = discord.Activity(name=f"www.reelab.studio", type=discord.ActivityType.watching)
    await reelab.change_presence(activity=activity)

_cogs = [p.stem for p in Path('./cogs').glob('*.py') if p.stem != '__init__']
[(reelab.load_extension(f'cogs.{ext}'), print(f'\033[32m{ext}\033[0m was loaded successfully')) for ext in _cogs]


# ⏤ { settings } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

reelab.run(my_secrets.key.token)
