import hassapi as hass

MODULE = "reset_zha_sensor"
CLASS = "ResetZHASensor"

CONF_TIMEOUT = "timeout"
CONF_MOTION_SENSORS = "motion_sensors"

DEFAULT_TIMEOUT = 5

class ResetZHASensor(hass.Hass):
    """
    A class to interact with Aqara motion sensors, sets them to unoccupied after a specific timeout.
    """

    def initialize(self):
        """
        Initialize the ResetZHASensor app. Listens for state changes in the motion sensors.
        """
        self.motion_sensors = self.args.get(CONF_MOTION_SENSORS, [])
        self.timeout = self.args.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

        self.log(f"Initializing ResetZHASensor with sensors: {self.motion_sensors} and timeout: {self.timeout}", level="INFO")

        for sensor in self.motion_sensors:
            self.listen_state(self.motion_detected, sensor['entity_id'])

    def motion_detected(self, entity, attribute, old, new, kwargs):
        """
        Handles state change of motion sensor, sets state to "on" if new state is "on".
        Schedules to set state to "off" after a timeout.
        """
        if new == "on":
            self.log(f"Motion detected by {entity}. Scheduling reset.", level="INFO")
            self.run_in(self.reset_sensor_state, self.timeout, sensor=entity)

    def reset_sensor_state(self, kwargs):
        """
        Resets the state of the motion sensor in ZHA.
        """
        entity = kwargs.get("sensor")
        sensor = next((s for s in self.motion_sensors if s['entity_id'] == entity), None)
        if sensor is None:
            self.log(f"No sensor found for entity {entity}", level="ERROR")
            return

        self.log(f"Resetting sensor state for {sensor['ieee']}", level="INFO")
        self.call_service("zha/set_zigbee_cluster_attribute", ieee=sensor['ieee'], endpoint_id=1, cluster_id=1280, cluster_type="in", attribute=2, value=0)
