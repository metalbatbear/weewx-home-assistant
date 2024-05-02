import re
import time
import requests
import weewx
from weewx.engine import StdService

# logging
import weeutil.logger
import logging
log = logging.getLogger(__name__)

class AddHomeAssistant(StdService):

    def __init__(self, engine, config_dict):
        super(AddHomeAssistant, self).__init__(engine, config_dict)
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        self.last_total = None

        try:
            self.svc_dict = config_dict['StdService']['AddHomeAssistant']
        except KeyError as e:
            log.error("Will not pull from Home Assistant API: Missing option %s" % e)
            return

        log.debug("Using Home Assistant API url %s" % self.svc_dict['home-assistant_api_url'])

    def query_api(self, item_name):
        packet = dict()
        packet["dateTime"] = int(time.time())
        packet["usUnits"] = weewx.US

        # contruct query
        query_url = self.svc_dict['home-assistant_api_url'] + item_name
        log.debug("Using query url %s" % query_url)

        # assemble headers
        headers = {
            'Authorization': 'Bearer ' + self.svc_dict['home-assistant_api_token'],
            'content-type': 'application/json',
        }

        # send query
        try:
            response = requests.get(query_url, headers=headers)
        except requests.Timeout as error:
            log.error("Message: %s" % error)
        except requests.RequestException as error:
            log.error("RequestException: %s" % error)

        # extract value
        try:
            data = response.json()
        except:
            packet = 'null'
            log.error("Cannot obtain data for " + item_name)
        else:
            packet = data["state"]
            log.debug("%s: %s" % (item_name, packet))

        return packet

    def new_archive_record(self, event):

        # query user-provided key/value combos from [[[Mappings]]]
        for key in self.svc_dict['Mappings']:
            # strip anything after the first set of digits
            results = re.findall('\d+', self.query_api(self.svc_dict['Mappings'][key]))

            # check that the HA system returned a valid result
            try:
                result = float(results[0])
            except:
                break

            # if a unit C specified, convert; otherwise assume F
            try:
                unit = self.svc_dict['Units'][key]
            except:
                result = float(results[0])
                log.debug("No unit specified for %s" % (key))
            else:
                if unit == "C":
                    result = float(results[0]) * 1.8 + 32
                else:
                    result = float(results[0])
                    log.debug("Unit %s specified for %s, but only C is supported; will not convert" % (unit, key))

            # record value
            event.record[key] = result
            log.debug("key %s = %s = %s" % (key, self.svc_dict['Mappings'][key], result))
