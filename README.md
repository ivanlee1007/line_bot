# Line Bot
Home Assistant custom component for notifying message via Line Messaging API (https://developers.line.biz/en/docs/messaging-api/overview/)

## Unreleased
- Added public HA sensor `sensor.line_bot_alias_registry` for browsing registered aliases in UI without exposing raw `chat_id`
- Keeps detailed alias-to-`chat_id` mapping in `line_bot.list_chats` only

## What's new in 0.0.7
- Updated repo links and Home Assistant metadata to point to this fork (`ivanlee1007/line_bot`)
- Prevents docs / HACS helper links from sending users to the old upstream repo

## What's new in 0.0.6
- Added `line_bot.list_chats` service so users can see the currently registered alias list
- Service response can include alias only, or alias + raw `chat_id`
- Makes it easier to discover valid `to:` targets before using notification automations

## What's new in 0.0.5
- Added manual alias + `chat_id` entry in the Add a chat UI
- You can now register chats without waiting for webhook-discovered New Messages
- Existing New Messages selection flow remains supported
- Added validation for duplicate alias and mixed manual/selector input

### How to get a `user_id` or `group_id` manually
If you do not want to rely on the built-in New Messages discovery flow, you can obtain a LINE `user_id` or `group_id` externally and enter it manually.

One practical method is to use <https://webhook.site/> as a temporary webhook receiver:

1. Create a temporary URL at `webhook.site`.
2. Set that URL as your LINE Messaging API webhook URL.
3. Send a message to the bot (for a direct chat) or send a message in the group where the bot is present.
4. Inspect the webhook payload captured by `webhook.site`.
5. Copy the value from:
   - `events[0].source.userId` for a direct chat
   - `events[0].source.groupId` for a group chat
6. Open the Line Bot integration UI, choose **Add a chat**, and manually enter:
   - **Alias**: any friendly name you want
   - **Chat ID**: the copied `userId` or `groupId`

This allows you to register a chat without waiting for the integration to discover it from stored New Messages.

## What's new in 0.0.4
- Added direct `chat_id` support for `line_bot.send_message`
- Added direct `chat_id` support for `line_bot.send_button_message`
- Added direct `chat_id` support for `line_bot.send_confirm_message`
- Exposed `chat_id` in `services.yaml` so Home Assistant service UI/schema can show the field
- Existing alias-based `to` usage remains supported

## Usage
```
service: line_bot.send_message
data:
  to: me
  message:
    type: text
    text: "Hello World!"
```

Or send directly to a raw LINE chat id without pre-registering an alias:

```yaml
service: line_bot.send_message
data:
  chat_id: "C0bd3f7f1963a78c479b9170a238cbf6f"
  message:
    type: text
    text: "Hello Group!"
```

## Prequisite
- Created a channel from Line Console.
    - Follow instructions from the [link](https://developers.line.biz/en/docs/messaging-api/getting-started/) to create a new channel.

## Installation

1. Install via custom component of HACS.

   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ivanlee1007&repository=line_bot&category=integration)
2. Go to https://developers.line.biz/console
3. Retrieve "Channel access token" and "Channel secret" from Line Console

4. Install integration
    - [Settings] > [Devices and Services] > [Add Integration] > [Line Bot]
    - Use "Channel access token" and "Channel secret" retrieved from above (#3).
        <img width="302" alt="스크린샷 2024-12-22 오후 9 00 33" src="https://github.com/user-attachments/assets/b5a8fc74-d2f7-415a-8c03-10f3fab4e46f" />


5. Set "Webhook URL" from "Messaging API" tab of Line Console as below
    - Webhook URL is base_url + "/api/line/callback"
    - Your HomeAssistant URL has to support https

    <img width="300" alt="스크린샷 2024-12-22 오후 9 13 12" src="https://github.com/user-attachments/assets/7c1de92c-e44d-492e-950a-5e11946bb5a2" />
    
   
6. Click "Verify" button to verify URL is valid. It has to return "Success"

    ![11](https://user-images.githubusercontent.com/2917984/69878717-081d6900-1309-11ea-8b08-c319bd4b333a.png)

7. Add a bot as a friend by either QR code or Bot ID
8. Send any message to a bot
9. Go to [Configure > Add a chat] and follow the directions.

    configure | add a chat | configure a chat
    --|--|--
    <img width="442" src="https://github.com/user-attachments/assets/63ddeb48-6248-4488-813a-429b8f993a85" /> | <img width="400" src="https://github.com/user-attachments/assets/20475b4b-c2d1-4ee2-bc8a-0ede595f7da7" /> | <img width="400" src="https://github.com/user-attachments/assets/f581c3c7-139a-44ec-8707-5badc4c00f4b" />

10. Try [examples](https://github.com/ivanlee1007/line_bot/tree/master/examples)

## Services
### line_bot.send_message
| service data attribute | required | dataType | description
| --- | --- | --- | ---
| **to** | no | string | name of chat ID from `allowed_chat_ids` in `configuration.yaml` file to push message.
| **chat_id** | no | string | raw LINE user/group/room id to push message directly without pre-registering an alias.
| **reply_token** | no | string | reply_token received from webhook [event](https://developers.line.biz/en/reference/messaging-api/#message-event) to reply message.
| **message** | yes | [Message](https://developers.line.biz/en/reference/messaging-api/#message-objects) | eg. [Text message](https://developers.line.biz/en/reference/messaging-api/#text-message), [Image message](https://developers.line.biz/en/reference/messaging-api/#image-message),[Template message](https://developers.line.biz/en/reference/messaging-api/#template-messages), etc...
#### Example 1. [Text Message](https://developers.line.biz/en/reference/messaging-api/#text-message)
![a1](https://user-images.githubusercontent.com/2917984/69494729-580fc080-0f02-11ea-8231-6d0dde9bae14.png)
```yaml
service: line_bot.send_message
data:
  to: me
  message:
    type: text
    text: "Hello World!"
```

#### Example 1b. [Text Message by raw chat_id](https://developers.line.biz/en/reference/messaging-api/#text-message)
```yaml
service: line_bot.send_message
data:
  chat_id: "C0bd3f7f1963a78c479b9170a238cbf6f"
  message:
    type: text
    text: "Hello Group!"
```

#### Example 2. [Image Message](https://developers.line.biz/en/reference/messaging-api/#image-message)

<img width="300" height="178" src="https://github.com/user-attachments/assets/df60bdca-be60-45fc-b355-b994ccec1496" />

```yaml
action: line_bot.send_message
data:
  to: me
  message:
    type: image
    originalContentUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    previewImageUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
```

#### Example 3. [Location Message](https://developers.line.biz/en/reference/messaging-api/#location-message)

<img width="301" height="98" src="https://github.com/user-attachments/assets/1d3dd88c-3bf8-4e4a-9ee5-516ab6fc720b" />

```yaml
action: line_bot.send_message
data:
  to: me
  message:
    type: image
    originalContentUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    previewImageUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
```

### line_bot.send_button_message

| service data attribute | required | dataType | description
| --- | --- | --- | ---
| **to** | no | string | name of chat ID from `allowed_chat_ids` in `configuration.yaml` file to push message.
| **chat_id** | no | string | raw LINE user/group/room id to push message directly without pre-registering an alias.
| **reply_token** | no | string | reply_token received from webhook [event](https://developers.line.biz/en/reference/messaging-api/#message-event) to reply message.
| **buttons** | yes | list | a list of [Actions](https://developers.line.biz/en/reference/messaging-api/#action-objects) (max: 4)
#### example
![162292](https://user-images.githubusercontent.com/2917984/69495124-d2424400-0f06-11ea-8688-a3cc704eb73f.jpg)
```yaml
service: line_bot.send_button_message
data:
  to: me
  text: What do you want to do?
  buttons:
    # MessageAction (https://developers.line.biz/en/reference/messaging-api/#message-action)
    - label: Turn off the light
      text: light off
    # PostbackAction (https://developers.line.biz/en/reference/messaging-api/#postback-action)
    - label: Buy
      data: action=buy&itemid=111
    # UriAction (https://developers.line.biz/en/reference/messaging-api/#uri-action)
    - uri: https://www.google.com/
      label: Google
```

### line_bot.send_confirm_message

| service data attribute | required | dataType | description
| --- | --- | --- | ---
| **to** | no | string | name of chat ID from `allowed_chat_ids` in `configuration.yaml` file to push message.
| **chat_id** | no | string | raw LINE user/group/room id to push message directly without pre-registering an alias.
| **reply_token** | no | string | reply_token received from webhook [event](https://developers.line.biz/en/reference/messaging-api/#message-event) to reply message.
| **buttons** | yes | list | a list of [Actions](https://developers.line.biz/en/reference/messaging-api/#action-objects) (max: 2)
#### example
![162289](https://user-images.githubusercontent.com/2917984/69494775-cbb1cd80-0f02-11ea-827a-74955937cc8d.jpg)
```yaml
service: line_bot.send_confirm_message
data:
  to: me
  text: Are you sure?
  buttons:
    # PostbackAction 
    - text: Yes 
      data: action=buy&itemid=111 # equivalent to {"label" : "Yes", "data" : "action=buy&itemid=111 "}
    # MessageAction
    - text: No # equivalent to {"text" : "No", "label" : "No"}
```

### sensor.line_bot_alias_registry

Public alias registry sensor for Home Assistant UI.

- **state**: number of registered aliases
- **attributes**:
  - `aliases`: alias list
  - `updated_at`: last refresh timestamp

This sensor intentionally does **not** expose raw LINE `chat_id` values.
Use `line_bot.list_chats` when you need the detailed mapping for debugging or maintenance.

### line_bot.list_chats

Returns the currently registered alias list from the integration.

| service data attribute | required | dataType | description
| --- | --- | --- | ---
| **include_chat_id** | no | boolean | include raw LINE user/group/room ids in the response. default: `true` |

#### Example: list alias + chat_id
```yaml
action: line_bot.list_chats
data:
  include_chat_id: true
response_variable: line_bot_chats
```

Example response:
```yaml
line_bot_chats:
  count: 2
  aliases:
    - me
    - blueberry
  chats:
    - alias: me
      chat_id: Uxxxxxxxx
    - alias: blueberry
      chat_id: Cxxxxxxxx
  mapping:
    me: Uxxxxxxxx
    blueberry: Cxxxxxxxx
```

#### Example: alias only
```yaml
action: line_bot.list_chats
data:
  include_chat_id: false
response_variable: line_bot_chats
```

## Events
### line_webhook_text_received
| event data attribute | dataType | description
| --- | --- | ---
| **reply_token** | string | It is used to reply message.
| **event** | [MessageEvent](https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#linebot.models.events.MessageEvent) | Event object which contains the sent message. The message field contains a message object which corresponds with the message type. You can reply to message events.
| **content** | [TextMessage](https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#linebot.models.messages.TextMessage) | Message object which contains the text sent from the source.
| **text** | string | actual text received

### line_webhook_postback_received
| event data attribute | dataType | description
| --- | --- | ---
| **reply_token** | string | It is used to reply message.
| **event** | [PostbackEvent](https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#linebot.models.events.PostbackEvent) | Event object for when a user performs an action on a template message which initiates a postback. You can reply to postback events.
| **content** | [Postback](https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#linebot.models.events.Postback) | Postback
| **data** | string | Postback data
| **data_json** | dictionary | Postback data as JSON object
| **params** | dictionary | JSON object with the date and time selected by a user through a datetime picker action. Only returned for postback actions via the datetime picker.
