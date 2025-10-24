# Discord Bot MCP Server

This project provides a comprehensive set of tools to interact with the Discord API, wrapped in a Python server using the FastMCP framework. It allows you to manage guilds (servers), channels, messages, users, webhooks, and more through a standardized tool interface.

## Features

This server exposes a wide range of Discord API functionalities, grouped into the following categories:

- **Application & Command Management**: Create, update, delete, and manage Discord slash commands and applications
- **Channel & Thread Management**: Create, update, delete channels, manage threads, and handle permissions
- **Message Management**: Send, edit, delete messages, manage reactions, and handle bulk operations
- **Moderation & Automation**: Auto-moderation rules, user bans, and bulk operations
- **Guild (Server) Management**: Complete server management including members, roles, bans, and invites
- **User & Member Management**: User information, member updates, and role management
- **Emoji & Sticker Management**: Create, retrieve, update, delete, and list custom emojis and stickers
- **Webhook Management**: Full webhook lifecycle management with Slack/GitHub compatibility
- **Invite & Template Management**: Create, resolve, and revoke invite links and guild templates

## Getting Started

Follow these steps to get your Discord Bot MCP server up and running.

### Prerequisites

- Python 3.7+
- A Discord Bot Application and its secret token. You can create one on the [Discord Developer Portal](https://discord.com/developers/applications)

### Getting Your Discord Bot Token

Follow these steps to create a Discord bot and obtain its token:

#### Step 1: Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Enter a name for your application (this will be your bot's name)
4. Click **"Create"**

#### Step 2: Create a Bot

1. In your application dashboard, navigate to the **"Bot"** section in the left sidebar
2. Click **"Add Bot"** and confirm when prompted
3. Your bot is now created! You'll see a section with your bot's information

#### Step 3: Get Your Bot Token

1. In the **"Bot"** section, find the **"Token"** field
2. Click **"Copy"** to copy your bot token
3. **⚠️ IMPORTANT**: Keep this token secret! Never share it publicly or commit it to version control

#### Step 4: Set Bot Permissions

1. In the **"Bot"** section, scroll down to **"Privileged Gateway Intents"**
2. Enable the intents you need:
   - **Server Members Intent**: Required for `LIST_GUILD_MEMBERS`, `SEARCH_GUILD_MEMBERS`
   - **Message Content Intent**: Required for reading message content
   - **Presence Intent**: Required for presence information

#### Step 5: Generate Invite URL

1. Navigate to the **"OAuth2"** > **"URL Generator"** section
2. Under **"Scopes"**, select:
   - **`bot`**: Allows your application to join servers as a bot
   - **`applications.commands`**: Allows your bot to create slash commands
3. Under **"Bot Permissions"**, select the permissions your bot needs:
   - **Administrator**: Full access (use with caution)
   - Or select specific permissions like:
     - **Send Messages**
     - **Manage Messages**
     - **Manage Roles**
     - **Manage Channels**
     - **Kick Members**
     - **Ban Members**
     - **Manage Webhooks**
     - **Manage Emojis and Stickers**
4. Copy the generated URL and open it in your browser
5. Select a server and authorize the bot

#### Step 6: Configure Your Bot

1. Create a `.env` file in your project directory:
   ```bash
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_API_BASE=https://discord.com/api/v10
   REQUEST_TIMEOUT=30.0
   ```
2. Replace `your_bot_token_here` with the token you copied in Step 3

#### Security Best Practices

- ✅ **DO**: Store your token in environment variables
- ✅ **DO**: Use a `.env` file (make sure it's in your `.gitignore`)
- ✅ **DO**: Keep your token private and secure
- ❌ **DON'T**: Hardcode tokens in your source code
- ❌ **DON'T**: Share your token publicly
- ❌ **DON'T**: Commit tokens to version control

#### Troubleshooting

**Token not working?**
- Make sure you copied the entire token without extra spaces
- Verify the bot is properly invited to your server
- Check that the bot has the necessary permissions

**Bot not responding?**
- Ensure the bot is online in your server
- Check that the bot has the required intents enabled
- Verify the bot has the necessary permissions for the actions you're trying to perform

### Installation

1. Clone or download the repository containing your `stage_organized.py` file
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

This script requires your Discord Bot's secret token to be set as an environment variable.

Create a `.env` file in the same directory as `stage_organized.py`:

```bash
# .env file
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_API_BASE=https://discord.com/api/v10
REQUEST_TIMEOUT=30.0
```

Or set environment variables directly:

**On Windows (PowerShell):**
```powershell
$env:DISCORD_BOT_TOKEN = "Your_Secret_Bot_Token_Here"
```

**On macOS / Linux (Bash/Zsh):**
```bash
export DISCORD_BOT_TOKEN="Your_Secret_Bot_Token_Here"
```

## Running the Server

Once the environment variable is set, run the script from your terminal:

```bash
python stage_organized.py
```

The server will start, and you can now connect to it with a tool like the MCP Inspector to call the available tools.

## Available Tools

Here is a complete list of the tools available on this server, organized by category.

### Application & Command Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_APPLICATION_COMMAND` | Creates a new global application command | `application_id`, `name`, `description`, `type`, `options` | Created command object |
| `DISCORDBOT_DELETE_APPLICATION_COMMAND` | Deletes a global application command | `application_id`, `command_id` | Success status |
| `DISCORDBOT_UPDATE_APPLICATION_COMMAND` | Updates a global application command | `application_id`, `command_id`, fields to update | Updated command object |
| `DISCORDBOT_GET_APPLICATION_COMMAND` | Fetches a global application command | `application_id`, `command_id` | Command object |
| `DISCORDBOT_LIST_APPLICATION_COMMANDS` | Fetches all global commands for an application | `application_id`, `with_localizations` | Array of command objects |
| `DISCORDBOT_CREATE_GUILD_APPLICATION_COMMAND` | Creates a new guild application command | `application_id`, `guild_id`, `name`, `description` | Created command object |
| `DISCORDBOT_DELETE_GUILD_APPLICATION_COMMAND` | Deletes a guild application command | `application_id`, `guild_id`, `command_id` | Success status |
| `DISCORDBOT_UPDATE_GUILD_APPLICATION_COMMAND` | Updates a guild application command | `application_id`, `guild_id`, `command_id`, fields to update | Updated command object |
| `DISCORDBOT_GET_GUILD_APPLICATION_COMMAND` | Fetches a guild application command | `application_id`, `guild_id`, `command_id` | Command object |
| `DISCORDBOT_LIST_GUILD_APPLICATION_COMMANDS` | Fetches all guild commands for an application | `application_id`, `guild_id`, `with_localizations` | Array of command objects |

### Channel & Thread Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_GET_CHANNEL` | Gets a channel by ID | `channel_id` | Channel object |
| `DISCORDBOT_CREATE_GUILD_CHANNEL` | Creates a new channel in a guild | `guild_id`, `name`, `type`, optional settings | Created channel object |
| `DISCORDBOT_UPDATE_CHANNEL` | Updates a channel's settings | `channel_id`, fields to update | Updated channel object |
| `DISCORDBOT_DELETE_CHANNEL` | Deletes a channel | `channel_id` | Success status |
| `DISCORDBOT_LIST_GUILD_CHANNELS` | Lists all channels in a guild | `guild_id` | Array of channel objects |
| `DISCORDBOT_CREATE_CHANNEL_INVITE` | Creates a new invite for a channel | `channel_id`, invite settings | Created invite object |
| `DISCORDBOT_LIST_CHANNEL_INVITES` | Lists all invites for a channel | `channel_id` | Array of invite objects |
| `DISCORDBOT_SET_CHANNEL_PERMISSION_OVERWRITE` | Edits channel permission overwrites | `channel_id`, `overwrite_id`, `allow`, `deny`, `type` | Success status |
| `DISCORDBOT_DELETE_CHANNEL_PERMISSION_OVERWRITE` | Deletes a channel permission overwrite | `channel_id`, `overwrite_id` | Success status |
| `DISCORDBOT_CREATE_THREAD` | Creates a new thread from an existing channel | `channel_id`, `name`, `type`, settings | Created thread object |
| `DISCORDBOT_CREATE_THREAD_FROM_MESSAGE` | Creates a new thread from an existing message | `channel_id`, `message_id`, `name`, settings | Created thread object |
| `DISCORDBOT_JOIN_THREAD` | Adds the current user to a thread | `channel_id` | Success status |
| `DISCORDBOT_LEAVE_THREAD` | Removes the current user from a thread | `channel_id` | Success status |
| `DISCORDBOT_GET_THREAD_MEMBER` | Returns a thread member object | `channel_id`, `user_id` | Thread member object |
| `DISCORDBOT_DELETE_THREAD_MEMBER` | Removes another member from a thread | `channel_id`, `user_id` | Success status |
| `DISCORDBOT_LIST_THREAD_MEMBERS` | Returns array of thread members | `channel_id`, optional filters | Array of thread member objects |

### Message Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_MESSAGE` | Sends a message to a Discord channel | `channel_id`, `content`, `embeds`, `files`, `components` | Created message object |
| `DISCORDBOT_GET_MESSAGE` | Returns a specific message in the channel | `channel_id`, `message_id` | Message object |
| `DISCORDBOT_UPDATE_MESSAGE` | Updates a message | `channel_id`, `message_id`, new content | Updated message object |
| `DISCORDBOT_DELETE_MESSAGE` | Deletes a message | `channel_id`, `message_id` | Success status |
| `DISCORDBOT_LIST_MESSAGES` | Returns the messages for a channel | `channel_id`, optional filters | Array of message objects |
| `DISCORDBOT_PIN_MESSAGE` | Pins a message in a channel | `channel_id`, `message_id` | Success status |
| `DISCORDBOT_UNPIN_MESSAGE` | Unpins a message in a channel | `channel_id`, `message_id` | Success status |
| `DISCORDBOT_LIST_PINNED_MESSAGES` | Returns all pinned messages in the channel | `channel_id` | Array of message objects |
| `DISCORDBOT_ADD_MY_MESSAGE_REACTION` | Creates a reaction for the message | `channel_id`, `message_id`, `emoji` | Success status |
| `DISCORDBOT_DELETE_MY_MESSAGE_REACTION` | Deletes a reaction the current user has made | `channel_id`, `message_id`, `emoji` | Success status |
| `DISCORDBOT_DELETE_USER_MESSAGE_REACTION` | Deletes another user's reaction | `channel_id`, `message_id`, `emoji`, `user_id` | Success status |
| `DISCORDBOT_DELETE_ALL_MESSAGE_REACTIONS` | Deletes all reactions on a message | `channel_id`, `message_id` | Success status |
| `DISCORDBOT_DELETE_ALL_MESSAGE_REACTIONS_BY_EMOJI` | Deletes all reactions for the given emoji | `channel_id`, `message_id`, `emoji` | Success status |
| `DISCORDBOT_LIST_MESSAGE_REACTIONS_BY_EMOJI` | Gets a list of users that reacted with this emoji | `channel_id`, `message_id`, `emoji`, optional filters | Array of user objects |
| `DISCORDBOT_BULK_DELETE_MESSAGES` | Deletes multiple messages in a single request | `channel_id`, `messages` (array) | Success status |
| `DISCORDBOT_CROSSPOST_MESSAGE` | Crossposts a message in a News Channel | `channel_id`, `message_id` | Crossposted message object |

### Guild (Server) Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_GUILD` | Creates a new guild | `name`, optional settings | Created guild object |
| `DISCORDBOT_DELETE_GUILD` | Deletes a guild permanently | `guild_id` | Success status |
| `DISCORDBOT_UPDATE_GUILD` | Updates guild settings | `guild_id`, fields to update | Updated guild object |
| `DISCORDBOT_GET_GUILD` | Returns the guild object for the given id | `guild_id`, `with_counts` | Guild object |
| `DISCORDBOT_LIST_GUILD_MEMBERS` | Returns a list of guild member objects | `guild_id`, optional filters | Array of member objects |
| `DISCORDBOT_UPDATE_GUILD_MEMBER` | Modifies attributes of a guild member | `guild_id`, `user_id`, fields to update | Updated member object |
| `DISCORDBOT_BAN_USER_FROM_GUILD` | Bans a user from a guild | `guild_id`, `user_id`, optional settings | Success status |
| `DISCORDBOT_UNBAN_USER_FROM_GUILD` | Removes the ban for a user | `guild_id`, `user_id` | Success status |
| `DISCORDBOT_LIST_GUILD_BANS` | Returns a list of ban objects | `guild_id`, optional filters | Array of ban objects |
| `DISCORDBOT_GET_GUILD_BAN` | Returns a ban object for the given user | `guild_id`, `user_id` | Ban object |
| `DISCORDBOT_PRUNE_GUILD` | Begins a prune operation | `guild_id`, `days`, optional settings | Prune count |
| `DISCORDBOT_PREVIEW_PRUNE_GUILD` | Returns an object with prune count | `guild_id`, `days`, optional settings | Prune count object |
| `DISCORDBOT_LIST_GUILD_ROLES` | Returns a list of role objects | `guild_id` | Array of role objects |
| `DISCORDBOT_CREATE_GUILD_ROLE` | Creates a new role for the guild | `guild_id`, role settings | Created role object |
| `DISCORDBOT_UPDATE_GUILD_ROLE` | Modifies a guild role | `guild_id`, `role_id`, fields to update | Updated role object |
| `DISCORDBOT_DELETE_GUILD_ROLE` | Deletes a guild role | `guild_id`, `role_id` | Success status |
| `DISCORDBOT_LEAVE_GUILD` | Leaves a guild | `guild_id` | Success status |
| `DISCORDBOT_LIST_GUILD_INVITES` | Returns a list of invite objects | `guild_id` | Array of invite objects |

### Emoji & Sticker Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_GUILD_EMOJI` | Creates a new emoji for the guild | `guild_id`, `name`, `image`, optional `roles` | Created emoji object |
| `DISCORDBOT_GET_GUILD_EMOJI` | Returns an emoji object for the given IDs | `guild_id`, `emoji_id` | Emoji object |
| `DISCORDBOT_UPDATE_GUILD_EMOJI` | Modifies the given emoji | `guild_id`, `emoji_id`, fields to update | Updated emoji object |
| `DISCORDBOT_DELETE_GUILD_EMOJI` | Deletes the given emoji | `guild_id`, `emoji_id` | Success status |
| `DISCORDBOT_LIST_GUILD_EMOJIS` | Returns a list of emoji objects | `guild_id` | Array of emoji objects |
| `DISCORDBOT_CREATE_GUILD_STICKER` | Creates a new sticker for the guild | `guild_id`, `name`, `description`, `tags`, `file` | Created sticker object |
| `DISCORDBOT_GET_GUILD_STICKER` | Returns a sticker object for the given IDs | `guild_id`, `sticker_id` | Sticker object |
| `DISCORDBOT_UPDATE_GUILD_STICKER` | Modifies the given sticker | `guild_id`, `sticker_id`, fields to update | Updated sticker object |
| `DISCORDBOT_DELETE_GUILD_STICKER` | Deletes the given sticker | `guild_id`, `sticker_id` | Success status |
| `DISCORDBOT_LIST_GUILD_STICKERS` | Returns a list of sticker objects | `guild_id` | Array of sticker objects |
| `DISCORDBOT_LIST_STICKER_PACKS` | Returns the list of sticker packs | None | Array of sticker pack objects |
| `DISCORDBOT_GET_STICKER` | Returns a sticker object for the given ID | `sticker_id` | Sticker object |

### Webhook Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_CREATE_WEBHOOK` | Creates a webhook in a channel | `channel_id`, `name`, optional `avatar` | Created webhook object |
| `DISCORDBOT_GET_WEBHOOK` | Returns the webhook object for the given id | `webhook_id` | Webhook object |
| `DISCORDBOT_UPDATE_WEBHOOK` | Modifies a webhook | `webhook_id`, fields to update | Updated webhook object |
| `DISCORDBOT_DELETE_WEBHOOK` | Deletes a webhook permanently | `webhook_id` | Success status |
| `DISCORDBOT_GET_WEBHOOK_BY_TOKEN` | Returns the webhook object using its token | `webhook_id`, `webhook_token` | Webhook object |
| `DISCORDBOT_UPDATE_WEBHOOK_BY_TOKEN` | Modifies a webhook using its token | `webhook_id`, `webhook_token`, fields to update | Updated webhook object |
| `DISCORDBOT_DELETE_WEBHOOK_BY_TOKEN` | Deletes a webhook using its token | `webhook_id`, `webhook_token` | Success status |
| `DISCORDBOT_EXECUTE_WEBHOOK` | Executes a webhook | `webhook_id`, `webhook_token`, message content | Message object or success status |
| `DISCORDBOT_EXECUTE_SLACK_COMPATIBLE_WEBHOOK` | Executes a webhook in Slack-compatible mode | `webhook_id`, `webhook_token`, Slack payload | Message object or success status |
| `DISCORDBOT_EXECUTE_GITHUB_COMPATIBLE_WEBHOOK` | Executes a webhook in GitHub-compatible mode | `webhook_id`, `webhook_token`, GitHub payload | Message object or success status |
| `DISCORDBOT_GET_WEBHOOK_MESSAGE` | Returns a previously-sent webhook message | `webhook_id`, `webhook_token`, `message_id` | Message object |
| `DISCORDBOT_UPDATE_WEBHOOK_MESSAGE` | Edits a previously-sent webhook message | `webhook_id`, `webhook_token`, `message_id`, new content | Updated message object |
| `DISCORDBOT_DELETE_WEBHOOK_MESSAGE` | Deletes a message that was created by the webhook | `webhook_id`, `webhook_token`, `message_id` | Success status |
| `DISCORDBOT_GET_ORIGINAL_WEBHOOK_MESSAGE` | Returns the original interaction message | `webhook_id`, `webhook_token` | Original message object |
| `DISCORDBOT_UPDATE_ORIGINAL_WEBHOOK_MESSAGE` | Edits the original interaction message | `webhook_id`, `webhook_token`, new content | Updated message object |
| `DISCORDBOT_DELETE_ORIGINAL_WEBHOOK_MESSAGE` | Deletes the original interaction message | `webhook_id`, `webhook_token` | Success status |
| `DISCORDBOT_LIST_CHANNEL_WEBHOOKS` | Returns a list of channel webhook objects | `channel_id` | Array of webhook objects |
| `DISCORDBOT_GET_GUILD_WEBHOOKS` | Returns a list of guild webhook objects | `guild_id` | Array of webhook objects |

### Invite & Template Management Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_INVITE_RESOLVE` | Returns an invite object for the given code | `invite_code`, optional filters | Invite object |
| `DISCORDBOT_INVITE_REVOKE` | Deletes an invite | `invite_code` | Success status |
| `DISCORDBOT_CREATE_GUILD_FROM_TEMPLATE` | Creates a new guild based on a template | `template_code`, `name`, optional `icon` | New guild object |
| `DISCORDBOT_GET_GUILD_TEMPLATE` | Returns a guild template object | `template_code` | Template object |
| `DISCORDBOT_UPDATE_GUILD_TEMPLATE` | Modifies the template's metadata | `template_code`, fields to update | Updated template object |
| `DISCORDBOT_SYNC_GUILD_TEMPLATE` | Syncs the template to the guild's current state | `guild_id`, `template_code` | Updated template object |
| `DISCORDBOT_DELETE_GUILD_TEMPLATE` | Deletes the template | `template_code` | Success status |
| `DISCORDBOT_LIST_GUILD_TEMPLATES` | Returns an array of guild template objects | `guild_id` | Array of template objects |
| `DISCORDBOT_CREATE_GUILD_TEMPLATE` | Creates a template for the guild | `guild_id`, `name`, optional `description` | Template object |

### Miscellaneous / Utility Tools

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `DISCORDBOT_FOLLOW_CHANNEL` | Follows a News Channel to send messages to a target channel | `channel_id`, `webhook_channel_id` | Success status |
| `DISCORDBOT_TRIGGER_TYPING_INDICATOR` | Posts a typing indicator for the specified channel | `channel_id` | Success status |
| `DISCORDBOT_CROSSPOST_MESSAGE` | Crossposts a message in a News Channel | `channel_id`, `message_id` | Crossposted message object |
| `DISCORDBOT_LIST_VOICE_REGIONS` | Returns an array of voice region objects | None | Array of voice region objects |
| `DISCORDBOT_CREATE_DM` | Creates a new DM channel with a user | `recipient_id` | DM channel object |
| `DISCORDBOT_CREATE_GROUP_DM_USER` | Creates a new group DM channel with multiple users | `access_tokens`, optional `nicks` | Group DM channel object |
| `DISCORDBOT_GET_GATEWAY` | Gets the gateway URL and recommended number of shards | None | Gateway object |
| `DISCORDBOT_GET_BOT_GATEWAY` | Gets the gateway URL and recommended number of shards for the bot | None | Bot gateway object |
| `DISCORDBOT_GET_PUBLIC_KEYS` | Gets public keys for verifying interaction payloads | None | Public keys object |

## Configuration Options

The server supports various configuration options through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token (required) | None |
| `DISCORD_API_BASE` | Discord API base URL | `https://discord.com/api/v10` |
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | `30.0` |

## Production Features

This server includes production-ready features:

- **Connection Pooling**: Efficient HTTP client with connection pooling
- **Rate Limiting**: Built-in rate limiting with exponential backoff
- **Retry Logic**: Automatic retry for failed requests
- **Error Handling**: Comprehensive error handling with detailed messages
- **File Upload Support**: Support for file uploads up to 25MB
- **Health Monitoring**: Built-in health check capabilities

## Security

- Bot tokens are loaded from environment variables (never hardcoded)
- Automatic `.env` file loading for easy configuration
- Secure HTTP client with proper timeout handling
- Input validation for all parameters

# Discord Webhook Tools Comparison

## 🔧 Available Webhook Tools

### 1. DISCORDBOT_EXECUTE_WEBHOOK ⭐ (Recommended)
**Purpose**: Send rich Discord messages with full Discord features

**Parameters**:
- `webhook_id` (str): Webhook ID
- `webhook_token` (str): Webhook token
- `content` (Optional[str]): Message content (max 2000 chars)
- `username` (Optional[str]): Override webhook username
- `avatar_url` (Optional[str]): Override webhook avatar
- `tts` (bool): Text-to-speech
- `embeds` (Optional[List[Dict]]): Rich embeds
- `components` (Optional[List[Dict]]): Buttons, select menus
- `files` (Optional[List]): File uploads
- `attachments` (Optional[List[Dict]]): Attachment objects
- `flags` (Optional[int]): Message flags
- `thread_name` (Optional[str]): Thread creation
- `wait` (bool): Wait for message creation

**Use Case**: Full Discord integration, rich messages, file uploads, interactive components

---

### 2. DISCORDBOT_EXECUTE_SLACK_COMPATIBLE_WEBHOOK
**Purpose**: Send messages using Slack's webhook format

**Parameters**:
- `webhook_id` (str): Webhook ID
- `webhook_token` (str): Webhook token
- `payload` (Dict[str, Any]): Slack-compatible payload
- `wait` (bool): Wait for message creation
- `thread_id` (Optional[str]): Thread ID

**Payload Format**:
```json
{
  "text": "Hello from Slack!",
  "attachments": [
    {
      "color": "good",
      "title": "Notification",
      "text": "This is a test message"
    }
  ]
}
```

**Use Case**: Migrating from Slack, integrating with Slack-compatible systems

---

### 3. DISCORDBOT_EXECUTE_GITHUB_COMPATIBLE_WEBHOOK
**Purpose**: Send messages using GitHub's webhook format

**Parameters**:
- `webhook_id` (str): Webhook ID
- `webhook_token` (str): Webhook token
- `payload` (Dict[str, Any]): GitHub-compatible payload
- `wait` (bool): Wait for message creation
- `thread_id` (Optional[str]): Thread ID

**Payload Format**:
```json
{
  "sender": {
    "login": "username",
    "id": 12345,
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "html_url": "https://github.com/username"
  },
  "repository": {
    "name": "repo-name",
    "full_name": "owner/repo-name",
    "id": 123456789,
    "html_url": "https://github.com/owner/repo-name"
  },
  "action": "test"
}
```

**Use Case**: GitHub integration, CI/CD notifications, repository events

---

## 📊 Feature Comparison Table

| Feature | Standard Webhook | Slack-Compatible | GitHub-Compatible |
|---------|------------------|------------------|-------------------|
| **Rich Embeds** | ✅ Full Discord embeds | ❌ Limited attachments | ❌ Limited attachments |
| **Components** | ✅ Buttons, select menus | ❌ Not supported | ❌ Not supported |
| **File Uploads** | ✅ Multiple files | ❌ Limited support | ❌ Limited support |
| **Thread Support** | ✅ `thread_name` parameter | ✅ `thread_id` parameter | ✅ `thread_id` parameter |
| **Complexity** | 🔴 More parameters | 🟢 Simple payload | 🔴 Complex payload |
| **Reliability** | ✅ High | 🟡 Medium | 🔴 Low (strict format) |
| **Migration** | ❌ Discord-specific | ✅ Easy from Slack | ✅ Easy from GitHub |
| **Use Case** | General Discord integration | Slack migration | GitHub integration |

---

## 🎯 When to Use Which

### Use DISCORDBOT_EXECUTE_WEBHOOK when:
- ✅ Building Discord-native integrations
- ✅ Need rich embeds, components, file uploads
- ✅ Want maximum Discord features
- ✅ Sending custom messages

### Use DISCORDBOT_EXECUTE_SLACK_COMPATIBLE_WEBHOOK when:
- ✅ Migrating from Slack to Discord
- ✅ Integrating with existing Slack webhook systems
- ✅ Need simple, text-based messages
- ✅ Working with Slack-compatible tools

### Use DISCORDBOT_EXECUTE_GITHUB_COMPATIBLE_WEBHOOK when:
- ✅ GitHub integration notifications
- ✅ CI/CD pipeline notifications
- ✅ Repository event notifications
- ✅ Issue/PR notifications

---

## 🚨 Important Notes

- **Standard Webhook** is the most reliable and feature-rich
- **Slack-Compatible** is good for simple messages and Slack migration
- **GitHub-Compatible** is complex and requires exact GitHub webhook format
- All tools support the same webhook ID and token
- Thread support varies between tools (use `thread_name` vs `thread_id`)

**Recommendation**: Start with the **Standard Webhook** for most use cases, only use the compatible webhooks when specifically migrating from Slack/GitHub systems.
