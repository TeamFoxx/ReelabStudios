"""
All Rights Reserved © 2024 Aurel Hoxha

This code is proprietary and confidential. No part of this code may be reproduced, distributed, or transmitted
in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without
the prior written permission of the author, except in the case of brief quotations embodied in critical reviews and
certain other noncommercial uses permitted by copyright law.
"""

import my_secrets.key
import platform
from colorama import Fore, Style
import os
import io
import random
import asyncio
import time
import discord
import logging
import json
import traceback
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord import Modal, TextInput, Button, ButtonStyle, SelectMenu, SelectOption, SlashCommandOption as Option, Localizations,\
    SlashCommandOptionChoice as Choice
from discord.utils import get
from pathlib import Path