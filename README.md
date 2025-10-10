# Discord Bot MCP Server

This project provides a comprehensive set of tools to interact with the Discord API, wrapped in a Python server using the `FastMCP` framework. It allows you to manage guilds (servers), channels, messages, users, webhooks, and more through a standardized tool interface.

---
## ## Features

This server exposes a wide range of Discord API functionalities, grouped into the following categories:

* **Emoji & Sticker Management:** Create, retrieve, update, delete, and list custom emojis and stickers for a server.
* **Utility & Channel Tools:** Follow announcement channels, trigger typing indicators, crosspost messages, and manage DMs.
* **Guild (Server) Management:** A full suite of tools to create, delete, update, and retrieve information about servers, members, roles, bans, and invites.
* **Webhook Management:** Create, retrieve, update, delete, and execute webhooks, including special compatibility modes for Slack and GitHub.
* **Invite Management:** Create, resolve (get details), and revoke (delete) invite links for channels and servers.

---
## ## Getting Started

Follow these steps to get your Discord Bot MCP server up and running.

### ### Prerequisites

* Python 3.7+
* A Discord Bot Application and its secret token. You can create one on the [Discord Developer Portal](https://discord.com/developers/applications).

### ### Installation

1.  Clone or download the repository containing your `production.py` file.
2.  Install the required Python libraries:
    ```bash
    pip install "fastmcp[server]" aiohttp
    ```

### ### Configuration

This script requires your Discord Bot's secret token to be set as an environment variable.

* **On Windows (PowerShell):**
    ```powershell
    $env:DISCORDBOT_TOKEN = "Your_Secret_Bot_Token_Here"
    ```

* **On macOS / Linux (Bash/Zsh):**
    ```bash
    export DISCORDBOT_TOKEN="Your_Secret_Bot_Token_Here"
    ```

---
## ## Running the Server

Once the environment variable is set, run the script from your terminal:

```bash
python production.py
```

The server will start, and you can now connect to it with a tool like the MCP Inspector to call the available tools.

---
## ## Available Tools

Here is a complete list of the tools available on this server.

### ### Emoji & Sticker Management

* **`DISCORDBOT_CREATE_GUILD_EMOJI`**: Creates a new custom emoji.
    * `guild_id` (str): The ID of the server.
    * `name` (str): The emoji name.
    * `image` (str): Base64 encoded image data.
    * `roles` (Optional[List[str]]): Roles allowed to use this emoji.

* **`DISCORDBOT_GET_GUILD_EMOJI`**: Retrieves a specific custom emoji.
    * `guild_id` (str): The server ID.
    * `emoji_id` (str): The ID of the emoji to fetch.

* **`DISCORDBOT_UPDATE_GUILD_EMOJI`**: Updates an emoji's name or roles.
    * `guild_id` (str): The server ID.
    * `emoji_id` (str): The ID of the emoji to update.
    * `name` (Optional[str]): New name for the emoji.
    * `roles` (Optional[List[str]]): New list of roles that can use the emoji.

* **`DISCORDBOT_DELETE_GUILD_EMOJI`**: Deletes a custom emoji.
    * `guild_id` (str): The server ID.
    * `emoji_id` (str): The ID of the emoji to delete.

* **`DISCORDBOT_LIST_GUILD_EMOJIS`**: Retrieves all custom emojis for a server.
    * `guild_id` (str): The server ID.

## Discord Guild Tools

These are the available Discord guild management tools in this project:

- `DISCORDBOT_CREATE_GUILD`
- `DISCORDBOT_DELETE_GUILD`
- `DISCORDBOT_UPDATE_GUILD`
- `DISCORDBOT_GET_GUILD`
- `DISCORDBOT_LIST_GUILD_CHANNELS`
- `DISCORDBOT_LIST_GUILD_MEMBERS`
- `DISCORDBOT_GET_GUILD_MEMBER`
- `DISCORDBOT_UPDATE_GUILD_MEMBER`
- `DISCORDBOT_DELETE_GUILD_MEMBER`
- `DISCORDBOT_BAN_USER_FROM_GUILD`
- `DISCORDBOT_UNBAN_USER_FROM_GUILD`
- `DISCORDBOT_LIST_GUILD_BANS`
- `DISCORDBOT_GET_GUILD_BAN`
- `DISCORDBOT_PRUNE_GUILD`
- `DISCORDBOT_PREVIEW_PRUNE_GUILD`
- `DISCORDBOT_LIST_GUILD_ROLES`
- `DISCORDBOT_CREATE_GUILD_ROLE`
- `DISCORDBOT_UPDATE_GUILD_ROLE`
- `DISCORDBOT_DELETE_GUILD_ROLE`
- `DISCORDBOT_SEARCH_GUILD_MEMBERS`
- `DISCORDBOT_LEAVE_GUILD`
- `DISCORDBOT_LIST_GUILD_INVITES`
- `DISCORDBOT_CREATE_GUILD_FROM_TEMPLATE`
- `DISCORDBOT_SYNC_GUILD_TEMPLATE`
- `DISCORDBOT_GET_GUILD_TEMPLATE`
- `DISCORDBOT_UPDATE_GUILD_TEMPLATE`
- `DISCORDBOT_DELETE_GUILD_TEMPLATE`
- `DISCORDBOT_CREATE_GUILD_TEMPLATE`
- `DISCORDBOT_GET_GUILD_PREVIEW`
- `DISCORDBOT_GET_GUILDS_ONBOARDING`
- `DISCORDBOT_PUT_GUILDS_ONBOARDING`
- `DISCORDBOT_GET_GUILD_WIDGET`
- `DISCORDBOT_GET_GUILD_WIDGET_SETTINGS`
- `DISCORDBOT_UPDATE_GUILD_WIDGET_SETTINGS`
- `DISCORDBOT_GET_GUILD_WELCOME_SCREEN`
- `DISCORDBOT_UPDATE_GUILD_WELCOME_SCREEN`
- `DISCORDBOT_GET_GUILD_VANITY_URL`
- `DISCORDBOT_GET_GUILD_WEBHOOKS`
- `DISCORDBOT_GET_GUILD_SCHEDULED_EVENT`
- `DISCORDBOT_CREATE_GUILD_SCHEDULED_EVENT`
- `DISCORDBOT_UPDATE_GUILD_SCHEDULED_EVENT`
- `DISCORDBOT_DELETE_GUILD_SCHEDULED_EVENT`
- `DISCORDBOT_LIST_GUILD_SCHEDULED_EVENTS`
- `DISCORDBOT_LIST_GUILD_SCHEDULED_EVENT_USERS`
- `DISCORDBOT_LIST_GUILD_VOICE_REGIONS`
- `DISCORDBOT_LIST_GUILD_INTEGRATIONS`
- `DISCORDBOT_DELETE_GUILD_INTEGRATION`
