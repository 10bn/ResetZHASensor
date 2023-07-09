# ResetZHASensor

This project was heavly inspired by [WernerHP's Aqara Motion Sensors AppDaemon app](https://github.com/wernerhp/ha.appdaemon.aqara_motion_sensors). Many thanks to WernerHP for the original idea and implementation.

## Introduction

ResetZHASensor is an AppDaemon app for Home Assistant designed to manage Xiaomi Aqara motion sensors in a Zigbee Home Automation (ZHA) setup. It works in conjunction with a hardware modification that allows the sensors to detect motion every 5 seconds. The app resets the sensor states in ZHA after a specified timeout, enabling the sensors to toggle state every few seconds. This approach helps avoid 'ghost' motion events caused by state desynchronization between Home Assistant and ZHA, ensuring accurate motion detection. 

Please note that a hardware modification to the Xiaomi Aqara motion sensors is necessary for this app to function as intended. The hardware modification allows the sensors to detect motion more frequently than they do by default. Without this modification, the sensors would only be able to detect motion every 120 seconds.

## HACS Installation

1. Make sure you have the option "Enable AppDaemon apps discovery & tracking". This is located in: Configuration -> Integrations -> HACS (options).
2. Restart Home Assistant.
3. Go to HACS -> Automation -> search for "ResetZHASensor" and install it.
4. Follow the app configuration section below.

## Manual Installation

Download the `reset_zha_sensor` directory from inside the `apps` directory to your local `apps` directory, then configure the `reset_zha_sensor` module in `apps.yaml`.

## App Configuration

```yaml
reset_zha_sensor:
  module: reset_zha_sensor
  class: ResetZHASensor
  timeout: 5
  motion_sensors:
    - entity_id: binary_sensor.kitchen_motion_sensor_motion
      ieee: '00:15:8d:00:04:05:85:98'
    - entity_id: binary_sensor.bathroom_motion_sensor_motion
      ieee: '00:15:8d:00:04:05:85:98'
    - entity_id: binary_sensor.bathroom_motion_sensor_2_motion
      ieee: '00:15:8d:00:05:81:2c:ac'
```

| key | optional | type | default | description |
| --- | --- | --- | --- | --- |
| `module` | False | string | | The module name of the app. |
| `class` | False | string | | The name of the Class. |
| `timeout` | True | int | 5 | Timeout after which motion sensor state is set to off. |
| `motion_sensors` | False | list | | A list of motion sensor entity_ids and their corresponding ieee addresses. |
