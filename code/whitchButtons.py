from evdev import InputDevice, list_devices, categorize, ecodes

devices = [InputDevice(path) for path in list_devices()]
device = None

for dev in devices:
    if dev.name == "Xbox Wireless Controller":
        device = dev
        break

if device is None:
    print("Xbox Wireless Controller not found.")
    exit()

# Main loop
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print('key event at {}, {} ({}), {}'.format(
            event.timestamp(), event.code, keyevent.keycode, 'down' if event.value else 'up'))
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print('ABS event at {}, code {}, value {}'.format(event.timestamp(), event.code, absevent.event.value))