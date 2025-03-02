#!/data/data/com.termux/files/usr/bin/bash

# Initialize counters
installed_count=0
skipped_count=0

# Ensure package list is up-to-date
echo "Updating package list..."
pkg update -y

# Get the full list of available packages
echo "Fetching list of all available packages..."
package_list=$(pkg list-all | cut -d'/' -f1)

# Total number of packages for reference
total_packages=$(echo "$package_list" | wc -l)
echo "Total packages to attempt: $total_packages"

# Loop through each package
for pkg in $package_list; do
    echo "--------------------------------------------------"
    echo "Attempting to install $pkg..."
    
    # Try to install the package
    if pkg install -y "$pkg" 2>/dev/null; then
        echo "Successfully installed $pkg"
        ((installed_count++))
    else
        echo "Failed to install $pkg, attempting cleanup..."
        
        # Cleanup: Remove any partially installed package and clear cache
        pkg remove -y "$pkg" 2>/dev/null || true
        pkg autoclean 2>/dev/null || true
        
        echo "Skipped $pkg after cleanup"
        ((skipped_count++))
    fi
done

# Final report
echo "--------------------------------------------------"
echo "Installation process complete!"
echo "Total packages attempted: $total_packages"
echo "Packages successfully installed: $installed_count"
echo "Packages skipped: $skipped_count"
echo "Success rate: $((installed_count * 100 / total_packages))%"#!/data/data/com.termux/files/usr/bin/bash

# Initialize counters
installed_count=0
skipped_count=0

# Ensure package list is up-to-date
echo "Updating package list..."
pkg update -y

# Get the full list of available packages
echo "Fetching list of all available packages..."
package_list=$(pkg list-all | cut -d'/' -f1)

# Total number of packages for reference
total_packages=$(echo "$package_list" | wc -l)
echo "Total packages to attempt: $total_packages"

# Loop through each package
for pkg in $package_list; do
    echo "--------------------------------------------------"
    echo "Attempting to install $pkg..."
    
    # Try to install the package
    if pkg install -y "$pkg" 2>/dev/null; then
        echo "Successfully installed $pkg"
        ((installed_count++))
    else
        echo "Failed to install $pkg, attempting cleanup..."
        
        # Cleanup: Remove any partially installed package and clear cache
        pkg remove -y "$pkg" 2>/dev/null || true
        pkg autoclean 2>/dev/null || true
        
        echo "Skipped $pkg after cleanup"
        ((skipped_count++))
    fi
done

# Final report
echo "--------------------------------------------------"
echo "Installation process complete!"
echo "Total packages attempted: $total_packages"
echo "Packages successfully installed: $installed_count"
echo "Packages skipped: $skipped_count"
echo "Success rate: $((installed_count * 100 / total_packages))%"
