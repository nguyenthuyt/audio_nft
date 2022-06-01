#pip install qrcode
#Documentation: https://pypi.org/project/qrcode/

import qrcode


img = qrcode.make((f"https://gateway.pinata.cloud/ipfs/123"))
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")