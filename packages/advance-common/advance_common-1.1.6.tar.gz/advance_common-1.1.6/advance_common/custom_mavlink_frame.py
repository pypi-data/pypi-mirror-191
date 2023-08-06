from typing import Any

from google.protobuf.json_format import MessageToDict
from pymavlink.dialects.v20.ardupilotmega import (
    MAVLink_command_long_message,
    MAVLink_encapsulated_data_message,
    MAVLink_mission_clear_all_message,
    MAVLink_mission_count_message,
    MAVLink_mission_item_int_message,
    MAVLink_param_set_message,
    MAVLink_statustext_message,
)

from .messages_pb2 import SaeTelemetry


class CustomMavlinkFrame:
    MAX_MESSAGE_LENGTH = 252

    @classmethod
    def from_mavlink_message(
        cls, mavlink_message: MAVLink_encapsulated_data_message
    ) -> SaeTelemetry:
        protobuf_payload_length = int(mavlink_message.data[0])

        if protobuf_payload_length > cls.MAX_MESSAGE_LENGTH:
            raise ValueError("Too large message length")

        protobuf_payload = bytes(mavlink_message.data[1 : protobuf_payload_length + 1])

        result_message = SaeTelemetry()
        result_message.ParseFromString(protobuf_payload)
        return result_message

    @classmethod
    def to_dict(cls, message: SaeTelemetry):
        return MessageToDict(
            message,
            including_default_value_fields=True,
            preserving_proto_field_name=True,
        )

    @classmethod
    def to_mavlink_message(
        cls, message_to_send: SaeTelemetry, target_system: int, target_component: int
    ) -> MAVLink_encapsulated_data_message:
        protobuf_payload: bytes = message_to_send.SerializeToString()
        payload_size_bytes = len(protobuf_payload)

        bytes_to_send = bytes(
            [payload_size_bytes]
        )  # First byte - protobuf payload length
        bytes_to_send += protobuf_payload  # Protobuf payload
        bytes_to_send += bytes([0x42]) * (
            cls.MAX_MESSAGE_LENGTH - payload_size_bytes
        )  # Padding bytes
        msg = MAVLink_encapsulated_data_message(0, bytes_to_send)
        msg._header.srcSystem = target_system
        msg._header.srcComponent = target_component

        return msg

    @classmethod
    def to_mavlink_command_long_message(
        cls,
        target_system: int,
        target_component: int,
        command: Any,
        confirmation: Any,
        param1: Any = 0,
        param2: Any = 0,
        param3: Any = 0,
        param4: Any = 0,
        param5: Any = 0,
        param6: Any = 0,
        param7: Any = 0,
    ) -> MAVLink_command_long_message:
        msg = MAVLink_command_long_message(
            target_system=target_system,
            target_component=target_component,
            command=command,
            confirmation=confirmation,
            param1=param1,
            param2=param2,
            param3=param3,
            param4=param4,
            param5=param5,
            param6=param6,
            param7=param7,
        )

        return msg

    @classmethod
    def to_mavlink_param_set_message(
        cls,
        target_system: int,
        target_component: int,
        param_id: Any,
        param_value: Any,
        param_type: Any,
    ) -> MAVLink_param_set_message:
        msg = MAVLink_param_set_message(
            target_system=target_system,
            target_component=target_component,
            param_id=param_id,
            param_value=param_value,
            param_type=param_type,
        )

        return msg

    @classmethod
    def to_mavlink_mission_count_message(
        cls,
        target_system: int,
        target_component: int,
        count: Any,
    ) -> MAVLink_mission_count_message:
        msg = MAVLink_mission_count_message(
            target_system=target_system, target_component=target_component, count=count
        )

        return msg

    @classmethod
    def to_mavlink_mission_clear_message(
        cls,
        target_system: int,
        target_component: int,
    ) -> MAVLink_mission_clear_all_message:
        msg = MAVLink_mission_clear_all_message(
            target_system=target_system, target_component=target_component
        )

        return msg

    @classmethod
    def to_mavlink_mission_item_int_message(
        cls,
        target_system: int,
        target_component: int,
        seq: int,
        frame: Any,
        command: Any,
        current: Any,
        autocontinue: Any,
        param1: Any = 0,
        param2: Any = 0,
        param3: Any = 0,
        param4: Any = 0,
        x: int = 0,
        y: int = 0,
        z: int = 0,
    ) -> MAVLink_mission_item_int_message:
        msg = MAVLink_mission_item_int_message(
            target_system=target_system,
            target_component=target_component,
            seq=seq,
            frame=frame,
            command=command,
            current=current,
            autocontinue=autocontinue,
            param1=param1,
            param2=param2,
            param3=param3,
            param4=param4,
            x=x,
            y=y,
            z=z,
        )

        return msg

    @classmethod
    def to_mavlink_statustext_message(
        cls, severity: Any, text: Any
    ) -> MAVLink_statustext_message:
        msg = MAVLink_statustext_message(severity=severity, text=text)

        return msg
