from dcim.models import Device

def get_device():
    devices = Device.objects.all()
    devices = devices.order_by('rack', '-position')
    return devices