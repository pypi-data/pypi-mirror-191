import logging

from pymavlink.mavutil import mavlink, mavlink_connection

logging.basicConfig(level=logging.INFO)

DEFAULT_DEVICE = "/dev/ttyUSB0"
# DEFAULT_DEVICE = "udpin:127.0.0.1:14551"
DEFAULT_BAUD = 112500
DEFAULT_SYSTEM_ID = 21
DEFAULT_COMPONENT_ID = 37


def log_mavlink_messages():
    connection = mavlink_connection(
        DEFAULT_DEVICE,
        baud=DEFAULT_BAUD,
        source_system=DEFAULT_SYSTEM_ID,
        source_component=DEFAULT_COMPONENT_ID,
    )
    connection.mav.request_data_stream_send(
        connection.target_system,
        connection.target_component,
        mavlink.MAV_DATA_STREAM_ALL,
        10,
        1,
    )

    logging.info("Awaiting heartbeat")

    connection.wait_heartbeat()

    logging.info("Heartbeat received")

    while True:
        msg = connection.recv_match(blocking=True)
        msg_type: str = msg.get_type()
        # logging.info(msg_type)
        # logging.info(msg)

        if msg_type == "GLOBAL_POSITION_INT":
            lat = msg.lat
            lon = msg.lon
            alt = msg.alt

            logging.info("Lat: %s lon: %s alt: %s", lat, lon, alt)

        if msg_type == "ATTITUDE":
            roll = msg.roll
            pitch = msg.pitch
            yaw = msg.yaw

            logging.info("Roll: %s pitch: %s yaw: %s", roll, pitch, yaw)


if __name__ == "__main__":
    log_mavlink_messages()
