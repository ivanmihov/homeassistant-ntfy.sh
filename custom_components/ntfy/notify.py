import logging
import requests
from typing import Any
import voluptuous as vol
from homeassistant.const import (
    CONF_URL,
    CONF_TOKEN,
    CONF_ICON
)

CONF_TOPIC = 'topic'

import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    ATTR_TITLE_DEFAULT,
    ATTR_TITLE,
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_URL): cv.url,
    vol.Optional(CONF_TOKEN): cv.string,
    vol.Optional(CONF_TOPIC): cv.string,
    vol.Optional(CONF_ICON): cv.url
})
_LOGGER = logging.getLogger(__name__)

def get_service(hass, config, discovery_info=None):
    url = config.get(CONF_URL) or 'https://ntfy.sh'
    token = config.get(CONF_TOKEN) or ''
    topic = config.get(CONF_TOPIC)
    icon = config.get(CONF_ICON)

    _LOGGER.info('Service created')

    return HassAgentNotificationService(hass, url, token, topic, icon)


class HassAgentNotificationService(BaseNotificationService):
    def __init__(self, hass, url, token, topic, icon):
        self._url = url
        self._token = token
        self._topic = topic
        self._icon = icon
        self._hass = hass

        # if not self._url.endswith('/'):
        #     self._url += '/'
        # self._url += topic

    def send_request(self, url, token, data):
        headers = {}
        if token != '':
            headers = {'Authorization': 'Bearer ' + token}
        return requests.post(url, headers=headers, json=data, timeout=10)

    async def async_send_message(self, message: str, **kwargs: Any):
        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        data = kwargs.get(ATTR_DATA, None)
        if data is None:
            data = dict()

        # Prefer topic in automation
        topic = data.get('topic') or self._topic or "homeassistant"
        # Prefer icon in automation
        icon = data.get('icon') or self._icon or ""

        payload = {
            "topic": topic,
            "message": message,
            "title": title,
            "tags": data.get("tags", []),
            "priority": data.get("priority", 3),
            "attach": data.get("attach", "") or data.get("image", ""),
            "filename": data.get("filename", ""),
            "click": data.get("click", "") or data.get("click_url", ""),
            "actions": data.get("actions", []),
            "icon": icon,
            "markdown": "markdown" in data,
            "delay": data.get("delay", ""),
            "email": data.get("email", ""),
            "call": data.get("call", ""),
        }

        _LOGGER.debug('Sending message to ntfy.sh: %s', payload)

        try:
            response = await self.hass.async_add_executor_job(self.send_request, self._url, self._token, payload)
            response.raise_for_status()
        except Exception as ex:
            _LOGGER.error('Error while sending ntfy.sh message: %s', ex)
