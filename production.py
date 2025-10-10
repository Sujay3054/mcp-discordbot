import os
import aiohttp
import logging
from typing import Optional, List, Dict
from mcp.server.fastmcp import FastMCP
import urllib.parse
# ---------- CONFIG ----------
# Securely loading the token from an environment variable
DISCORD_BOT_TOKEN = "MTQyNTM2OTgyNDQ2NDIwNzg5Mg.GuHH9o.Z6in6WZ9uiEgAG2fUt6vVOzV3Y5h1hwsMotmjM"
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORDBOT_TOKEN environment variable not set.")

DISCORD_API_BASE = "https://discord.com/api/v10"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("discordbot_mcp")

mcp = FastMCP("discordbot-mcp")

# ---------- HELPER ----------
async def discord_request(method: str, endpoint: str, json: Optional[Dict] = None):
    """
    Generic helper to make Discord REST API requests.
    """
    url = f"{DISCORD_API_BASE}{endpoint}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=json, headers=headers) as resp:
            # ...
            if resp.status in [200, 201]:
                return await resp.json()
            elif resp.status == 204:
                return {"status": "success", "detail": "Action completed successfully."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

# ---------- TOOL DEFINITIONS ----------
# Emoji started 
@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_EMOJI(
    guild_id: str,
    name: str,
    image: str,
    roles: Optional[List[str]] = None
) -> Dict:
    """
    Create a new custom emoji in a specified Discord guild.

    Args:
        guild_id: The ID of the Discord guild (server).
        name: The emoji name (2–32 chars, alphanumeric or underscores).
        image: Base64 encoded image data (PNG or GIF), e.g. 'data:image/png;base64,...'.
        roles: Optional list of role IDs allowed to use this emoji.

    Returns:
        A dictionary with the created emoji data.
    """
    payload = {"name": name, "image": image}
    if roles:
        payload["roles"] = roles

    endpoint = f"/guilds/{guild_id}/emojis"
    return await discord_request("POST", endpoint, json=payload)


@mcp.tool()
async def DISCORDBOT_GET_GUILD_EMOJI(guild_id: str, emoji_id: str):
    """
    Retrieves a specific custom emoji from a Discord guild.
    Args:
        guild_id: The Discord guild (server) ID.
        emoji_id: The ID of the emoji to fetch.
    Returns:
        A dictionary containing emoji details.
    """
    endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_EMOJI(
    guild_id: str,
    emoji_id: str,
    name: Optional[str] = None,
    roles: Optional[List[str]] = None
):
    """
    Update a guild emoji's name and/or roles.
    Args:
        guild_id: The Discord guild (server) ID.
        emoji_id: The ID of the emoji to update.
        name: Optional new name for the emoji (2-32 chars).
        roles: Optional list of role IDs allowed to use the emoji. 
               Empty list makes it available to everyone. 
               If None, roles remain unchanged.
    Returns:
        A dictionary with the updated emoji data.
    """
    payload = {}
    if name is not None:
        payload["name"] = name
    if roles is not None:
        payload["roles"] = roles

    endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"
    return await discord_request("PATCH", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_EMOJI(guild_id: str, emoji_id: str):
    """
    Deletes a custom emoji from a Discord guild.
    Args:
        guild_id: The Discord guild (server) ID.
        emoji_id: The ID of the emoji to delete.
    Returns:
        A dictionary indicating success or error.
    """
    endpoint = f"/guilds/{guild_id}/emojis/{emoji_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_EMOJIS(guild_id: str):
    """
    Retrieves all custom emojis for a specified Discord guild.
    Args:
        guild_id: The Discord guild (server) ID.
    Returns:
        A dictionary containing a list of emojis and their details.
    """
    endpoint = f"/guilds/{guild_id}/emojis"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_STICKER(
    guild_id: str,
    name: str = None,
    description: str = None,
    tags: str = None,
    file: str = None
):
    """
    Creates a new sticker in a specified Discord guild.

    Args:
        guild_id: ID of the guild.
        name: Name of the sticker (2-30 characters).
        description: Description of the sticker (2-100 characters).
        tags: Autocomplete tags (comma-separated, max 200 chars).
        file: Sticker file path (PNG, APNG, Lottie JSON; max 512KB; 320x320px recommended).

    Returns:
        dict containing:
            - data: newly created sticker object
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/guilds/{guild_id}/stickers"
    payload = {}

    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if tags:
        payload["tags"] = tags

    files = {"file": open(file, "rb")} if file else None

    return await discord_request("POST", endpoint, json=payload if not files else None, files=files)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_STICKER(
    guild_id: str,
    sticker_id: str
):
    """
    Retrieves a Discord sticker from a specified guild.

    Args:
        guild_id: The ID of the guild (server) where the sticker exists.
        sticker_id: The ID of the sticker to retrieve.

    Returns:
        dict containing:
            - data: the retrieved sticker object
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"
    
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_STICKER(
    guild_id: str,
    sticker_id: str,
    name: str = None,
    description: str = None,
    tags: str = None
):
    """
    Updates a sticker in a specified Discord guild. Supports partial updates.

    Args:
        guild_id: ID of the guild where the sticker exists.
        sticker_id: ID of the sticker to update.
        name: New name of the sticker (2-30 characters).
        description: New description of the sticker (2-100 characters).
        tags: New autocomplete tags (comma-separated, max 200 chars).

    Returns:
        dict containing:
            - data: updated sticker object
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"
    payload = {}

    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if tags:
        payload["tags"] = tags

    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_STICKER(
    guild_id: str,
    sticker_id: str
):
    """
    Deletes a sticker from a specified Discord guild.

    Args:
        guild_id: ID of the guild where the sticker exists.
        sticker_id: ID of the sticker to delete.

    Returns:
        dict containing:
            - data: typically empty on successful deletion
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/guilds/{guild_id}/stickers/{sticker_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_STICKERS(
    guild_id: str
):
    """
    Retrieves a list of all custom stickers in the specified Discord guild.

    Args:
        guild_id: ID of the Discord guild.

    Returns:
        dict containing:
            - data: list of sticker objects
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/guilds/{guild_id}/stickers"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_STICKER_PACKS():
    """
    Lists all standard sticker packs available to Nitro subscribers.
    
    Returns:
        dict containing:
            - data: an object with a list of sticker packs and their stickers
            - successful: bool
            - error: error message if any
    """
    endpoint = "/sticker-packs"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_STICKER(sticker_id: str):
    """
    Retrieves a specific Discord sticker by its ID.

    Args:
        sticker_id: The unique ID of the sticker to retrieve.

    Returns:
        dict containing:
            - data: a dictionary representing the sticker object
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/stickers/{sticker_id}"
    return await discord_request("GET", endpoint)
#emoji ended 

#utility started
@mcp.tool()
async def DISCORDBOT_FOLLOW_CHANNEL(channel_id: str, webhook_channel_id: str):
    """
    Follows an Announcement Channel and posts its messages to another channel via a webhook.

    Args:
        channel_id: ID of the Announcement Channel to follow (source channel).
        webhook_channel_id: ID of the channel where messages will be posted (destination channel).

    Returns:
        dict containing:
            - data: dict with 'channel_id' (source) and 'webhook_id' (created webhook)
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/channels/{channel_id}/followers"
    payload = {"webhook_channel_id": webhook_channel_id}
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_TRIGGER_TYPING_INDICATOR(channel_id: str):
    """
    Triggers the typing indicator in a specified Discord channel.

    Args:
        channel_id: ID of the Discord channel where the typing indicator should appear.

    Returns:
        dict containing:
            - data: empty dict (operation returns 204 on success)
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/channels/{channel_id}/typing"
    return await discord_request("POST", endpoint)

@mcp.tool()
async def DISCORDBOT_CROSSPOST_MESSAGE(channel_id: str, message_id: str):
    """
    Crossposts a message from an announcement (news) channel.

    Args:
        channel_id: ID of the announcement channel containing the message.
        message_id: ID of the message to be crossposted.

    Returns:
        dict containing:
            - data: the crossposted message object (or empty dict)
            - successful: bool
            - error: error message if any
    """
    endpoint = f"/channels/{channel_id}/messages/{message_id}/crosspost"
    return await discord_request("POST", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_VOICE_REGIONS():
    """
    Lists all available voice regions in Discord.

    Returns:
        dict containing:
            - data: list of voice region objects with properties id, name, custom, deprecated, optimal
            - successful: bool
            - error: str if any error occurred
    """
    endpoint = "/voice/regions"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_DM(recipient_id: str = None, access_tokens: list = None, nicks: dict = None):
    """
    Creates a DM channel with a single user or a group DM.

    Parameters:
        recipient_id (str, optional): The User ID for a 1-on-1 DM. Use this OR `access_tokens`.
        access_tokens (list, optional): OAuth2 tokens for multiple users in a group DM (1–9 others). Use this OR `recipient_id`.
        nicks (dict, optional): Custom nicknames for group DM users. Only used with `access_tokens`.

    Returns:
        dict: Contains 'data' (DM channel object), 'successful' (bool), 'error' (str if any)
    """
    payload = {}
    if recipient_id:
        payload["recipient_id"] = recipient_id
    if access_tokens:
        payload["access_tokens"] = access_tokens
    if nicks:
        payload["nicks"] = nicks

    endpoint = "/users/@me/channels"
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_CREATE_GROUP_DM_USER(channel_id: str, user_id: str):
    """
    Removes a user from a Discord group DM channel.

    Parameters:
        channel_id (str): The ID of the group DM channel.
        user_id (str): The ID of the user to remove.

    Returns:
        dict: Contains 'data' (usually empty), 'successful' (bool), 'error' (str if any)
    """
    endpoint = f"/channels/{channel_id}/recipients/{user_id}"
    return await discord_request("DELETE", endpoint)
#emoji ended
#*****************************************************************************************
# Guild (Server) Management Tools started
@mcp.tool()
async def DISCORDBOT_CREATE_GUILD(
    name: str,
    **kwargs
):
    """Creates a new Discord guild (server).

    NOTE: Unverified bots are limited to 10 guilds. Use this tool sparingly.

    Args:
        name (str): The name of the new guild (2-100 characters).
        **kwargs: Any other optional parameters from the Discord API documentation,
                  such as 'icon', 'roles', or 'channels'. These should be
                  provided as keyword arguments.
    """
    endpoint = "/guilds"
    
    # Start with the required name
    payload = {
        "name": name,
    }
    # Add all other optional parameters provided by the user
    payload.update(kwargs)
        
    return await discord_request("POST", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD(guild_id: str):
    """
    Deletes a guild permanently. 

    WARNING: This is an irreversible action. The bot MUST be the owner of the 
    guild to perform this operation.

    Args:
        guild_id: The ID of the guild (server) to be deleted.
    """
    endpoint = f"/guilds/{guild_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD(
    guild_id: str,
    **kwargs
):
    """
    Updates a guild's settings.

    The bot must have the 'Manage Server' permission in the guild.

    Args:
        guild_id (str): The ID of the guild (server) to update.
        **kwargs: Any other optional parameters from the Discord API documentation,
                  such as 'name', 'description', 'icon', etc. These should be
                  provided as keyword arguments.
    """
    if not kwargs:
        raise ValueError("At least one setting (e.g., name, description) must be provided to update.")

    endpoint = f"/guilds/{guild_id}"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("PATCH", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD(
    guild_id: str,
    with_counts: Optional[bool] = None
):
    """
    Retrieves detailed information about a specific guild (server).

    The bot must be a member of the guild to retrieve its information.

    Args:
        guild_id (str): The ID of the guild to retrieve.
        with_counts (Optional[bool]): When true, includes approximate member 
                                      and presence counts.
    """
    endpoint = f"/guilds/{guild_id}"
    
    # Add the with_counts parameter to the URL if requested
    if with_counts:
        endpoint += "?with_counts=true"
        
    return await discord_request("GET", endpoint)


@mcp.tool()
async def DISCORDBOT_LIST_GUILD_CHANNELS(guild_id: str):
    """
    Retrieves a list of all channels in a specific guild (server).

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild to retrieve channels from.
    """
    endpoint = f"/guilds/{guild_id}/channels"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_MEMBERS(
    guild_id: str,
    limit: Optional[int] = None,
    after: Optional[str] = None
):
    """
    Retrieves a list of members from a specific guild (server).

    NOTE: Requires the privileged 'Server Members Intent' to be enabled for your
    bot in the Discord Developer Portal.

    Args:
        guild_id (str): The ID of the guild to retrieve members from.
        limit (Optional[int]): Max number of members to return (1-1000).
        after (Optional[str]): The user ID to start fetching members after.
    """
    endpoint = f"/guilds/{guild_id}/members"
    
    params = {}
    if limit is not None:
        params["limit"] = limit
    if after is not None:
        params["after"] = after
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_MEMBER(
    guild_id: str,
    user_id: str
):
    """
    Retrieves information about a specific member of a guild.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild.
        user_id (str): The ID of the user to retrieve.
    """
    endpoint = f"/guilds/{guild_id}/members/{user_id}"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_MEMBER(
    guild_id: str,
    user_id: str,
    **kwargs
):
    """
    Updates attributes of a specific guild member.

    Requires different permissions based on the action:
    - nick: MANAGE_NICKNAMES
    - roles: MANAGE_ROLES
    - mute: MUTE_MEMBERS
    - deaf: DEAFEN_MEMBERS
    - channel_id (moving): MOVE_MEMBERS
    - communication_disabled_until (timeout): MODERATE_MEMBERS

    Args:
        guild_id (str): The ID of the guild.
        user_id (str): The ID of the user to update.
        **kwargs: Fields to update, e.g., nick="NewNick", roles=["role_id_1"].
    """
    if not kwargs:
        raise ValueError("At least one attribute to update must be provided.")

    endpoint = f"/guilds/{guild_id}/members/{user_id}"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("PATCH", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_MEMBER(
    guild_id: str,
    user_id: str
):
    """
    Removes (kicks) a member from a guild.

    The bot must have the 'Kick Members' permission.

    Args:
        guild_id (str): The ID of the guild.
        user_id (str): The ID of the user to remove.
    """
    endpoint = f"/guilds/{guild_id}/members/{user_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_BAN_USER_FROM_GUILD(
    guild_id: str,
    user_id: str,
    delete_message_days: Optional[int] = None,
    delete_message_seconds: Optional[int] = None
):
    """
    Bans a user from a guild and optionally deletes their recent messages.

    The bot must have the 'Ban Members' permission. You can specify a message
    deletion period in days (0-7) or seconds, but not both.

    Args:
        guild_id (str): The ID of the guild to ban the user from.
        user_id (str): The ID of the user to ban.
        delete_message_days (Optional[int]): Number of days of messages to delete.
        delete_message_seconds (Optional[int]): Number of seconds of messages to delete.
    """
    endpoint = f"/guilds/{guild_id}/bans/{user_id}"
    
    payload = {}
    # The API accepts either days or seconds, but not both.
    # We will prioritize the more modern 'seconds' parameter.
    if delete_message_seconds is not None:
        payload["delete_message_seconds"] = delete_message_seconds
    elif delete_message_days is not None:
        payload["delete_message_days"] = delete_message_days
        
    return await discord_request("PUT", endpoint, data=payload)
    
@mcp.tool()
async def DISCORDBOT_UNBAN_USER_FROM_GUILD(
    guild_id: str,
    user_id: str
):
    """
    Removes a ban for a user from a guild.

    The bot must have the 'Ban Members' permission.

    Args:
        guild_id (str): The ID of the guild.
        user_id (str): The ID of the user to unban.
    """
    endpoint = f"/guilds/{guild_id}/bans/{user_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_BANS(
    guild_id: str,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None
):
    """
    Retrieves a list of banned users from a specific guild (server).

    NOTE: Requires the 'Ban Members' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve bans from.
        limit (Optional[int]): Max number of bans to return (1-1000).
        before (Optional[str]): The user ID to get bans before.
        after (Optional[str]): The user ID to get bans after.
    """
    endpoint = f"/guilds/{guild_id}/bans"
    
    params = {}
    if limit is not None:
        params["limit"] = limit
    if before is not None:
        params["before"] = before
    if after is not None:
        params["after"] = after
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_BAN(
    guild_id: str,
    user_id: str
):
    """
    Retrieves the ban information for a specific user in a guild.

    NOTE: Requires the 'Ban Members' permission.

    Args:
        guild_id (str): The ID of the guild.
        user_id (str): The ID of the user to check for a ban.
    """
    endpoint = f"/guilds/{guild_id}/bans/{user_id}"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_PRUNE_GUILD(
    guild_id: str,
    days: Optional[int] = None,
    compute_prune_count: Optional[bool] = None,
    include_roles: Optional[List[str]] = None
):
    """
    Kicks inactive members from a guild (server).

    NOTE: Requires the 'Kick Members' permission.

    Args:
        guild_id (str): The ID of the guild to prune.
        days (Optional[int]): Number of inactivity days before pruning (1-30).
        compute_prune_count (Optional[bool]): If true, returns the number of members
                                           that would be pruned without actually
                                           kicking them.
        include_roles (Optional[List[str]]): List of role IDs to restrict pruning to.
    """
    endpoint = f"/guilds/{guild_id}/prune"
    
    payload = {}
    if days is not None:
        payload["days"] = days
    if compute_prune_count is not None:
        payload["compute_prune_count"] = compute_prune_count
    if include_roles is not None:
        payload["include_roles"] = include_roles
        
    return await discord_request("POST", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_PREVIEW_PRUNE_GUILD(
    guild_id: str,
    days: Optional[int] = None,
    include_roles: Optional[List[str]] = None
):
    """
    Previews the number of members that would be pruned from a guild.

    NOTE: Requires the 'Kick Members' permission. This does not kick anyone.

    Args:
        guild_id (str): The ID of the guild to preview the prune for.
        days (Optional[int]): Number of inactivity days to check (1-30).
        include_roles (Optional[List[str]]): List of role IDs to restrict the count to.
    """
    endpoint = f"/guilds/{guild_id}/prune"
    
    params = {}
    if days is not None:
        params["days"] = days
    if include_roles is not None:
        # The API expects multiple roles to be passed as separate query params
        # e.g., ?include_roles=id1&include_roles=id2
        # aiohttp's ClientSession handles this automatically if we pass a list
        params["include_roles"] = include_roles
        
    if params:
        query_string = urllib.parse.urlencode(params, doseq=True)
        endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_ROLES(guild_id: str):
    """
    Retrieves a list of all roles in a specific guild (server).

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild to retrieve roles from.
    """
    endpoint = f"/guilds/{guild_id}/roles"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_ROLE(
    guild_id: str,
    **kwargs
):
    """
    Creates a new role in a guild.

    NOTE: Requires the 'Manage Roles' permission.

    Args:
        guild_id (str): The ID of the guild to create the role in.
        **kwargs: Optional parameters for the role, such as 'name', 'permissions',
                  'color', 'hoist', etc.
    """
    endpoint = f"/guilds/{guild_id}/roles"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("POST", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_ROLE(
    guild_id: str,
    role_id: str,
    **kwargs
):
    """
    Updates an existing role in a guild.

    NOTE: Requires the 'Manage Roles' permission. The bot's highest role must
    be above the role being modified.

    Args:
        guild_id (str): The ID of the guild where the role exists.
        role_id (str): The ID of the role to update.
        **kwargs: Optional parameters for the role to update, such as 'name', 
                  'permissions', 'color', etc.
    """
    if not kwargs:
        raise ValueError("At least one attribute to update (e.g., name, color) must be provided.")

    endpoint = f"/guilds/{guild_id}/roles/{role_id}"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("PATCH", endpoint, data=payload)

@mcp.tool()
async def DISCORDBOT_SEARCH_GUILD_MEMBERS(
    guild_id: str,
    query: str,
    limit: Optional[int] = 1
):
    """
    Searches for members in a guild whose username or nickname starts with a query.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild to search in.
        query (str): The string to search for at the beginning of usernames/nicknames.
        limit (Optional[int]): The maximum number of members to return (1-1000).
    """
    endpoint = f"/guilds/{guild_id}/members/search"
    
    params = {
        "query": query,
        "limit": limit
    }
        
    query_string = urllib.parse.urlencode(params)
    endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LEAVE_GUILD(guild_id: str):
    """
    Makes the bot leave a guild (server).

    Args:
        guild_id (str): The ID of the guild for the bot to leave.
    """
    endpoint = f"/users/@me/guilds/{guild_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_INVITES(guild_id: str):
    """
    Retrieves a list of all active invite links for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve invites from.
    """
    endpoint = f"/guilds/{guild_id}/invites"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_FROM_TEMPLATE(
    code: str,
    name: str,
    icon: Optional[str] = None
):
    """
    Creates a new guild from a guild template.

    NOTE: Unverified bots are limited to being in 10 guilds.

    Args:
        code (str): The code for the guild template.
        name (str): The name for the new guild (2-100 characters).
        icon (Optional[str]): A Base64 encoded 128x128 image for the guild icon.
    """
    endpoint = f"/guilds/templates/{code}"
    
    payload = {
        "name": name
    }
    if icon:
        payload["icon"] = icon
        
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_SYNC_GUILD_TEMPLATE(
    guild_id: str,
    code: str
):
    """
    Synchronizes a guild template with its source guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the source guild.
        code (str): The code of the template to sync.
    """
    endpoint = f"/guilds/{guild_id}/templates/{code}"
    return await discord_request("PUT", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_TEMPLATE(code: str):
    """
    Retrieves information about a guild template.

    Args:
        code (str): The unique code of the guild template.
    """
    endpoint = f"/guilds/templates/{code}"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_TEMPLATE(
    guild_id: str,
    code: str,
    name: Optional[str] = None,
    description: Optional[str] = None
):
    """
    Updates a guild template's metadata (name and/or description).

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild where the template exists.
        code (str): The code of the template to update.
        name (Optional[str]): The new name for the template.
        description (Optional[str]): The new description for the template.
    """
    if name is None and description is None:
        raise ValueError("At least one attribute (name or description) must be provided.")

    endpoint = f"/guilds/{guild_id}/templates/{code}"
    
    payload = {}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_TEMPLATE(
    guild_id: str,
    code: str
):
    """
    Deletes a guild template.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild where the template exists.
        code (str): The code of the template to delete.
    """
    endpoint = f"/guilds/{guild_id}/templates/{code}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_TEMPLATE(
    guild_id: str,
    name: str,
    description: Optional[str] = None
):
    """
    Creates a new guild template from an existing guild's structure.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to create the template from.
        name (str): The name for the new template (1-100 characters).
        description (Optional[str]): The description for the template (0-120 characters).
    """
    endpoint = f"/guilds/{guild_id}/templates"
    
    payload = {
        "name": name,
    }
    if description is not None:
        payload["description"] = description
        
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_PREVIEW(guild_id: str):
    """
    Retrieves a public preview of a guild.

    The bot does not need to be a member of the guild for this to work,
    but the guild must be discoverable.

    Args:
        guild_id (str): The ID of the guild to preview.
    """
    endpoint = f"/guilds/{guild_id}/preview"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILDS_ONBOARDING(guild_id: str):
    """
    Retrieves the onboarding configuration for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve the onboarding settings from.
    """
    endpoint = f"/guilds/{guild_id}/onboarding"
    return await discord_request("GET", endpoint)
    
@mcp.tool()
async def DISCORDBOT_PUT_GUILDS_ONBOARDING(
    guild_id: str,
    prompts: List[Dict],
    default_channel_ids: List[str],
    enabled: bool,
    mode: int = 0
):
    """
    Updates a guild's onboarding configuration. Replaces the entire configuration.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to update.
        prompts (List[Dict]): The list of onboarding prompt objects.
        default_channel_ids (List[str]): The list of default channel IDs.
        enabled (bool): Whether onboarding is enabled.
        mode (int): The onboarding mode (must be 0 for now).
    """
    endpoint = f"/guilds/{guild_id}/onboarding"
    
    payload = {
        "prompts": prompts,
        "default_channel_ids": default_channel_ids,
        "enabled": enabled,
        "mode": mode
    }
        
    return await discord_request("PUT", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_WIDGET(guild_id: str):
    """
    Retrieves the widget object for a given guild.

    NOTE: The guild widget must be enabled in Server Settings for this to work.

    Args:
        guild_id (str): The ID of the guild to retrieve the widget for.
    """
    endpoint = f"/guilds/{guild_id}/widget.json"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_WIDGET_SETTINGS(guild_id: str):
    """
    Retrieves the widget settings for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to get widget settings for.
    """
    endpoint = f"/guilds/{guild_id}/widget"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_WIDGET_SETTINGS(
    guild_id: str,
    enabled: Optional[bool] = None,
    channel_id: Optional[str] = None
):
    """
    Updates the widget settings for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to update the widget settings for.
        enabled (Optional[bool]): Whether the widget is enabled.
        channel_id (Optional[str]): The ID of the widget channel.
    """
    if enabled is None and channel_id is None:
        raise ValueError("At least one setting (enabled or channel_id) must be provided.")

    endpoint = f"/guilds/{guild_id}/widget"
    
    payload = {}
    if enabled is not None:
        payload["enabled"] = enabled
    if channel_id is not None:
        payload["channel_id"] = channel_id
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_WELCOME_SCREEN(guild_id: str):
    """
    Retrieves the welcome screen configuration for a guild.

    NOTE: Requires the 'Manage Server' permission. The guild must also
    have the Welcome Screen feature enabled.

    Args:
        guild_id (str): The ID of the guild to retrieve the welcome screen from.
    """
    endpoint = f"/guilds/{guild_id}/welcome-screen"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_WELCOME_SCREEN(
    guild_id: str,
    enabled: Optional[bool] = None,
    welcome_channels: Optional[List[Dict]] = None,
    description: Optional[str] = None
):
    """
    Updates the welcome screen for a guild.

    NOTE: Requires the 'Manage Server' permission. The guild must have the
    Welcome Screen feature enabled (be a Community server).

    Args:
        guild_id (str): The ID of the guild to update the welcome screen for.
        enabled (Optional[bool]): Whether the welcome screen is enabled.
        welcome_channels (Optional[List[Dict]]): Array of welcome channel objects.
        description (Optional[str]): The server description shown in the welcome screen.
    """
    if enabled is None and welcome_channels is None and description is None:
        raise ValueError("At least one field (enabled, welcome_channels, or description) must be provided.")

    endpoint = f"/guilds/{guild_id}/welcome-screen"
    
    payload = {}
    if enabled is not None:
        payload["enabled"] = enabled
    if welcome_channels is not None:
        payload["welcome_channels"] = welcome_channels
    if description is not None:
        payload["description"] = description
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_VANITY_URL(guild_id: str):
    """
    Retrieves the vanity URL information for a specific guild.

    NOTE: Requires the 'Manage Server' permission. The guild must have a
    vanity URL set (usually through Server Boosting).

    Args:
        guild_id (str): The ID of the guild to retrieve the vanity URL from.
    """
    endpoint = f"/guilds/{guild_id}/vanity-url"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_WEBHOOKS(guild_id: str):
    """
    Retrieves a list of all webhooks in a specific guild.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve webhooks from.
    """
    endpoint = f"/guilds/{guild_id}/webhooks"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_SCHEDULED_EVENT(
    guild_id: str,
    guild_scheduled_event_id: str,
    with_user_count: Optional[bool] = None
):
    """
    Retrieves a specific scheduled event from a guild.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild where the event exists.
        guild_scheduled_event_id (str): The ID of the scheduled event to retrieve.
        with_user_count (Optional[bool]): If true, includes the number of subscribed users.
    """
    endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
    
    if with_user_count:
        endpoint += "?with_user_count=true"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_GUILD_SCHEDULED_EVENT(
    guild_id: str,
    **kwargs
):
    """
    Creates a new scheduled event in a guild.

    NOTE: Requires the 'Manage Events' permission. Depending on the event
    type, other permissions like 'Manage Channels' may be needed.

    Args:
        guild_id (str): The ID of the guild to create the event in.
        **kwargs: The event data. You MUST provide 'name', 'privacy_level',
                  'scheduled_start_time', and 'entity_type'. Refer to the
                  Discord API documentation for the full object structure.
    """
    required_keys = ["name", "privacy_level", "scheduled_start_time", "entity_type"]
    if not all(key in kwargs for key in required_keys):
        raise ValueError(f"Missing one of the required arguments: {required_keys}")

    endpoint = f"/guilds/{guild_id}/scheduled-events"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_SCHEDULED_EVENT(
    guild_id: str,
    guild_scheduled_event_id: str,
    **kwargs
):
    """
    Updates a guild's scheduled event.

    NOTE: Requires the 'Manage Events' permission.

    Args:
        guild_id (str): The ID of the guild where the event exists.
        guild_scheduled_event_id (str): The ID of the event to update.
        **kwargs: Fields to update, e.g., name="New Event Name",
                  description="Updated info.", status=2 (to start).
    """
    if not kwargs:
        raise ValueError("At least one attribute to update (e.g., name, status) must be provided.")

    endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_SCHEDULED_EVENT(
    guild_id: str,
    guild_scheduled_event_id: str
):
    """
    Deletes a scheduled event from a guild.

    NOTE: Requires the 'Manage Events' permission.

    Args:
        guild_id (str): The ID of the guild where the event exists.
        guild_scheduled_event_id (str): The ID of the event to delete.
    """
    endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_SCHEDULED_EVENTS(
    guild_id: str,
    with_user_count: Optional[bool] = None
):
    """
    Retrieves a list of all scheduled events for a specific guild.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild to retrieve events from.
        with_user_count (Optional[bool]): If true, includes the number of subscribed users for each event.
    """
    endpoint = f"/guilds/{guild_id}/scheduled-events"
    
    if with_user_count:
        endpoint += "?with_user_count=true"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_SCHEDULED_EVENT_USERS(
    guild_id: str,
    guild_scheduled_event_id: str,
    limit: Optional[int] = None,
    before: Optional[str] = None,
    after: Optional[str] = None,
    with_member: Optional[bool] = None
):
    """
    Retrieves a list of users subscribed to a specific scheduled event.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild.
        guild_scheduled_event_id (str): The ID of the scheduled event.
        limit (Optional[int]): Max number of users to return (1-100).
        before (Optional[str]): The user ID to get users before.
        after (Optional[str]): The user ID to get users after.
        with_member (Optional[bool]): If true, includes the full guild member object for each user.
    """
    endpoint = f"/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users"
    
    params = {}
    if limit is not None:
        params["limit"] = limit
    if before is not None:
        params["before"] = before
    if after is not None:
        params["after"] = after
    if with_member is not None:
        params["with_member"] = with_member
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_VOICE_REGIONS(guild_id: str):
    """
    Retrieves a list of available voice regions for a specific guild.

    The bot must be a member of the guild.

    Args:
        guild_id (str): The ID of the guild to retrieve voice regions for.
    """
    endpoint = f"/guilds/{guild_id}/regions"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_INTEGRATIONS(guild_id: str):
    """
    Retrieves a list of all integrations for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve integrations from.
    """
    endpoint = f"/guilds/{guild_id}/integrations"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_DELETE_GUILD_INTEGRATION(
    guild_id: str,
    integration_id: str
):
    """
    Deletes an integration from a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild.
        integration_id (str): The ID of the integration to delete.
    """
    endpoint = f"/guilds/{guild_id}/integrations/{integration_id}"
    return await discord_request("DELETE", endpoint)
#guild management ended
#*********************************************************************************
# webhook management started

@mcp.tool()
async def DISCORDBOT_CREATE_WEBHOOK(
    channel_id: str,
    name: str,
    avatar: Optional[str] = None
):
    """
    Creates a new webhook in a channel.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        channel_id (str): The ID of the channel to create the webhook in.
        name (str): The name for the webhook (1-80 characters).
        avatar (Optional[str]): A Base64 encoded image data URI for the webhook avatar.
    """
    endpoint = f"/channels/{channel_id}/webhooks"
    
    payload = {
        "name": name,
    }
    if avatar is not None:
        payload["avatar"] = avatar
        
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_WEBHOOK(webhook_id: str):
    """
    Retrieves a specific webhook object.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        webhook_id (str): The ID of the webhook to retrieve.
    """
    endpoint = f"/webhooks/{webhook_id}"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_WEBHOOK(
    webhook_id: str,
    **kwargs
):
    """
    Updates an existing webhook.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        webhook_id (str): The ID of the webhook to update.
        **kwargs: Optional fields to update, such as 'name', 'avatar', or 'channel_id'.
    """
    if not kwargs:
        raise ValueError("At least one attribute to update (e.g., name, avatar) must be provided.")

    endpoint = f"/webhooks/{webhook_id}"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_DELETE_WEBHOOK(webhook_id: str):
    """
    Deletes a specific webhook.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        webhook_id (str): The ID of the webhook to delete.
    """
    endpoint = f"/webhooks/{webhook_id}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_GET_WEBHOOK_BY_TOKEN(
    webhook_id: str,
    webhook_token: str
):
    """
    Retrieves a webhook object using its token for authentication.

    NOTE: This method does not require bot authentication.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}"
    # This specific endpoint doesn't use the standard bot token,
    # so we call it directly instead of using the helper.
    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_UPDATE_WEBHOOK_BY_TOKEN(
    webhook_id: str,
    webhook_token: str,
    name: Optional[str] = None,
    avatar: Optional[str] = None
):
    """
    Updates a webhook using its token for authentication.

    NOTE: This method does not require bot authentication.

    Args:
        webhook_id (str): The ID of the webhook to update.
        webhook_token (str): The secret token of the webhook.
        name (Optional[str]): The new default name for the webhook.
        avatar (Optional[str]): A new Base64 encoded image data URI for the avatar.
    """
    if name is None and avatar is None:
        raise ValueError("At least one attribute to update (name or avatar) must be provided.")

    endpoint = f"/webhooks/{webhook_id}/{webhook_token}"
    url = f"{DISCORD_API_BASE}{endpoint}"
    
    payload = {}
    if name is not None:
        payload["name"] = name
    if avatar is not None:
        payload["avatar"] = avatar
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload) as resp:
            if resp.status in [200, 201]:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_DELETE_WEBHOOK_BY_TOKEN(
    webhook_id: str,
    webhook_token: str
):
    """
    Deletes a webhook using its token for authentication.

    NOTE: This method does not require bot authentication.

    Args:
        webhook_id (str): The ID of the webhook to delete.
        webhook_token (str): The secret token of the webhook.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}"
    # This specific endpoint doesn't use the standard bot token,
    # so we call it directly instead of using the helper.
    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as resp:
            # A successful deletion returns a 204 No Content status
            if resp.status == 204:
                return {"successful": True, "data": {"message": "Webhook deleted successfully."}}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")


@mcp.tool()
async def DISCORDBOT_EXECUTE_WEBHOOK(
    webhook_id: str,
    webhook_token: str,
    wait: Optional[bool] = None,
    thread_id: Optional[str] = None,
    **kwargs
):
    """
    Executes a webhook to send a message.

    NOTE: This method uses the webhook's token for authentication, not the bot's.
    You must provide at least one of 'content', 'embeds', or 'files'.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        wait (Optional[bool]): If true, waits for server confirmation of message send.
        thread_id (Optional[str]): Sends the message to a thread within the webhook's channel.
        **kwargs: The message content, e.g., content="Hello", username="Custom Name", embeds=[...].
    """
    if not any(key in kwargs for key in ["content", "embeds", "files"]):
        raise ValueError("You must provide at least one of 'content', 'embeds', or 'files'.")

    endpoint = f"/webhooks/{webhook_id}/{webhook_token}"
    
    params = {}
    if wait is not None:
        params["wait"] = str(wait).lower()
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    payload = kwargs
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status in [200, 201]:
                return await resp.json()
            elif resp.status == 204:
                return {"status": "success", "detail": "Webhook executed successfully."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_EXECUTE_SLACK_COMPATIBLE_WEBHOOK(
    webhook_id: str,
    webhook_token: str,
    wait: Optional[bool] = None,
    thread_id: Optional[str] = None,
    **kwargs
):
    """
    Executes a webhook with a Slack-compatible payload.

    NOTE: This method uses the webhook's token for authentication. You must provide
    a Slack-formatted payload (e.g., with 'text' or 'attachments') as keyword arguments.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        wait (Optional[bool]): If true, waits for server confirmation of message send.
        thread_id (Optional[str]): Sends the message to a thread within the webhook's channel.
        **kwargs: The Slack-compatible message payload (e.g., text="Hello", attachments=[...]).
    """
    if not kwargs:
        raise ValueError("You must provide a Slack-compatible payload (e.g., 'text').")

    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/slack"
    
    params = {}
    if wait is not None:
        params["wait"] = str(wait).lower()
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    payload = kwargs
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            # A successful execution returns a 200 OK with 'ok' or a 204 No Content
            if resp.status in [200, 204]:
                try:
                    return await resp.json()
                except aiohttp.ContentTypeError: # Handle empty response on 204
                    return {"status": "success", "detail": "Webhook executed successfully."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_EXECUTE_GITHUB_COMPATIBLE_WEBHOOK(
    webhook_id: str,
    webhook_token: str,
    wait: Optional[bool] = None,
    thread_id: Optional[str] = None,
    **kwargs
):
    """
    Executes a webhook with a GitHub-compatible payload.

    NOTE: This method uses the webhook's token for authentication. You must provide
    a GitHub-formatted payload (e.g., with 'ref', 'commits', 'sender') as keyword arguments.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        wait (Optional[bool]): If true, waits for server confirmation of message send.
        thread_id (Optional[str]): Sends the message to a thread within the webhook's channel.
        **kwargs: The GitHub-compatible message payload.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/github"
    
    params = {}
    if wait is not None:
        params["wait"] = str(wait).lower()
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    payload = kwargs
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status in [200, 204]:
                try:
                    # Try to return JSON if wait=true, otherwise return success message
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    return {"status": "success", "detail": "Webhook executed successfully."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_GET_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    message_id: str,
    thread_id: Optional[str] = None
):
    """
    Retrieves a specific message previously sent by a webhook.

    NOTE: This method uses the webhook's token for authentication, not the bot's.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        message_id (str): The ID of the message to retrieve.
        thread_id (Optional[str]): The ID of the thread the message is in.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_UPDATE_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    message_id: str,
    thread_id: Optional[str] = None,
    **kwargs
):
    """
    Updates a specific message previously sent by a webhook.

    NOTE: This method uses the webhook's token for authentication, not the bot's.
    You must provide at least one content field (e.g., 'content', 'embeds') to update.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        message_id (str): The ID of the message to edit.
        thread_id (Optional[str]): The ID of the thread the message is in.
        **kwargs: The new message content, e.g., content="New content", embeds=[...].
    """
    if not kwargs:
        raise ValueError("You must provide at least one field to update (e.g., 'content').")

    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    payload = kwargs
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_DELETE_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    message_id: str,
    thread_id: Optional[str] = None
):
    """
    Deletes a specific message previously sent by a webhook.

    NOTE: This method uses the webhook's token for authentication, not the bot's.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        message_id (str): The ID of the message to delete.
        thread_id (Optional[str]): The ID of the thread the message is in.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as resp:
            # A successful deletion returns a 204 No Content status
            if resp.status == 204:
                return {"status": "success", "detail": "Webhook message deleted successfully."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_GET_ORIGINAL_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    thread_id: Optional[str] = None
):
    """
    Retrieves the original message sent by a webhook after an interaction.

    NOTE: This method uses the webhook's token for authentication, not the bot's.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        thread_id (Optional[str]): The ID of the thread the message is in.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/@original"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")

@mcp.tool()
async def DISCORDBOT_UPDATE_ORIGINAL_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    thread_id: Optional[str] = None,
    **kwargs
):
    """
    Updates the original message sent by a webhook after an interaction.

    NOTE: This method uses the webhook's token for authentication, not the bot's.
    You must provide at least one content field (e.g., 'content', 'embeds') to update.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        thread_id (Optional[str]): The ID of the thread the message is in.
        **kwargs: The new message content, e.g., content="New content", embeds=[...].
    """
    if not kwargs:
        raise ValueError("You must provide at least one field to update (e.g., 'content').")

    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/@original"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    payload = kwargs
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")


@mcp.tool()
async def DISCORDBOT_DELETE_ORIGINAL_WEBHOOK_MESSAGE(
    webhook_id: str,
    webhook_token: str,
    thread_id: Optional[str] = None
):
    """
    Deletes the original message sent by a webhook after an interaction.

    NOTE: This method uses the webhook's token for authentication, not the bot's.

    Args:
        webhook_id (str): The ID of the webhook.
        webhook_token (str): The secret token of the webhook.
        thread_id (Optional[str]): The ID of the thread the message is in.
    """
    endpoint = f"/webhooks/{webhook_id}/{webhook_token}/messages/@original"
    
    params = {}
    if thread_id is not None:
        params["thread_id"] = thread_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"

    url = f"{DISCORD_API_BASE}{endpoint}"
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as resp:
            # A successful deletion returns a 204 No Content status
            if resp.status == 204:
                return {"status": "success", "detail": "Original webhook message deleted."}
            else:
                text = await resp.text()
                raise Exception(f"Discord API Error {resp.status}: {text}")


@mcp.tool()
async def DISCORDBOT_LIST_CHANNEL_WEBHOOKS(channel_id: str):
    """
    Retrieves a list of all webhooks for a specific channel.

    NOTE: Requires the 'Manage Webhooks' permission.

    Args:
        channel_id (str): The ID of the channel to retrieve webhooks from.
    """
    endpoint = f"/channels/{channel_id}/webhooks"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_INTEGRATIONS(guild_id: str):
    """
    Retrieves a list of all integrations for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve integrations from.
    """
    endpoint = f"/guilds/{guild_id}/integrations"
    return await discord_request("GET", endpoint)
#webhook management ended
#*********************************************************************************
#invite management started
@mcp.tool()
async def DISCORDBOT_INVITE_RESOLVE(
    code: str,
    with_counts: Optional[bool] = None,
    guild_scheduled_event_id: Optional[str] = None
):
    """
    Retrieves details about a specific guild invite.

    Args:
        code (str): The unique code from the invite link.
        with_counts (Optional[bool]): If true, includes approximate member counts.
        guild_scheduled_event_id (Optional[str]): The ID of a scheduled event to
                                                 include in the invite data.
    """
    endpoint = f"/invites/{code}"
    
    params = {}
    if with_counts is not None:
        params["with_counts"] = with_counts
    if guild_scheduled_event_id is not None:
        params["guild_scheduled_event_id"] = guild_scheduled_event_id
        
    if params:
        query_string = urllib.parse.urlencode(params)
        endpoint += f"?{query_string}"
        
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_INVITE_REVOKE(code: str):
    """
    Deletes (revokes) a guild invite.

    NOTE: Requires the 'Manage Server' or 'Manage Channels' permission.

    Args:
        code (str): The unique code of the invite to delete.
    """
    endpoint = f"/invites/{code}"
    return await discord_request("DELETE", endpoint)

@mcp.tool()
async def DISCORDBOT_CREATE_CHANNEL_INVITE(
    channel_id: str,
    **kwargs
):
    """
    Creates a new invite for a channel.

    NOTE: Requires the 'Create Instant Invite' permission.

    Args:
        channel_id (str): The ID of the channel to create the invite for.
        **kwargs: Optional parameters for the invite, such as 'max_age' (in seconds),
                  'max_uses', 'temporary', etc.
    """
    endpoint = f"/channels/{channel_id}/invites"
    
    # The keyword arguments are passed directly as the payload
    payload = kwargs
        
    return await discord_request("POST", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_LIST_CHANNEL_INVITES(channel_id: str):
    """
    Retrieves a list of all active invites for a specific channel.

    NOTE: Requires the 'Manage Channel' permission for that channel.

    Args:
        channel_id (str): The ID of the channel to retrieve invites from.
    """
    endpoint = f"/channels/{channel_id}/invites"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_LIST_GUILD_INVITES(guild_id: str):
    """
    Retrieves a list of all active invite links for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to retrieve invites from.
    """
    endpoint = f"/guilds/{guild_id}/invites"
    return await discord_request("GET", endpoint)

@mcp.tool()
async def DISCORDBOT_UPDATE_GUILD_WIDGET_SETTINGS(
    guild_id: str,
    enabled: Optional[bool] = None,
    channel_id: Optional[str] = None
):
    """
    Updates the widget settings for a specific guild.

    NOTE: Requires the 'Manage Server' permission.

    Args:
        guild_id (str): The ID of the guild to update the widget settings for.
        enabled (Optional[bool]): Whether the widget is enabled.
        channel_id (Optional[str]): The ID of the widget channel.
    """
    if enabled is None and channel_id is None:
        raise ValueError("At least one setting (enabled or channel_id) must be provided.")

    endpoint = f"/guilds/{guild_id}/widget"
    
    payload = {}
    if enabled is not None:
        payload["enabled"] = enabled
    if channel_id is not None:
        payload["channel_id"] = channel_id
        
    return await discord_request("PATCH", endpoint, json=payload)

@mcp.tool()
async def DISCORDBOT_GET_GUILD_VANITY_URL(guild_id: str):
    """
    Retrieves the vanity URL information for a specific guild.

    NOTE: Requires the 'Manage Server' permission. The guild must have a
    vanity URL set (usually through Server Boosting).

    Args:
        guild_id (str): The ID of the guild to retrieve the vanity URL from.
    """
    endpoint = f"/guilds/{guild_id}/vanity-url"
    return await discord_request("GET", endpoint)
#invite management ended
# ---------- MAIN ----------
if __name__ == "__main__":
    mcp.run()