import os
import json
import time
import sys


data_path = 'data.json'
name = 'Volume Control'
standard_ttl = 2500
standard_ttl_s = standard_ttl / 1000

def get_timestanp():
    return int(round(time.time(), 0))

def get_volume_master():
    command = 'awk -F"[][]" \'/Left:/ { print $2 }\' <(amixer sget Master)'
    return os.popen(f'{command}').read().strip()

def get_if_muted():
    command = "amixer get Master | grep 'Left:' | awk -F'[][]' '{print $4}'"
    returnstate =  os.popen(command).read().strip()
    if returnstate == "off":
        return True
    else:
        return False

def data_exists(data_path):
    if not os.path.exists(data_path):
        data = {"message" : {"last_called" : get_timestanp(), "last_message_id" : 0, "volume" : get_volume_master()},
                "mute" : {"state" : get_if_muted()}}
        save_data(data)

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

def load_data(data_path):
    data_exists(data_path)
    with open(data_path, 'r') as file:
        return json.load(file)

def cli_command(command):
    return os.popen(f'{command}').read().strip()

def notify(message="No message provided.", id=0, ttl=standard_ttl):
    return_data = os.popen(f'notify-send -t {ttl} -r {id} -p "{name}" "{message}"').read().strip()
    print(return_data)
    return return_data

def main(data_path=data_path, name=name, standard_ttl=standard_ttl, standard_ttl_s=standard_ttl_s):
    args = sys.argv
    data = load_data(data_path)
    if len(args) == 1:
       notify("Error: No arguments provided. Please provide an argument.")
       return
    
    # check if the argument is valid
    if not (args[1] == "raise" or args[1] == "lower" or args[1] == "mute"):
        notify("Error: Invalid argument provided. Please provide a valid argument.")
        return
    
    # do if argument raise
    if args[1] == "raise":
        cli_command(f'amixer set Master {args[2]}+')

        if get_timestanp() - data['message']['last_called'] <= standard_ttl_s:
            return_data = notify(f'Volume raised from {data["message"]["volume"]} to {get_volume_master()}', data['message']['last_message_id'])
        else:
            return_data = notify(f'Volume raised from {data["message"]["volume"]} to {get_volume_master()}')
        # update the data
        data['message']['volume'] = get_volume_master()
        data['message']['last_message_id'] = return_data.strip() 
        data['message']['last_called'] = get_timestanp()
        save_data(data)

    # do if argument lower
    elif args[1] == "lower":
        cli_command(f'amixer set Master {args[2]}-')

        if get_timestanp() - data['message']['last_called'] <= standard_ttl_s:
            return_data = notify(f'Volume lowered from {data["message"]["volume"]} to {get_volume_master()}', data['message']['last_message_id'])
        else:
            return_data = notify(f'Volume lowered from {data["message"]["volume"]} to {get_volume_master()}')
        # update the data
        data['message']['volume'] = get_volume_master()
        data['message']['last_message_id'] = return_data.strip()
        data['message']['last_called'] = get_timestanp()
        save_data(data)

    # do if argument mute
    elif args[1] == "mute":
        if data['mute']['state']:
            cli_command('amixer set Master unmute')
            
            if (get_timestanp() - data['message']['last_called'] <= standard_ttl_s):
                return_data = notify('Unmuted', data['message']['last_message_id'])
            else:
                return_data = notify('Unmuted')

            # update the data
            data['message']['last_message_id'] = return_data.strip()
            data['mute']['state'] = False
            data['message']['last_called'] = get_timestanp()
            save_data(data)
        elif not data['mute']['state']:
            cli_command('amixer set Master mute')
            
            if (get_timestanp() - data['message']['last_called'] <= standard_ttl_s):
                return_data = notify('Muted', data['message']['last_message_id'])
            else:
                return_data = notify('Muted')

            # update the data
            data['message']['last_message_id'] = return_data.strip()
            data['mute']['state'] = True
            data['message']['last_called'] = get_timestanp()
            save_data(data)
        else:
            notify("Error: Something went wrong.")

main()