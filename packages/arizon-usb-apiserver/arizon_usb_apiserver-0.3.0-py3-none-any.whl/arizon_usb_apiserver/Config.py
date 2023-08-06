import yaml
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    path: str = './arizon_config.yaml'
    serial_port: str = None
    serial_baudrate: int = 115200
    api_port: str = 8080
    api_interface: str = '0.0.0.0'
    debug: bool = False
    valid: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        err = self.load()
        if err is None:
            self.valid = True
        else:
            self.valid = False

    def load(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                cfg_dict = yaml.load(open(self.path, "r"),
                                     Loader=yaml.SafeLoader)
            except Exception as e:
                return e

            try:
                cfg = cfg_dict['arizon_usb_apiserver']
                self.serial_port = cfg['serial']['port']
                self.serial_baudrate = cfg['serial']['baudrate'] if 'baudrate' in cfg['serial'] else 115200
                self.api_port = cfg['api']['port']
                self.api_interface = cfg['api']['interface'] if 'interface' in cfg['api'] else '0.0.0.0'
                self.debug = cfg['debug']
                return None

            except Exception as e:
                return e

        else:
            return Exception("Config path is not set")

    def dump(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                with open(self.path, 'w') as f:
                    yaml.dump({
                        "serial": {
                            "port": self.serial_port,
                            "baudrate": self.serial_baudrate
                        },
                        "api": {
                            "port": self.api_port,
                            "interface": self.api_interface
                        }
                    }, f)
                    return None
            except:
                return Exception("Failed to dump config")
        else:
            return Exception("Config path is not set")
