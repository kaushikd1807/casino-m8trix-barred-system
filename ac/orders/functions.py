from io import BytesIO
from base64 import b64encode
from urllib.parse import quote
from datauri import DataURI
import shortuuid
import qrcode
import qrcode.image.svg

def generate_magic_url_seed():
    return shortuuid.ShortUUID().random(length=8)

def generate_qr_code(url):
    factory = qrcode.image.svg.SvgFillImage
    img = qrcode.make(url, image_factory=factory)
    svg_out = BytesIO()
    img.save(svg_out)
    data = b64encode(svg_out.getvalue()).decode('ascii')
    data_url = 'data:image/svg+xml;base64,{}'.format(quote(data))
    return data_url
