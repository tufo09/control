## Volume Control Script
This Python script provides command-line control over your system's volume. It uses the amixer command to interact with the system's sound settings.

### Functions
Here are the main functions in the script:

get_timestanp(): Returns the current timestamp as an integer.
get_volume_master(): Returns the current master volume level.
get_if_muted(): Checks if the master volume is muted. Returns True if muted, False otherwise.
data_exists(data_path): Checks if the data file exists. If not, it creates a new one with default values.
save_data(data): Saves the provided data into a JSON file.
load_data(data_path): Loads data from the JSON file.
cli_command(command): Executes a command in the terminal and returns its output.
notify(message, id, ttl): Sends a desktop notification with the provided message, id, and time-to-live (ttl).
main(data_path, name, standard_ttl, standard_ttl_s): The main function that parses command-line arguments and performs the appropriate action (raise, lower, mute).
### Usage
You can use this script from the command line as follows:

To raise the volume: python main.py raise [amount]
To lower the volume: python main.py lower [amount]
To mute/unmute the volume: python main.py mute
Replace [amount] with the desired volume change amount. You can use % Values or just normal numbers.

### Dependencies
This script requires Python 3 and the amixer command available on your system. It has been tested on Linux systems.

### Note
This script directly interacts with the system's sound settings. Please use it responsibly.