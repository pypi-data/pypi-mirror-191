# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ha_mqtt_discoverable', 'ha_mqtt_discoverable.cli']

package_data = \
{'': ['*']}

install_requires = \
['gitlike-commands>=0.2.1,<0.3.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'thelogrus>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hmd = ha_mqtt_discoverable.cli.main_driver:hmd_driver',
                     'hmd-create-binary-sensor = '
                     'ha_mqtt_discoverable.cli.sensor_driver:create_binary_sensor',
                     'hmd-create-device = '
                     'ha_mqtt_discoverable.cli.device_driver:create_device',
                     'hmd-version = ha_mqtt_discoverable.cli:module_version']}

setup_kwargs = {
    'name': 'ha-mqtt-discoverable',
    'version': '0.4.2',
    'description': '',
    'long_description': '<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [ha-mqtt-discoverable](#ha-mqtt-discoverable)\n  - [Installing](#installing)\n    - [Python](#python)\n    - [Docker](#docker)\n  - [Supported Types](#supported-types)\n    - [Binary Sensors](#binary-sensors)\n      - [Usage](#usage)\n    - [Devices](#devices)\n      - [Usage](#usage-1)\n  - [Scripts Provided](#scripts-provided)\n    - [`hmd`](#hmd)\n    - [`hmd create binary sensor`](#hmd-create-binary-sensor)\n    - [`hmd create device`](#hmd-create-device)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n# ha-mqtt-discoverable\n\nA python 3 module that takes advantage of HA(Home Assistant(\'s MQTT discovery protocol to create sensors without having to define anything on the HA side.\n\nUsing MQTT discoverable devices lets us add new sensors and devices to HA without having to restart HA. This module includes scripts to make it easy to create discoverable devices from the command line if you don\'t want to bother writing python.\n\n## Installing\n\n### Python\n\n`pip install ha-mqtt-discoverable` if you want to use it in your python scripts. This will also install the `hmd` utility scripts.\n\n### Docker\n\nIf all you want to do is use the command line tools, the simplest way is to use them with `docker` or `nerdctl`. It won\'t interfere with your system python and potentially cause you issues there. You can use the [unixorn/ha-mqtt-discoverable](https://hub.docker.com/repository/docker/unixorn/ha-mqtt-discoverable) image on dockerhub directly, but if you add `$reporoot/bin` to your `$PATH`, the `hmd` script in there will automatically run the command line tools inside a docker container with `docker` or `nerdctl`, depending on what it finds in your `$PATH`.\n\n## Supported Types\n\n### Binary Sensors\n\n#### Usage\n\nHere is an example that creates a binary sensor.\n\n```py\nfrom ha_mqtt_discoverable.sensors import BinarySensor\n\n# Create a settings dictionary\n#\n# Mandatory Keys:\n#  mqtt_server\n#  mqtt_user\n#  mqtt_password\n#  device_id\n#  device_name\n#  device_class\n#\n# Optional Keys:\n#  mqtt_prefix - defaults to homeassistant\n#  payload_off\n#  payload_on\n#  unique_id\n\nconfigd = {\n    "mqtt_server": "mqtt.example.com",\n    "mqtt_prefix": "homeassistant",\n    "mqtt_user": "mqtt_user",\n    "mqtt_password": "mqtt_password",\n    "device_id": "device_id",\n    "device_name":"MySensor",\n    "device_class":"motion",\n}\n\nmysensor = BinarySensor(settings=configd)\nmysensor.on()\nmysensor.off()\n\n```\n\n### Devices\n\n#### Usage\n\nHere\'s an example that will create a MQTT device and add multiple sensors to it.\n\n```py\nfrom ha_mqtt_discoverable.device import Device\n\n# Create a settings dictionary\n#\n# Mandatory Keys:\n#  mqtt_server\n#  mqtt_user\n#  mqtt_password\n#  device_id\n#  device_name\n#  device_class\n#  unique_id\n#\n# Optional Keys:\n#  client_name\n#  manufacturer\n#  model\n#  mqtt_prefix - defaults to homeassistant\n\nconfigd = {\n    "mqtt_server": "mqtt.example.com",\n    "mqtt_prefix": "homeassistant",\n    "mqtt_user": "mqtt_user",\n    "mqtt_password": "mqtt_password",\n    "device_id": "device_id",\n    "device_name":"MySensor",\n    "device_class":"motion",\n    "manufacturer":"Acme Products",\n    "model": "Rocket Skates",\n}\n\ndevice = Device(settings=configd)\n\n# You can add more than one metric to a device\ndevice.add_metric(\n    name="Left skate thrust",\n    value=33,\n    configuration={"name": f"Left Skate Thrust"},\n)\ndevice.add_metric(\n    name="Right skate thrust",\n    value=33,\n    configuration={"name": f"Right Skate Thrust"},\n)\n\n# Nothing gets written to MQTT until we publish\ndevice.publish()\n\n# Do your own code\n\n# If we add a metric using the same name as an existing metric, the value is updated\ndevice.add_metric(\n    name="Right skate thrust",\n    value=99,\n    configuration={"name": f"Right Skate Thrust"},\n)\ndevice.publish()\n```\n\n## Scripts Provided\n\nThe `ha_mqtt_discoverable` module also installs the following helper scripts you can use in your own shell scripts.\n\n### `hmd`\n\nUses the [gitlike-commands](https://github.com/unixorn/gitlike-commands/) module to find and execute `hmd` subcommands. Allows you to run `hmd create binary sensor` and `hmd` will find and run `hmd-create-binary-sensor` and pass it all the command line options.\n\n### `hmd create binary sensor`\n\nCreate/Update a binary sensor and set its state.\n\nUsage: `hmd create binary sensor --device-name mfsmaster --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --client-name inquisition --mqtt-server mqtt.unixorn.net --metric-name tamper --device-class motion --state off`\n\n### `hmd create device`\n\nCreate/Update a device and set the state of multiple metrics on it.\n\nUsage: `hmd create device --device-name coyote --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --mqtt-server mqtt.example.com --model \'Rocket Skates\' --manufacturer \'Acme Products\' --metric-data \'{"name":"Left Rocket Skate","value":93}\' --metric-data \'{"name":"Right Rocket Skate","value":155}\' --unique-id \'hmd-26536\'`\n',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
