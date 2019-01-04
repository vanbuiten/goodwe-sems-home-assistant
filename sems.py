#!/usr/bin/env python3
import voluptuous as vol

import json
import logging
# import urllib.request
import requests
from bs4 import BeautifulSoup

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['BeautifulSoup4==4.7.0']

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

_LOGGER = logging.getLogger(__name__)

_URL = 'https://www.semsportal.com/home/login'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the GoodWe SEMS portal scraper platform."""
    # Add devices
    add_devices([SemsSensor("SEMS Portal", config)], True)

class SemsSensor(Entity):
    """Representation of the SEMS portal."""

    def __init__(self, name, config):
        """Initialize a SEMS sensor."""
        # self.rest = rest
        self._name = name
        self._config = config
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._attributes['status']

    @property
    def device_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        return self._attributes

    def update(self):
        """Get the latest data from the SEMS API and updates the state."""
        _LOGGER.debug("update called.")
        try:
            login_data = dict(account=self._config.get(CONF_USERNAME), pwd=self._config.get(CONF_PASSWORD))

            session_requests = requests.session()
            r = session_requests.post(_URL, data=login_data)

            htmlresponse = json.loads(r.text).get('data').get('redirect') # Convert response to dict
            url = "https://www.semsportal.com" + htmlresponse

            result = session_requests.get(url, headers = dict(referer = url) )
            htmlcontent= result.content # transform the result to html content

            _LOGGER.debug("HTML content received")

            soup = BeautifulSoup(htmlcontent, 'html.parser')

            _LOGGER.debug("HTML content parsed")
            _LOGGER.debug("update finished. result=%s", soup)

            
            # Filtering
            data = soup.find_all("script")[19].string
            filter1 = str(soup).split("var pw_info = ")[1]
            filter2 = str(filter1).split("var pw_id = ")[0]
            filter3 = filter2.split(";")[0]

            filter4 = json.loads(filter3)
            filter5 = dict(filter4)


            for k, v in filter4['inverter'][0]['invert_full'].items():
                # payload_dict = {}
                key = k
                value = v
                self._attributes[key] = value
                _LOGGER.debug("Updated attribute %s: %s", key, value)
        except Exception as e:
            _LOGGER.error(
                "Unable to fetch data from SEMS. %s", e)
