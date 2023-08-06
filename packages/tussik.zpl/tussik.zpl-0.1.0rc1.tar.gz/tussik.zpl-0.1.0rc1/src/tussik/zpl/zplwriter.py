import io
import json
import logging
import math
import socket
from typing import List, Optional, Union

import requests

try:
    from PIL import ImageOps, Image
except:
    Image = None
    ImageOps = None
from .zplconfig import ZplConfig

logger = logging.getLogger()


class ZplWriter:
    __slots__ = ['_stream', '_attrib', '_config', '_font', '_reverse']

    def __init__(self, config: Optional[ZplConfig] = None):
        self._attrib: List[str] = []
        self._stream: List[str] = []
        self._font: str = ''
        self._reverse: str = ''
        self._config: ZplConfig = config.copy() if isinstance(config, ZplConfig) else ZplConfig()

    def export(self) -> str:
        config = "".join(self._attrib)
        stream = "".join(self._stream)
        return f"^XA^MT{config}{stream}^XZ"

    def clear(self):
        self._stream: List[str] = []

    def add(self, command: str):
        self._stream.append(command)

    def coordinates(self, left: int, top: int) -> (int, int):
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        return left, top

    def to_reverse(self):
        self._reverse = "^FR"

    def to_normal(self):
        self._reverse = ""

    def print(self, ipaddress: str, port: int = 9100) -> bool:
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            mysocket.settimeout(self._config.timeout)
            mysocket.connect((ipaddress, port))  # connecting to host
            content = self.export()
            payload = bytes(content, "utf8")
            mysocket.send(payload)
            mysocket.close()
        except OSError as e:
            logger.exception(f"Unable to connect to {ipaddress}:{port}")
            return False
        except Exception as e:
            logger.exception("Error with the connection")
            return False
        return True

    def saveas(self, destination: Union[str, io.BytesIO]) -> bool:
        #
        # uses a 3rd party service not affiliated with this library in any way
        #
        url = f"http://api.labelary.com/v1/printers/{int(self._config.dpmm)}dpmm/labels" \
              f"/{int(self._config.width)}x{int(self._config.height)}/0/"
        headers = {'Accept': 'application/pdf'}
        response = requests.post(url, self.export(), headers=headers)
        if response.status_code == 200:
            if isinstance(destination, str):
                with open(destination, 'wb') as f:
                    f.write(response.content)
            else:
                destination.write(response.content)
            return True
        logging.error(response.content)
        return False

    def textblock(self, left: int = 0, top: int = 0, data: str = "",
                  width: int = 0, justify: str = "J", maxlines: int = 1) -> bool:
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        justify = justify.upper()
        if justify not in ['L', 'C', 'R', 'J']:
            return False
        width = max(0, int(width * self._config.dpmm))
        self.add(f"^FO{left},{top}{self._font}{self._reverse}"
                 f"^FB{width},{maxlines},0,{justify},0^FD{data}^FS")
        return True

    def font(self, height: int = 10, width: Optional[int] = None, flip: int = 0,
             fontcode: str = "0", isdefault: bool = False):
        height = int(min(max(height * self._config.dpmm, 0), 32000))
        if isinstance(width, int):
            width = int(min(max(width * self._config.dpmm, 0), 32000))
        if flip >= 270:
            orient = "B"
        elif flip >= 180:
            orient = "I"
        elif flip >= 90:
            orient = "R"
        else:
            orient = "N"
        if width is None:
            self._font = f"^A{fontcode}{orient},{height}"
            if isdefault:
                self.add(f'^CF{fontcode},{height}')
        else:
            self._font = f"^A{fontcode}{orient},{height},{width}"
            if isdefault:
                self.add(f'^CF{fontcode},{height},{width}')

    def text(self, data: str, left: int = 0, top: int = 0):
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._font}{self._reverse}^FD{data}^FS")

    def ellipse(self, left: int = 0, top: int = 0, width: int = 100, height: int = 100, thick: int = 2):
        width = int(min(max(width * self._config.dpmm, 3), 4095))
        height = int(min(max(height * self._config.dpmm, 3), 4095))
        thick = int(min(max(thick, 2), 4095))
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._reverse}^GE{width},{height},{thick},B^FS")

    def circle(self, left: int = 0, top: int = 0, diameter: int = 100, thick: int = 2):
        diameter = int(min(max(diameter * self._config.dpmm, 3), 4095))
        thick = int(min(max(thick, 2), 4095))
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._reverse}^GC{diameter},{thick},B^FS")

    def box(self, left: int = 0, top: int = 0, width: int = 100, height: int = 100, thick: float = 2, round: int = 0):
        thick = int(min(max(1, int(thick * self._config.dpmm)), 32000))
        width = int(min(max(thick, int(width * self._config.dpmm)), 32000))
        height = int(min(max(thick, int(height * self._config.dpmm)), 32000))
        round = int(min(max(0, round), 8))
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._reverse}^GB{width},{height},{thick},B,{round}^FS")

    def hline(self, left: int = 0, top: int = 0, width: int = 100, thick: int = 2):
        thick = int(min(max(1, int(thick * self._config.dpmm)), 32000))
        width = int(min(max(thick, int(width * self._config.dpmm)), 32000))
        height = max(thick, 0)
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._reverse}^GB{width},{height},{thick},B,0^FS")

    def vline(self, left: int = 0, top: int = 0, height: int = 100, thick: int = 2):
        thick = int(min(max(1, int(thick * self._config.dpmm)), 32000))
        width = max(thick, 0)
        height = int(min(max(thick, int(height * self._config.dpmm)), 32000))
        left = min(max(int(left * self._config.dpmm), 0), 32000)
        top = min(max(int(top * self._config.dpmm), 0), 32000)
        self.add(f"^FO{left},{top}{self._reverse}^GB{width},{height},{thick},B,0^FS")

    def image(self, image: Union[str, Image], left: int = 0, top: int = 0,
              width: Optional[int] = None, height: Optional[int] = None) -> bool:

        if Image is None:
            raise Exception("Developer! pillow library is required for ZplWriter.image")

        try:
            left = min(max(int(left * self._config.dpmm), 0), 32000)
            top = min(max(int(top * self._config.dpmm), 0), 32000)

            if isinstance(image, str):
                rc = requests.get(image, stream=True)
                if not rc.ok:
                    return False
                image = Image.open(rc.raw)

            if width is None:
                width = int(image.size[0])
            if height is None:
                # maintain aspect ratio
                height = int(float(image.size[1]) / image.size[0] * width)
            width = width * self._config.dpmm
            height = height * self._config.dpmm

            totalbytes = math.ceil(width / 8.0) * height
            bytesperrow = math.ceil(width / 8.0)
            image = image.resize((int(width), int(height)))
            image = ImageOps.invert(image.convert('L')).convert('1')
            data = image.tobytes().hex().upper()
            self.add(f"^FO{left},{top}^GFA,{len(data)},{totalbytes},{bytesperrow},{data}")
            return True
        except Exception as e:
            logger.exception("failed to load image")
            return False

    def qrcode(self, left: int = 0, top: int = 0, data: Union[str, dict, list, int, float, None] = None,
               magnify: Optional[int] = None) -> None:
        if data is None:
            return
        elif isinstance(data, str):
            content = data
        elif isinstance(data, (int, float)):
            content = str(data)
        else:
            content = json.dumps(data)
        if magnify is None:
            magnify = ''
        left, top = self.coordinates(left, top)
        self.add(f"^FO{left},{top}^BQ,2,{magnify},H^FDQA,{content}^FS")

    def orientation(self, rotate: int = 0, justify: int = 2) -> None:
        if rotate < 90:
            rotate = 0
        elif rotate < 180:
            rotate = 90
        elif rotate < 270:
            rotate = 180
        else:
            rotate = 270
        justify = min(2, max(0, justify))
        self.add(f"^FW{rotate},{justify}")

    def label_reverse(self, reverse: bool = False):
        a = "Y" if reverse else "N"
        self.add(f"^LR{a}")

    def label_length(self, length: int):
        len = int(min(32000, max(1, length)) * self._config.dpmm)
        self.add(f"^LL{len}")

    def cut(self, kiosk_cut_amount: bool = True):
        a = "0" if kiosk_cut_amount else "1"
        self.add(f"^CN{a}")
