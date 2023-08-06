import os
import g4s
from g4s.utils.enums import DeviceType
import logging

LOGGER = logging.getLogger(__name__)
USERNAME: str = os.environ["g4s_username"]
PASSWORD: str = os.environ["g4s_password"]


def test_creation():
    alarm = g4s.Alarm(USERNAME, PASSWORD)
    assert alarm is not None


def test_access_code_on_chip():
    alarm = g4s.Alarm(USERNAME, PASSWORD)
    assert alarm is not None
    chips = [
        device for device in alarm.sensors if device.type == DeviceType.ACCESSCHIP and device.access_code is not None
    ]
    LOGGER.info(len(chips))
    assert len(chips) > 0
