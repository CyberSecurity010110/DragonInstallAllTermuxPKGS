# DragonInstallAllTermuxPKGS

DragonInstallAllTermuxPKGS is a Python script designed to automate the installation of all available Termux packages. It includes robust error handling, a blacklist of packages to ignore, and the ability to fix broken packages during the installation process.

## Features

- Fetches and installs all available Termux packages.
- Skips packages listed in a configurable blacklist.
- Handles installation errors and retries failed installations.
- Fixes broken packages automatically.
- Prompts the user to add packages to the blacklist at startup.

## Requirements

- Termux
- Python 3
- Rich library for enhanced console output

## Installation

1. Clone the repository:
    git clone https://github.com/CyberSecurity010110/DragonInstallAllTermuxPKGS.git
    cd DragonInstallAllTermuxPKGS

2. Install the required Python library:
    pip install rich

## Usage

1. Run the script:
    python3 installaltermuxpkgs.py

2. At startup, you will be prompted to add any packages to the blacklist. Enter the package names separated by commas.

3. The script will fetch all available Termux packages and begin the installation process, skipping any packages in the blacklist.

## Configuration

- **Blacklist**: The blacklist is stored in a file named `blacklist.txt`. You can manually edit this file to add or remove packages from the blacklist.

## Script Details

### Functions

- **get_all_packages**: Retrieves the list of all available Termux packages.
- **is_package_installed**: Checks if a package is already installed.
- **install_package**: Attempts to install a package and handles errors.
- **fix_broken_packages**: Attempts to fix broken packages.
- **prompt_for_blacklist**: Prompts the user to add packages to the blacklist.
- **load_blacklist**: Loads the blacklist from a file.
- **save_blacklist**: Saves the blacklist to a file.

### Main Process

1. Loads the existing blacklist from `blacklist.txt`.
2. Prompts the user to add additional packages to the blacklist.
3. Fetches all available Termux packages.
4. Iterates through the package list, installing each package unless it is in the blacklist.
5. Logs the results of the installation process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

