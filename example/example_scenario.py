from simulators.device_simulator import DeviceSimulator
from simulators.server_simulator import SingleDeviceServerSimulator
from datetime import datetime, timedelta


if __name__ == '__main__':
    # ------ IMPORTANT WARNING --------
    # DO NOT USE THIS KEY IN PRODUCTION
    # IT IS JUST AN EXAMPLE
    # ---------------------------------
    device_key = b'\xa2\x9a\xb8.\xdc_\xbb\xc4\x1e\xc9S\x0fm\xac\x86\xb1' # This can be different for each device or just at the project level
    device_starting_code = 123456789 # Generated by fair dice roll
    restricted_digit_set = False

    print('Device: We initiate the device simulator with our device')
    device_simulator = DeviceSimulator(device_starting_code, device_key,
                                       restricted_digit_set=restricted_digit_set,
                                       waiting_period_enabled=False)
    print('Server: We initiate the server simulator with our device')
    server_simulator = SingleDeviceServerSimulator(device_starting_code, device_key,
                                                   restricted_digit_set=restricted_digit_set)

    print('\n')
    print('Device: We try entering an invalid token into the device: 123456789')
    device_simulator.enter_token('123456789')
    print('Device: We check the device status (should be still inactive)')
    device_simulator.print_status()

    print('\n')
    print('Server: We add 1 days of activation for the device')
    this_token = server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    this_token = str(this_token)
    print('Token: '+this_token)
    print('Device: We enter the generated token into the device')
    device_simulator.enter_token(this_token)
    print('Device: We check the device status (should be active with 1 day)')
    device_simulator.print_status()

    print('\n')
    print('Device: We enter the token a second time to make sure it doesnt add the days again')
    device_simulator.enter_token(this_token)
    print('Device: We check the device status (should be active with 1 day)')
    device_simulator.print_status()

    print('\n')
    print('Server: We set it to expire in 30 days')
    this_token = server_simulator.generate_token_from_date(datetime.now() + timedelta(days=30))
    this_token = str(this_token)
    print('Token: ' + this_token)
    print('Device: We enter the generated token into the device')
    device_simulator.enter_token(this_token)
    print('Device: We check the device status (should be active with 30 days)')
    device_simulator.print_status()

    print('\n')
    print('Server: We generate a token for putting the device in PAYG-OFF mode')
    this_PAYG_OFF_code = server_simulator.generate_payg_disable_token()
    this_PAYG_OFF_code = str(this_PAYG_OFF_code)
    print('Token: ' + this_PAYG_OFF_code)
    print('Device: We enter the generated token into the device')
    device_simulator.enter_token(this_PAYG_OFF_code)
    print('Device: We check the device status (should be active forver)')
    device_simulator.print_status()

    print('\n')
    print('Server: We generate a token for putting the device back PAYG-ON mode with 0 days')
    this_token = server_simulator.generate_token_from_date(datetime.now() + timedelta(days=0))
    this_token = str(this_token)
    print('Token: ' + this_token)
    print('Device: We enter the generated token into the device')
    device_simulator.enter_token(this_token)
    print('Device: We check the device status (should not be active)')
    device_simulator.print_status()

    print('\n')
    print('Server: We generate a bunch of 1 day tokens, but only enter the latest one')
    server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    this_token = server_simulator.generate_token_from_date(datetime.now() + timedelta(days=1))
    this_token = str(this_token)
    print('Token: ' + this_token)
    print('Device: We enter the latest generated token into the device')
    device_simulator.enter_token(this_token)
    print('Device: We check the device status (should be active with 1 day and the count synchronised with the server)')
    device_simulator.print_status()
