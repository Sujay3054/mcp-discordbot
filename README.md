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

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_GUILD` | Creates a new Discord guild. | `name`, `region`, optional settings like `icon`, `channels` | Success status and guild object |
| `DISCORDBOT_DELETE_GUILD` | Deletes a guild. | `guild_id` | Success status |
| `DISCORDBOT_UPDATE_GUILD` | Updates guild settings. | `guild_id`, settings to update | Updated guild object |
| `DISCORDBOT_GET_GUILD` | Retrieves guild information. | `guild_id` | Guild object |
| `DISCORDBOT_LIST_GUILD_CHANNELS` | Lists all channels in a guild. | `guild_id` | Array of channel objects |
| `DISCORDBOT_LIST_GUILD_MEMBERS` | Lists all members of a guild. | `guild_id`, optional `limit` | Array of member objects |
| `DISCORDBOT_GET_GUILD_MEMBER` | Retrieves a specific member in a guild. | `guild_id`, `user_id` | Member object |
| `DISCORDBOT_UPDATE_GUILD_MEMBER` | Updates a guild member's info. | `guild_id`, `user_id`, updated fields | Updated member object |
| `DISCORDBOT_DELETE_GUILD_MEMBER` | Removes a member from a guild. | `guild_id`, `user_id` | Success status |
| `DISCORDBOT_BAN_USER_FROM_GUILD` | Bans a user from a guild. | `guild_id`, `user_id`, optional `reason`, `delete_message_days` | Success status |
| `DISCORDBOT_UNBAN_USER_FROM_GUILD` | Removes a ban from a user. | `guild_id`, `user_id` | Success status |
| `DISCORDBOT_LIST_GUILD_BANS` | Lists all banned users in a guild. | `guild_id` | Array of ban objects |
| `DISCORDBOT_GET_GUILD_BAN` | Retrieves ban info for a user. | `guild_id`, `user_id` | Ban object |
| `DISCORDBOT_PRUNE_GUILD` | Prunes inactive members from a guild. | `guild_id`, `days` | Number of members removed |
| `DISCORDBOT_PREVIEW_PRUNE_GUILD` | Previews how many members would be pruned. | `guild_id`, `days` | Number of members that would be removed |
| `DISCORDBOT_LIST_GUILD_ROLES` | Lists all roles in a guild. | `guild_id` | Array of role objects |
| `DISCORDBOT_CREATE_GUILD_ROLE` | Creates a new role in a guild. | `guild_id`, role settings (`name`, `permissions`, etc.) | Created role object |
| `DISCORDBOT_UPDATE_GUILD_ROLE` | Updates a role in a guild. | `guild_id`, `role_id`, fields to update | Updated role object |
| `DISCORDBOT_DELETE_GUILD_ROLE` | Deletes a role from a guild. | `guild_id`, `role_id` | Success status |
| `DISCORDBOT_SEARCH_GUILD_MEMBERS` | Searches members by username/nickname. | `guild_id`, `query`, optional `limit` | Array of matching member objects |
| `DISCORDBOT_LEAVE_GUILD` | Makes the bot leave a guild. | `guild_id` | Success status |
| `DISCORDBOT_LIST_GUILD_INVITES` | Lists all invites for a guild. | `guild_id` | Array of invite objects |
| `DISCORDBOT_CREATE_GUILD_FROM_TEMPLATE` | Creates a guild from a template. | `template_code`, `name` | New guild object |
| `DISCORDBOT_SYNC_GUILD_TEMPLATE` | Syncs a guild with its template. | `guild_id`, `template_code` | Updated template object |
| `DISCORDBOT_GET_GUILD_TEMPLATE` | Retrieves a guild template. | `template_code` | Template object |
| `DISCORDBOT_UPDATE_GUILD_TEMPLATE` | Updates a guild template. | `template_code`, fields to update | Updated template object |
| `DISCORDBOT_DELETE_GUILD_TEMPLATE` | Deletes a guild template. | `template_code` | Success status |
| `DISCORDBOT_CREATE_GUILD_TEMPLATE` | Creates a new template from a guild. | `guild_id`, `name`, `description` | Template object |
| `DISCORDBOT_GET_GUILD_PREVIEW` | Retrieves a preview of a guild. | `guild_id` | Guild preview object |
| `DISCORDBOT_GET_GUILDS_ONBOARDING` | Gets guild onboarding info. | `guild_id` | Onboarding object |
| `DISCORDBOT_PUT_GUILDS_ONBOARDING` | Updates guild onboarding. | `guild_id`, updated fields | Updated onboarding object |
| `DISCORDBOT_GET_GUILD_WIDGET` | Retrieves the guild widget. | `guild_id` | Widget object |
| `DISCORDBOT_GET_GUILD_WIDGET_SETTINGS` | Retrieves guild widget settings. | `guild_id` | Widget settings object |
| `DISCORDBOT_UPDATE_GUILD_WIDGET_SETTINGS` | Updates guild widget settings. | `guild_id`, updated fields | Updated widget settings |
| `DISCORDBOT_GET_GUILD_WELCOME_SCREEN` | Gets the welcome screen of a guild. | `guild_id` | Welcome screen object |
| `DISCORDBOT_UPDATE_GUILD_WELCOME_SCREEN` | Updates a guild's welcome screen. | `guild_id`, updated fields | Updated welcome screen |
| `DISCORDBOT_GET_GUILD_VANITY_URL` | Gets the vanity URL for a guild. | `guild_id` | Vanity URL object |
| `DISCORDBOT_GET_GUILD_WEBHOOKS` | Lists all webhooks in a guild. | `guild_id` | Array of webhook objects |
| `DISCORDBOT_GET_GUILD_SCHEDULED_EVENT` | Retrieves a scheduled event. | `guild_id`, `event_id` | Event object |
| `DISCORDBOT_CREATE_GUILD_SCHEDULED_EVENT` | Creates a scheduled event. | `guild_id`, event fields | Created event object |
| `DISCORDBOT_UPDATE_GUILD_SCHEDULED_EVENT` | Updates a scheduled event. | `guild_id`, `event_id`, updated fields | Updated event object |
| `DISCORDBOT_DELETE_GUILD_SCHEDULED_EVENT` | Deletes a scheduled event. | `guild_id`, `event_id` | Success status |
| `DISCORDBOT_LIST_GUILD_SCHEDULED_EVENTS` | Lists all scheduled events. | `guild_id` | Array of event objects |
| `DISCORDBOT_LIST_GUILD_SCHEDULED_EVENT_USERS` | Lists users for a scheduled event. | `guild_id`, `event_id` | Array of user objects |
| `DISCORDBOT_LIST_GUILD_VOICE_REGIONS` | Lists voice regions in a guild. | `guild_id` | Array of voice region objects |
| `DISCORDBOT_LIST_GUILD_INTEGRATIONS` | Lists integrations in a guild. | `guild_id` | Array of integration objects |
| `DISCORDBOT_DELETE_GUILD_INTEGRATION` | Deletes a guild integration. | `guild_id`, `integration_id` | Success status |
