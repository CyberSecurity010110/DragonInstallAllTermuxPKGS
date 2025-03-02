# DragonInstallAllTermuxPKGS
This is an updated yet simplified and better version of my previous attempt to create a  program to install as many packages as possible for testing without breaking the termux package system.

##Features

This version sticks to pure Bash, avoiding many issues entirely my previous script had.

Verbose Terminal Output:
Instead of progress bars, it now prints clear messages for each package attempt, success, or failure. You’ll now get to see exactly what’s happening in real-time

Robust Error Handling:
The || true construct ensures the script doesn’t exit on cleanup failures (e.g., if a package wasn’t partially installed or autoclean fails).
Redirects error output (2>/dev/null) to keep the terminal cleaner while still showing meaningful status updates.

Cleanup Logic:
If a package fails to install, it attempts to remove it (pkg remove) and clears the cache (pkg autoclean). This prevents broken packages from piling up and causing subsequent failures.

Accurate Counting:
Tracks installed_count and skipped_count explicitly, avoiding the off-by-one or misreported counts you noticed. It also calculates a success rate as a percentage.

No Wildcard Conflicts:
Unlike the original wildcard approach (pkg install *), which Termux doesn’t handle well, this iterates over the explicit package list from pkg list-all, ensuring every package is tried individually.


## Installation

 Clone the repository:

git clone https://github.com/CyberSecurity010110/DragonInstallAllTermuxPKGS

## Usage

Run the script:
./installaltermuxpkgs.sh



## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
