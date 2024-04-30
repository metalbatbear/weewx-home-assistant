# WeeWX Home Assistant
*Pull sensor data from Home Assistant (API) into WeeWX (StdService)*

## Manual installation instructions
1. Put the extension file in your user dir, e.g., for Debian package installations:

    ```
    cp home-assistant.py /usr/share/weewx/user/
    ```

2. Add the service:

    ```
    [Engine]
        [[Services]]
            ...
            data_services = user.home-assistant.AddHomeAssistant
            ...
    ```

3. Add the configuration:

    First provide the address for your Home Assistant server API.  Then, for each Home Assistant sensor value (either temperature or humidity) you want to pull into WeeWX, add a definition in the form of `weewx_key = HomeAssistant_item` in the [[[Mappings]]] section.  If your Home Assistant installation provides temperature data in C, add definition for each WeeWX temperature key you're pulling in the [[[Units]]] section (this is optional if you do not need to convert).  E.g.:

    ```
    [StdService]
        [[AddHomeAssistant]]
            home-assistant_api_url = http://my.home-assistant.server:8123/api/states/
            home-assistant_api_token = token_obtained_from_home-assistant_settings_page
            [[[Mappings]]]
                extraTemp1 = sensor.drawingroom_thermostat_air_temperature
                extraHumid1 = sensor.drawingroom_thermostat_humidity
                extraTemp2 = sensor.outdoorgarden_thermostat_air_temperature
                extraHumid2 = sensor.outdoorgarden_thermostat_humidity
            [[[Units]]]
                extraTemp1 = F
                extraTemp2 = F
    ```

4. Restart WeeWX, e.g., for Debian package installations:

    ```
    sudo systemctl restart weewx
    ```

## License
GNU Public License v3
