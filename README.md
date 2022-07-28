# WeeWX OpenHAB
*Pull sensor data from OpenHAB (API) into WeeWX (StdService)*

## Manual installation instructions
1. Put the extension file in your user dir, e.g., for Debian package installations:

    ```
    cp openhab.py /usr/share/weewx/user/
    ```

2. Add the service:

    ```
    [Engine]
        [[Services]]
            ...
            data_services = user.openhab.AddOpenHAB
            ...
    ```

3. Add the configuration:

    First provide the address for your OpenHAB server API.  Then, for each OpenHAB sensor value (either temperature or humidity) you want to pull into WeeWX, add a definition in the form of `weewx_key = OpenHAB_item` in the [[[Mappings]]] section.  If your OpenHAB installation provides temperature data in C, add definition for each WeeWX temperature key you're pulling in the [[[Units]]] section (this is optional if you do not need to convert).  E.g.:

    ```
    [StdService]
        [[AddOpenHAB]]
            openhab_api_url = http://my.openhab.server:8080/rest/items/
            [[[Mappings]]]
                extraTemp1 = ThermostatDrawingRoom_Sensortemperature
                extraHumid1 = ThermostatDrawingRoom_Sensorrelativehumidity
                extraTemp2 = ThermostatOutdoorGarden_Sensortemperature
                extraHumid2 = ThermostatOutdoorGarden_Sensorrelativehumidity
            [[[Units]]]
                extraTemp1 = C
                extraTemp2 = C
    ```

4. Restart WeeWX, e.g., for Debian package installations:

    ```
    sudo systemctl restart weewx
    ```

## License
GNU Public License v3
