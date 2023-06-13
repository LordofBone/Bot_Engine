import io

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi 4' in m.read().lower():
                return "vcorevi"
            elif 'raspberry pi' in m.read().lower():
                return "vcoreiv"

    except FileNotFoundError:
        return "other"
