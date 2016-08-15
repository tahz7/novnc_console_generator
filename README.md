# novnc console generator


### description:

The novnc link generator is used to generate novnc console links for Rackspace Cloud servers. The script will ask your user, api key and server id and then generate a new link for you.

 * It automatically generates the API token
 * Detects whether the account is UK or US 
 * Finds the region the server belongs to and grabs the console link.

### requirements:

 * tested to work with python 2.6/2.67
 * Your mycloud.rackspace.com username. Your API key (this can be found in your control panel -> top right click your username -> account settings -> show api key). Your server id, click your server name in your control panel and the ID is listed in the details. 

### example usage:

You can run this script via curl or locally, with or without command line arguments;

```
curl -s https://raw.githubusercontent.com/tahz89/novnc_console_generator/master/novnc_console_generator.py | python

python novnc_console_generator.py
```

```
curl -s https://raw.githubusercontent.com/tahz89/novnc_console_generator/master/novnc_console_generator.py | python - -u username -k api_key -s server_id

python novnc_console_generator.py -u username -k api_key -s server_id
```

