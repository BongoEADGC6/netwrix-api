# Netwrix Search API Module
[![Build Status](https://travis-ci.org/BongoEADGC6/netwrix-api.svg?branch=master)](https://travis-ci.org/BongoEADGC6/netwrix-api)

This is a python3 library to interact with [Netwrix Auditor](https://www.netwrix.com/auditor.html) 

```
pip install netwrix-api
```

Example:
```
from netwrix_api import NetwrixAPI


filter_data = {
    "what": {"Contains": "GroupTest"},
    "datasource": "Active Directory",
    "objecttype": {"Contains": "Group"}
}
netwrix_host = "netwrixsv01.contoso.com"
username = "Username"
passwd = "ENTERPASSOWRD"
api = NetwrixAPI(netwrix_host, username, passwd)
results = api.queryDB(filter_data)
```
