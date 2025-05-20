#!/usr/bin/env python

import array
import sys
import logging # Added logging
from ola.ClientWrapper import ClientWrapper

# Global variables
UNIVERSE = 0  # OLA Universe (0-indexed)
DMX_DATA = array.array('B', [0] * 512)  # Array to hold DMX channel values (512 channels)
wrapper = None  # OLA ClientWrapper global instance

# Get a logger instance
logger = logging.getLogger(__name__)

def dmx_sent_callback(state):
    """
    Callback function that is called after a DMX frame has been sent.
    Args:
        state: ola.OlaClient.DmxSentState indicating success or failure.
    """
    if not state.Succeeded():
        logger.error("Error sending DMX data: %s", state.message)
    else:
        logger.debug("DMX data sent successfully for universe %s", UNIVERSE)
    # No explicit flush needed, logging handler does it.

def new_dmx_data_callback(universe):
    """
    Callback function that OLA calls when it needs new DMX data for the specified universe.
    This function will then send the current DMX_DATA.
    Args:
        universe: The DMX universe number for which data is requested.
    """
    logger.debug("OLA requesting data for universe %s", universe)
    # Send the current DMX data
    try:
        if wrapper:
            wrapper.Client().SendDmx(universe, DMX_DATA, dmx_sent_callback)
        else:
            logger.error("Error: OLA wrapper not initialized in new_dmx_data_callback.")
    except Exception: # Changed to logger.exception
        logger.exception("Error in new_dmx_data_callback")

def main():
    """
    Main function to initialize OLA client, register universe, and run the client.
    """
    global wrapper
    logger.info("Starting DMX controller...")

    # Initialize the OLA ClientWrapper
    try:
        wrapper = ClientWrapper()
    except Exception as e: # Changed to logger.exception for socket.error or other init errors
        logger.exception("Failed to initialize OLA ClientWrapper. Ensure the OLA daemon (olad) is running.")
        return

    client = wrapper.Client()

    # Register the universe with OLA, specifying the callback for data requests
    try:
        logger.info("Registering universe %s with OLA...", UNIVERSE)
        client.RegisterUniverse(UNIVERSE, client.REGISTER, new_dmx_data_callback)
        logger.info("Universe %s registered.", UNIVERSE)
    except Exception as e: # Changed to logger.exception
        logger.exception("Failed to register universe %s", UNIVERSE)
        # Clean up wrapper if registration fails
        if wrapper:
            wrapper.Stop()
        return

    # Run the OLA client event loop
    logger.info("OLA client running. Press Ctrl+C to exit.")
    try:
        wrapper.Run()  # This will block until wrapper.Stop() is called or an error occurs
    except KeyboardInterrupt:
        logger.info("\nKeyboardInterrupt received. Shutting down...")
    except Exception as e: # Changed to logger.exception
        logger.exception("An error occurred while running the OLA client")
    finally:
        if wrapper:
            logger.info("Stopping OLA client...")
            wrapper.Stop()
            logger.info("OLA client stopped.")

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO, # Default level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Example: Set logging level for this script's logger specifically if needed
    # logging.getLogger(__name__).setLevel(logging.DEBUG) # To see DEBUG messages

    logger.info("Setting initial DMX values: Channel 1 to 255, Channel 2 to 128.")
    DMX_DATA[0] = 255  # Channel 1
    DMX_DATA[1] = 128  # Channel 2
    # DMX_DATA[2] = 50   # Channel 3
    # ... and so on for other channels

    main()
