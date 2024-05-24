# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# »› Developed by Foxx
# »› Copyright © 2024 Aurel Hoxha. All rights reserved.
# »› GitHub: https://github.com/TeamFoxx
# »› For support and inquiries, please contact info@aurelhoxha.de
# »› Use of this program is subject to the terms the terms of the MIT licence.
# »› A copy of the license can be found in the "LICENSE" file in the root directory of this project.
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#
# ⏤ { config } ⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤

# Version Configuration: Defines the current version of the bot
version = "v1.0"

# Access Control: Identifies the unique IDs for developers and staff members for privileged actions
developer = {599204513722662933}
staff = {599204513722662933, 549591994020659211}

# Localization: Specifies supported languages for multi-lingual support
supported_languages = "de, tr, fr, it, ja, zh, ko"

# Discord Channels: Stores Discord channel IDs where bot interactions occur
order_product_channel_id = 1216178294458814526

# Role Management: Defines IDs for various roles used in role-based features within the bot
official_staff_id = 1216137762537996479
reelab_role_id = 1217207299874230273
customer_support_id = 1216142380571295855

# Styling: Configures colors used in embeds throughout the bot's responses
EMBED_COLOR = 0x48689b  # primary color for embeds
HEADER_COLOR = 0x2b2d31  # color used for header sections in embeds

# Emoji Configuration: Defines custom emoji IDs for rich presence and interaction feedback
EMOJIS = {
    "community_owner": 1217203408516284516,
    "community_admin": 1217203398802280631,
    "community_artist": 1217203397409636362,
    "community_developer": 1217203400593117256,
    "community_advisor": 1217203395434385438,
    "community_member": 1217203405316030595,
    "community_manager": 1217203403709612073,
    "community_eventhost": 1217203402237280488,
    "community_planner": 1217203741279653968,
    "function_emergency": 1217203837295792129,
    "function_tick": 1217203424425152582,
    "function_cross": 1217203796065648691,
    "function_time": 1217203427361165403,
    "log_link": 1217203432906297414,
    "promo": 1231695279200272435,
    "log_timeoutremoved": 1217203449654018128,
    "log_rolesadd": 1217203440472555710,
    "log_membershipscreening": 1217203998659055797,
    "log_timeout": 1217203448005791795,
    "log_memberjoin": 1217203966450860093,
    "log_memberleave": 1217203436551016688,
    "plantbig_plant": 1217203467777474640,
    "plant_plant": 1217204087884611665,
    "role_star": 1217203475004526613
}

# Pricing Models: Detailed pricing configurations for various tiers of bot services
discord_bot_user_based_pricing_1 = 2  # Price for less than 1000 users
discord_bot_user_based_pricing_2 = 2.50  # Price for 1000-2499 users
discord_bot_user_based_pricing_3 = 3.00  # Price for 2500-4999 users
discord_bot_user_based_pricing_4 = 3.50  # Price for 5000 or more users

# Setup Fees: Specific charges for initial setup across different service durations
setup_fee_1_month = 5  # Fees for 1 month hosting.
setup_fee_3_month = 4  # Fees for 3 month hosting.
setup_fee_6_month = 2.50  # Fees for 6 month hosting.
setup_fee_12_month = 0  # Fees for 12 month hosting.

# Promotional Codes: Lists discounts available through promo codes
DISCOUNT_CODES = {
    'lifeservices_reelab': 5,  # 5% discount
    '0000': 0,  # No discount
    'newcomer': 20  # 20% discount
}
