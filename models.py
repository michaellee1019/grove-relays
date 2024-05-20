import viam_wrap
from viam.components.generic import Generic
from viam.proto.app.robot import ComponentConfig
from typing import Mapping, Self
from viam.utils import ValueTypes
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
import time
import sys
import smbus2

CMD_CHANNEL_CTRL=0x10
CMD_SAVE_I2C_ADDR=0x11
CMD_READ_I2C_ADDR=0x12
CMD_READ_FIRMWARE_VER=0x13

class Grove4ChannelSPDTRelay(Generic):
    MODEL = "michaellee1019:grove:4_channel_spdt_relay"
    bus = None

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'pulse_one':
                if all(arg in args for arg in ("address","bit","pulse_seconds")):
                    results = await self.pulse_one(args['address'], args['bit'], args['pulse_seconds'])
                    result[name] = 'pulsed: ' + results
                else:
                    result[name] = 'missing address, bit, or pulse_seconds parameters'
        return result

    async def pulse_one(self, address: str, bit: str, pulse_seconds: str) -> str:
        hex_address = int(address, 16)
        hex_bit = int(bit, 16)
        self.bus.write_byte_data(hex_address,CMD_CHANNEL_CTRL,hex_bit)
        time.sleep(float(pulse_seconds))
        self.bus.write_byte_data(hex_address,CMD_CHANNEL_CTRL,0x00)
        return "{0} {1}".format(hex(hex_address), hex(hex_bit))

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        self.bus = smbus2.SMBus(1)
        output = self(config.name)
        return output

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        return None

if __name__ == '__main__':
    # necessary for pyinstaller to see it
    # build this with: 
    # pyinstaller --onefile --hidden-import viam-wrap --paths $VIRTUAL_ENV/lib/python3.10/site-packages installable.py 
    # `--paths` arg may no longer be necessary once viam-wrap is published somewhere
    # todo: utility to append this stanza automatically at build time
    viam_wrap.main(sys.modules.get(__name__))