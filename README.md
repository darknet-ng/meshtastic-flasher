# Meshtastic Flasher for DEF CON 33

A Python GUI application designed to flash Meshtastic firmware onto LoRa devices at DEF CON 33. This tool provides an easy-to-use interface for attendees to update their devices and join the DEF CON Meshtastic mesh network.

## Features

- **Visual Device Selection** - Grid layout with device images for currently supported devices
- **Guided Flashing Process** - Step-by-step instructions including device-specific boot sequences
- **Device Support** - Currently supports 4 devices: Heltec v3, LilyGo T-Beam, T-Deck, and T-Lora v2
- **Firmware Management** - Pre-packaged Meshtastic v2.7.3 firmware included
- **Cross-Platform** - Built with PyQt6 for cross-platform compatibility

## Quick Start

### Requirements

- Python 3.8 or higher
- PyQt6 and pyserial packages
- USB cable for your Meshtastic device

### Installation

```bash
# Clone the repository
git clone https://github.com/darknet-ng/meshtastic-flasher.git
cd meshtastic-flasher

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

## Application Flow

1. **Device Selection** - Choose your device model from the visual grid
2. **Connection Instructions** - Follow device-specific instructions for entering boot mode
3. **Flash Options** - Choose whether to erase device before flashing
4. **Flashing** - Watch progress as firmware is written to device

## Supported Devices

Currently supported in the UI:
- Heltec v3
- LilyGo T-Beam v1.1
- LilyGo T-Deck
- LilyGo T-Lora v2.1.6

Note: While firmware files for many more devices are included in the firmware/ directory, the UI currently only supports the 4 devices listed above.

## DEF CON 33 Channels

The default Meshtastic firmware includes these channels:
- #1 DEFCONnet - Main conference channel
- #2 HackerComms - General hacker chat
- #3 NodeChat - Node-specific discussions

Additional channels can be added via QR code at the conference.

## Troubleshooting

### Common Issues

**Device not detected:**
- Ensure device is in bootloader mode (follow on-screen instructions)
- Try different USB cable or port
- Check device drivers are installed

**Flashing fails:**
- Some devices require holding BOOT button during power-on
- Verify correct device model selected
- Try "Install" option instead of "Update"

**Permission errors (Linux):**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Logout and login for changes to take effect
```

## Future Enhancements

Planned features for future versions:
- Post-flash configuration (channels, pairing codes)
- GPS privacy settings
- Custom firmware support
- Batch flashing capabilities
- QR code generation for channel sharing
