# Goodwe SEMS scraper for Home Assistant

## Setup

Crude sensor for Home Assistant that scrapes from GoodWe SEMS portal. Copy all the files in `custom_components/sems/` in your Home Assistant config dir:
- `sensor.py`
- `__init__.py`
- `manifest.json`

And update configuration.

Example entry in `configuration.yaml`:

```
sensor:
  - platform: sems
    username: 'XXXX'
    password: 'XXXX'
    scan_interval: 60
```

Use the credentials you use to login to https://www.semsportal.com/. 

`scan_interval` controls how often the sensor updates/scrapes. By default this seems to be every 60 seconds.

## HACS

Note: The repository folder structure is changed in order to be compatible with [HACS](https://custom-components.github.io/hacs/), see [here](https://custom-components.github.io/hacs/#add-custom-repos ) how to add this as custom repo to HACS.
It is also [under submission](https://github.com/custom-components/hacs/pull/111) to be included by default in HACS.

## Screenies

![Overview icon](images/sems-icon.png)

![Detail window](images/sems-details.png)

## Credits

Reuses code from https://github.com/Sprk-nl/goodwe_sems_portal_scraper.
