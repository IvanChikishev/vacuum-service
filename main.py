from miio import DreameVacuumMiot, Gateway
from flask import Flask, Response
from string import Template

app = Flask('Dreame Miot Helper')

device = DreameVacuumMiot('192.168.31.67', '4441576e5431773843725262495a4570')

DEVICE_STATUS_MESSAGE = Template('{'
                                 '"success": $success, '
                                 '"clean_mode": $clean_mode, '
                                 '"battery_level": $battery_level, '
                                 '"volume": $volume, '
                                 '"charging_state": $charging_state, '
                                 '"operating_mode": $operating_mode'
                                 '}')

ACTION_STATE_MESSAGE = Template('{"success": $success}')


@app.route('/sensor/temperature')
def get_sensor_stata():
    try:
        service = Gateway("192.168.31.12", "7775744e5936547241637a4459594858")
        service.discover_devices()

        sensor_device = service.devices['lumi.158d00073a84b7']

        template = Template('{"temperature": $temperature, "humidity": $humidity, "success": true}')

        message = template.substitute(
            temperature=sensor_device.get_property('temperature')[0] / 100,
            humidity=sensor_device.get_property('humidity')[0] / 100
        )

    except Exception:
        message = '{"success": false}'
    finally:
        return Response(message, mimetype="application/json")



@app.route('/status')
def get_status():
    response = DEVICE_STATUS_MESSAGE.safe_substitute(
        clean_mode=-1,
        battery_level=-1,
        volume=-1,
        charging_state=-1,
        operating_mode=-1,
        success=0)
    try:
        device_status = device.status()

        response = DEVICE_STATUS_MESSAGE.safe_substitute(
            clean_mode=device_status.cleaning_mode.value,
            battery_level=device_status.battery_level,
            volume=device_status.volume,
            charging_state=device_status.charging_state.value,
            operating_mode=device_status.operating_mode.value,
            success=1
        )
    finally:
        return Response(response, mimetype="application/json")


@app.route('/action/home')
def charge():
    response = ACTION_STATE_MESSAGE.safe_substitute(success=0)
    try:
        device.home()
        response = ACTION_STATE_MESSAGE.safe_substitute(success=1)
    finally:
        return Response(response, mimetype="application/json")


@app.route('/action/clean/stop')
def clean_stop():
    response = ACTION_STATE_MESSAGE.safe_substitute(success=0)
    try:
        device.stop()
        response = ACTION_STATE_MESSAGE.safe_substitute(success=1)
    finally:
        return Response(response, mimetype="application/json")


@app.route('/action/clean/start')
def clean_start():
    response = ACTION_STATE_MESSAGE.safe_substitute(success=0)
    try:
        device.start()
        response = ACTION_STATE_MESSAGE.safe_substitute(success=1)
    finally:
        return Response(response, mimetype="application/json")


@app.route('/properties/clean_mode/<string:mode>')
def clean_mode(mode):
    response = ACTION_STATE_MESSAGE.safe_substitute(success=0)
    # try:
    device.set_property('clean_mode', int(mode))
    response = ACTION_STATE_MESSAGE.safe_substitute(success=1)
    # finally:
    return Response(response, mimetype="application/json")


if __name__ == '__main__':
    app.run('0.0.0.0', 8077)
