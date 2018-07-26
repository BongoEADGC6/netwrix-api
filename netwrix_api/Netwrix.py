#!/usr/bin/python3

import sys
import requests
import json
import logging
import pprint


class NetwrixAPI:
    def __init__(self, host, api_user, api_pass, port="9699"):
        endpoint_uri = "netwrix/api/v1"
        self.root_api_url = "https://{}:{}/{}".format(host, port, endpoint_uri)
        self.headers = {}
        self.user = api_user
        self.passwd = api_pass
#        api_status_url = self.root_api_url + ""
#        api_status = requests.get(api_status_url,
#                                  auth=(self.user, self.passwd),
#                                  verify=False)
#        api_status.raise_for_status()

    def postRequest(self, request_url, headers, data=None, ssl_verify=False):
        logging.info("Requested URL: {}".format(request_url))
        request_args = {
            'headers': headers,
            'auth': (self.user, self.passwd),
            'verify': ssl_verify
            }
        if data is not None:
            request_args['data'] = json.dumps(data)
        logging.info("Request Args: {}".format(request_args))
        response = requests.post(request_url, **request_args)
        logging.debug(response.json())
        if 200 <= response.status_code <= 299:
            query_count = len(response.json()['ActivityRecordList'])
            if query_count == 0:
                logging.info("Query returned 0 results")
                return None
            else:
                return response.json()
        elif response.status_code == 404 and\
                response.json()['status'] == "No objects found.":
            print("API was Unable to complete query -- Response: {} - {}"
                  .format(response.status_code, response.json()['status']))
            sys.exit(1)
        elif response.status_code == 401:
            print("API was Unable to complete query -- Response: {} - {}"
                  .format(response.status_code, response.json()['status']))
            sys.exit(1)
        elif response.status_code == 500:
            print("API Response - {} - {}".format(response.json()['status'],
                                                  response.json()['errors']))
            sys.exit(1)
        else:
            logging.debug("Returned Data: {}".format(response.json()))
            response.raise_for_status()

    def queryDB(self, filter_data, count=None, output_format="json"):
        query_url = "{}/activity_records/search"\
            .format(self.root_api_url)
        event_filter = self._build_filter(**filter_data)
        self.headers['Content-Type'] = 'application/json'
        query_return = self.postRequest(query_url,
                                        self.headers,
                                        data=event_filter)
        return query_return

    def _build_filter(self, datasource, who=None, where=None,
                      objecttype=None, what=None, monitoring_plan=None,
                      item=None, workstation=None, detail=None, action=None,
                      when=None, before=None, after=None):
        # See https://helpcenter.netwrix.com/API/Filter_Filters.html
        # for details about filters and operators
        event_filter = {
                'FilterList': {}
                }
        filter_list = event_filter['FilterList']
        if who is not None:
            filter_list['Who'] = who
        if where is not None:
            filter_list['Where'] = where
        if objecttype is not None:
            filter_list['ObjectType'] = objecttype
        if what is not None:
            filter_list['What'] = what
        if datasource is not None:
            filter_list['DataSource'] = datasource
        if monitoring_plan is not None:
            filter_list['Monitoring Plan'] = monitoring_plan
        if item is not None:
            filter_list['Item'] = item
        if workstation is not None:
            filter_list['Workstation'] = workstation
        if detail is not None:
            filter_list['Detail'] = detail
        if action is not None:
            filter_list['Action'] = action
        if when is not None:
            filter_list['When'] = when
        if before is not None:
            filter_list['Before'] = before
        if after is not None:
            filter_list['After'] = after
        return event_filter


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    filter_data = {
        "what": {"Contains": "ElasticGroupTest"},
        "datasource": "Active Directory",
        "objecttype": {"Contains": "Group"}
        }
    netwrix_host = "nenetwrixsv01.radnet.rdlx.pvt"
    username = "RADNET\\SA-Icinga"
    passwd = "vBDnZt9y7tUBZKp5gucdoo"
    api = NetwrixAPI(netwrix_host, username, passwd)
    results = api.queryDB(filter_data)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(results['ActivityRecordList'])
