# ntfy.sh Home Assistant Notifications

The `ntfy.sh` notification platform enables you to easily send notifications with a custom prioirty and extra information via [ntfy.sh](https://ntfy.sh).

### Installation
The recommended way to install the integration is via [HACS](https://hacs.xyz/). Add this repository to HACS custom integration repositories and install.
If you want to install it manually download the repository as zip and extract it to the `<config_dir>/custom_components/` directory of HomeAssistant.

### Configuration
This integration exposes itself as a [notifications integration](https://www.home-assistant.io/integrations/notify/) and configured by adding the folowing snippet to the `configuration.yaml` file:
```yaml
notify:
  - name: "my ntfy"
    platform: ntfy
    url: <ntfy.sh_url>
    token: <ntfy.sh_token>
    topic: <ntfy.sh_topic>
    icon: <notification_icon_url>
```
Replace `<ntfy.sh_url>`, `<ntfy.sh_token>`, `<ntfy.sh_topic>`, and `<notification_icon_url>` with the url, optional token, optional topic, and optional icon url for your ntfy.sh instance. Token is optional if your instance does not require authentication. Topic is also optional and will default to `homeassistant` if not specified. Topics in the automations have higher priority.

### Usage
This integration accepts the same values as the official ntfy.sh API. For a full list of options that can be added to a notification refer to the [ntfy.sh docs](https://docs.ntfy.sh/publish/#publish-as-json). Here a few examples:

#### Simple text message
```yaml
action:
  - service: notify.my_ntfy
    data:
      message: "This is a test message."
```

#### Message with title and priority
```yaml
action:
  - service: notify.my_ntfy
    data:
      message: "This is a test message."
      title: "ntfy Test"
      data:
        priority: 10
```

#### Message with click event
```yaml
action:
  - service: notify.my_ntfy
    data:
      message: "This is a test message."
      title: "ntfy Test"
      data:
        priority: 10
        click: https://www.home-assistant.io/
```

##### Message with image
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
      title: "Gotify Test"
      data:
        priority: 10
        image: https://placekitten.com/400/300
```

##### All available options
```yaml
action:
  - service: notify.my_gotify
    data:
      message: "This is a test message."
      title: "Gotify Test"
      topic: "override_default_topic"
      data:
        tags: [tags]
        priority: 3
        attach: https://placekitten.com/400/300
        filename: filename.jpg
        click: https://www.home-assistant.io/
        actions: [list_of_actions]
        icon: https://placekitten.com/400/300
        delay: 10s
        markdown: True
        call: "+324793245"
        email: "support@home-assistant.io"
```

### License
The whole project is under the [GPL-3 license](https://www.gnu.org/licenses/gpl-3.0.html).
