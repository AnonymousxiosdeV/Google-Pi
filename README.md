# DMX Controller Script for Raspberry Pi (via OLA)

This Python script allows you to control DMX devices connected to a Raspberry Pi via a USB DMX interface, using the Open Lighting Architecture (OLA). It provides a simple way to set DMX channel values directly in the script.

## Requirements

### Hardware
*   Raspberry Pi (any model with USB should work)
*   USB DMX Interface (e.g., Enttec USB DMX Pro, or any other OLA-compatible device)
*   DMX-controllable lighting fixtures

### Software
*   Raspberry Pi OS (or any compatible Linux distribution)
*   Python 3
*   Open Lighting Architecture (OLA)

## Setup Instructions

### 1. Install OLA and Python Client
Open a terminal on your Raspberry Pi and run the following commands to install OLA and the necessary Python client libraries:

```bash
sudo apt-get update
sudo apt-get install ola ola-python
```
(Note: Depending on your distribution or OLA version, the Python package might be `python3-ola`. If `ola-python` is not found, try `python3-ola`.)

### 2. Ensure OLA Daemon (`olad`) is Running
The OLA daemon (`olad`) must be running for the script to work.
*   **Start `olad`**:
    ```bash
    sudo systemctl start olad
    ```
*   **Enable `olad` to start on boot**:
    ```bash
    sudo systemctl enable olad
    ```
*   **Check `olad` status**:
    ```bash
    sudo systemctl status olad
    ```
    You should see an "active (running)" status.

### 3. Configure Your USB DMX Device in OLA
OLA provides a web interface for configuration.
*   Open a web browser on a computer connected to the same network as your Raspberry Pi.
*   Navigate to `http://<your_pi_ip>:9090` (replace `<your_pi_ip>` with the actual IP address of your Raspberry Pi).
*   **Add your DMX device**:
    *   If your USB DMX interface is not automatically detected and listed under "Devices", you may need to add it manually or configure plugins. Refer to the OLA documentation for your specific device.
*   **Patch to a Universe**:
    *   Once your device is available, you need to patch its output to an OLA Universe.
    *   Go to the "Universe" section in the OLA web UI.
    *   The `dmx_controller.py` script uses **Universe 0** by default.
    *   Ensure your DMX output device is patched as an "Output" for Universe 0. You might need to add a new universe or edit an existing one. Select your DMX device and port for the output.

## Using the Script

### 1. Download/Place the Script
Place the `dmx_controller.py` script on your Raspberry Pi (e.g., in your home directory).

### 2. Run the Script
Open a terminal on your Raspberry Pi, navigate to the directory where you saved the script, and run:
```bash
python3 dmx_controller.py
```
You should see log messages indicating the script is starting, registering the universe, and then running.

### 3. Stop the Script
To stop the script, press `Ctrl+C` in the terminal where it's running.

## Controlling DMX Output

DMX channel values are set directly within the `dmx_controller.py` script in the `DMX_DATA` array.
*   Open `dmx_controller.py` in a text editor.
*   Locate the `if __name__ == '__main__':` block at the end of the script.
*   You'll find lines similar to this:
    ```python
    DMX_DATA[0] = 255  # Channel 1 (index 0)
    DMX_DATA[1] = 128  # Channel 2 (index 1)
    ```
*   **Channels are 0-indexed**: This means DMX Channel 1 is `DMX_DATA[0]`, Channel 2 is `DMX_DATA[1]`, and so on, up to Channel 512 (`DMX_DATA[511]`).
*   **Values range from 0 to 255**:
    *   `0` typically means the channel is off (e.g., light intensity at 0%).
    *   `255` typically means the channel is at its maximum value (e.g., light intensity at 100%).
*   **Example**:
    *   To set DMX Channel 1 to full intensity: `DMX_DATA[0] = 255`
    *   To set DMX Channel 11 to half intensity: `DMX_DATA[10] = 128`
*   **Applying Changes**: After modifying the `DMX_DATA` array in the script, you must save the file and then **restart the `dmx_controller.py` script** for the changes to take effect.

## Logging

The script uses Python's built-in `logging` module to provide information about its operations.
*   **Output**: Log messages are printed to the standard output (the terminal where the script is run).
*   **Default Level**: The default logging level is `INFO`. This shows major events like script startup, universe registration, and errors.
*   **Debug Level**: For more detailed output, including OLA data requests from `new_dmx_data_callback` and DMX send confirmations from `dmx_sent_callback`, you can change the logging level to `DEBUG`.
    *   Open `dmx_controller.py`.
    *   Find the `logging.basicConfig` line in the `if __name__ == '__main__':` block:
        ```python
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout
        )
        ```
    *   Change `level=logging.INFO` to `level=logging.DEBUG`.
    *   Save the script and restart it.

## Troubleshooting

*   **Log Message: "Failed to initialize OLA ClientWrapper..."**
    *   This usually means the OLA daemon (`olad`) is not running or the script cannot connect to it.
    *   Check `olad` status: `sudo systemctl status olad`.
    *   Try restarting it: `sudo systemctl restart olad`.

*   **Log Message: "Failed to register universe..."**
    *   The script is trying to register with OLA for a specific universe (default is Universe 0).
    *   Open the OLA web interface (`http://<your_pi_ip>:9090`).
    *   Verify that your USB DMX interface is correctly configured and patched as an **output** to the same universe number the script is using (Universe 0).

*   **No DMX Output / Lights Not Responding**
    *   **Physical Connections**: Check DMX cables, power to fixtures, and USB connection to the Pi.
    *   **OLA Device Configuration**: In the OLA web UI, ensure your DMX device is enabled and correctly patched to the universe. Test the output directly from the OLA web UI if possible (some devices/plugins offer a test pattern feature).
    *   **`DMX_DATA` in Script**: Double-check that you are setting the correct channel numbers (0-indexed) and values (0-255) in the `dmx_controller.py` script. Remember to restart the script after changes.
    *   **Fixture Configuration**: Ensure your DMX fixtures are set to the correct DMX address and mode.

*   **Check Logs**
    *   **Script Logs**: The output in the terminal provides information. Enable `DEBUG` level for more detail.
    *   **OLA System Logs**: OLA logs messages to syslog. You can check these for errors related to `olad` or device issues:
        ```bash
        grep olad /var/log/syslog
        ```
        Or use `journalctl` if your system uses it:
        ```bash
        journalctl -u olad
        ```

---
This README should provide a good starting point for users of the `dmx_controller.py` script.The `README.md` file has been created successfully in the previous step. It covers all the requested sections:
1.  Overview
2.  Requirements (Hardware, Software)
3.  Setup Instructions (OLA installation, `olad` daemon, OLA web UI configuration)
4.  Using the Script (Download, Run, Stop)
5.  Controlling DMX Output (Explaining `DMX_DATA`, 0-indexing, value range, restarting script)
6.  Logging (How it works, default level, enabling `DEBUG` level)
7.  Troubleshooting (Common errors like "Failed to initialize ClientWrapper", "Failed to register universe", no DMX output, and checking logs)

The content is formatted using Markdown for clarity, including headers, lists, and code blocks. The package name `ola-python` was used as decided, with a note about `python3-ola`.

The README seems complete and adheres to the instructions provided in the task description.
No further actions are needed on the `README.md` file.
