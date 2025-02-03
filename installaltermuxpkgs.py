#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
from rich.console import Console
from rich.progress import Progress

console = Console()

# Path to the blacklist file
BLACKLIST_FILE = "blacklist.txt"

# Hardcoded blacklist of packages to ignore
BLACKLISTED_PACKAGES = [
    "frida-python", "zeronet", "bat", "make-guile", "libblosc", "libjpeg-turbo-static",
    "libminizip-ng", "libspnav", "openvdb", "ptex", "ptex-static", "libyaml-cpp",
    "opencolorio", "opencv", "openimageio", "openjpeg-tools", "pybind11",
    "pystring", "pyunbound", "sse2neon", "bison-static", "pysha3", "dropbear",
    "brotli-static", "assimp-glibc-static", "assimp-static", "binutils-gold",
    "clang-16", "cryptsetup-static", "exiv2-static", "emacs", "gap-static",
    "gcc10", "gcc9", "gcc-default-9", "gcc-default-10", "gcc-default-11",
    "gcc-default-12", "gcc-default-13", "gcc-default-14", "gdal-static",
    "ghc-libs-static", "global-static", "gspell-static",
    "gst-plugins-gl-headers", "guile-static", "guile18", "hash-slinger",
    "kakoune-lsp", "python-pyarrow", "lite-xl-static", "lighttpd-static",
    "libzthread-static", "libxxf86vm-static", "libxv-static", "libxslt-static",
    "libxshmfence-static", "libxrender-static", "libxau-static",
    "libwebrtc-audio-processing-static", "libvips-static", "libpixman-static",
    "libsm-static", "libusbredir-static", "libsixel-static", "libopus-glibc-static",
    "libobjc2", "libnfs-static", "libmad-static", "libmaa-static",
    "libllvm-classic-flang", "binutils-is-llvm", "libllvm-16-static",
    "libheif-static", "libfm", "libhiredis-static", "libice-static",
    "libflann-static", "libexecinfo-static", "lfortran-llvm",
    "mpv-x", "mpd-static", "mp3cat-go", "mp3cat",
    "mesa-zink-dev", "mesa-zink", "mesa-vulkan-icd-freedreno-dri3",
    "nodejs", "nodejs-lts", "nexttrace", "ndk-sysroot-gcc-compact",
    "ncspot-mpris", "ncspot", "osmesa", "opencolorio-static",
    "openblas", "mesa-zink", "octave", "obconf", "python-scipy-2", "python-is-python3.9", "python-is-python3.8",
    "python-is-python3.7", "python-is-python3.11", "python-is-python3.10",
    "pulseaudio-static", "pulseaudio-glib-static", "protobuf-static", "pinentry-gtk",
    "parole-static", "php", "php-fpm", "php-pgsql", "php7.2",
    "qemu-system-x86-64-static", "qemu-system-x86-64-headless-static",
    "qemu-system-x86-64-headless", "qemu-system-riscv64-headless",
    "qemu-system-ppc64-headless", "qemu-system-ppc-headless",
    "qemu-system-m68k-headless", "qemu-system-i386-headless",
    "qemu-system-arm-headless", "qemu-system-aarch64-headless",
    "rust-nightly-wasm32-unknown-unknown", "ruby", "rip",
    "rife-ncnn-vulkan-is-nihui", "recoll-static", "rc",
    "radare2-static", "spirv-llvm-translator-glibc-static",
    "spglib-static", "spirv-tools", "sdl2-compat",
    "glslang", "libncnn", "tree-sitter-c-static",
    "transmission", "tmux-sixel", "tinymist",
    "unbound-static", "vulkan-loader-generic",
    "virglrenderer-mesa-zink", "vlc-qt",
    "vim-gtk", "wireless-tools-static",
    "wasmedge-static", "xsv-ucw",
    "xfce4-wavelan-plugin-static", "xfce4-timer-plugin-static",
    "xfce4-places-plugin-static", "xfce4-notes-plugin-static",
    "xfce4-netload-plugin-static", "xfce4-mailwatch-plugin-static",
    "xfce4-genmon-plugin-static", "xfce4-eyes-plugin-static",
    "xfce4-calculator-plugin-static", "zstd-static"
]

def load_blacklist():
    """Load the blacklist from a file."""
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

def save_blacklist(blacklist):
    """Save the blacklist to a file."""
    with open(BLACKLIST_FILE, "w") as file:
        for package in blacklist:
            file.write(f"{package}\n")

def prompt_for_blacklist():
    """Prompt the user to add packages to the blacklist."""
    console.print("[blue]Enter packages to add to the blacklist (comma-separated):[/blue]")
    user_input = input().strip()
    if user_input:
        new_packages = [pkg.strip() for pkg in user_input.split(",")]
        return new_packages
    return []

def get_all_packages():
    """Retrieve the list of all available Termux packages."""
    result = subprocess.run(["pkg", "list-all"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print("[red]Failed to retrieve package list.[/red]")
        return []
    packages = [line.split("/")[0] for line in result.stdout.splitlines() if line]
    return sorted(set(packages))

def is_package_installed(package):
    """Check if a package is already installed."""
    result = subprocess.run(["dpkg", "-s", package], capture_output=True, text=True)
    return result.returncode == 0

def install_package(package, log_success, log_failure):
    """Attempt to install a package and handle errors."""
    if is_package_installed(package):
        console.print(f"[yellow]{package} is already installed. Skipping...[/yellow]")
        return True

    try:
        result = subprocess.run(["pkg", "install", "-y", package], capture_output=True, text=True)
        if result.returncode == 0:
            log_success.write(f"{package}: Successfully installed.\n")
            return True
        else:
            error_message = result.stderr.strip()
            log_failure.write(f"{package}: Failed to install. Error: {error_message}\n")
            # Attempt to fix broken packages and retry installation
            fix_broken_packages()
            result = subprocess.run(["pkg", "install", "-y", package], capture_output=True, text=True)
            if result.returncode == 0:
                log_success.write(f"{package}: Successfully installed after retry.\n")
                return True
            else:
                error_message = result.stderr.strip()
                log_failure.write(f"{package}: Failed to install after retry. Error: {error_message}\n")
                return False
    except Exception as e:
        log_failure.write(f"{package}: Exception occurred: {str(e)}\n")
        return False

def fix_broken_packages():
    """Attempt to fix broken packages."""
    console.print("[yellow]Fixing broken packages...[/yellow]")
    subprocess.run(["apt", "--fix-broken", "install", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    # Load the existing blacklist
    global BLACKLISTED_PACKAGES
    BLACKLISTED_PACKAGES.extend(load_blacklist())

    # Prompt the user to add packages to the blacklist
    new_blacklist_entries = prompt_for_blacklist()
    if new_blacklist_entries:
        BLACKLISTED_PACKAGES.extend(new_blacklist_entries)
        save_blacklist(BLACKLISTED_PACKAGES)

    # Logs and summary files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    success_log_path = f"termux_installed_packages_{timestamp}.log"
    failure_log_path = f"termux_failed_packages_{timestamp}.log"

    with open(success_log_path, "w") as log_success, open(failure_log_path, "w") as log_failure:
        console.print("[blue]Fetching all available Termux packages...[/blue]")
        all_packages = get_all_packages()

        if not all_packages:
            console.print("[red]No packages found.[/red]")
            return

        total_packages = len(all_packages)
        installed_count = 0
        skipped_count = 0

        console.print(f"[green]Found {total_packages} packages.[/green]")

        with Progress() as progress:
            overall_progress = progress.add_task("[cyan]Overall Progress[/cyan]", total=total_packages)
            current_progress = progress.add_task("[blue]Current Package[/blue]", total=1)

            for index, package in enumerate(all_packages, 1):
                # Skip blacklisted packages
                if package in BLACKLISTED_PACKAGES:
                    console.print(f"[yellow]{package} is in the blacklist. Skipping...[/yellow]")
                    skipped_count += 1
                    progress.update(overall_progress, advance=1)
                    continue

                progress.update(current_progress, completed=0, total=1)
                console.print(f"[cyan]Installing {package} ({index}/{total_packages})...[/cyan]")
                success = install_package(package, log_success, log_failure)

                if success:
                    installed_count += 1
                else:
                    skipped_count += 1

                # Update progress bars
                progress.update(current_progress, completed=1)
                progress.update(overall_progress, advance=1)

                # Fix broken packages after each attempt
                fix_broken_packages()

        # Summary
        console.print("\n[bold green]Installation process completed![/bold green]")
        console.print(f"[green]Installed Packages:[/green] {installed_count}")
        console.print(f"[yellow]Skipped Packages:[/yellow] {skipped_count}")

        log_success.write(f"\nTotal Installed Packages: {installed_count}\n")
        log_failure.write(f"\nTotal Skipped Packages: {skipped_count}\n")

if __name__ == "__main__":
    main()
