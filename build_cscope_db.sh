#!/bin/bash
#
#  Run cscope for kernel tree
#
#  Ref: http://naseer.in/use-cscope-to-browse-the-android-source-code
#


echo "Clean old database..."
rm -f cscope.*
rm -f tags

echo "ctags first..."
ctags -R *

echo "Listing kernel files..."
LNX=$(pwd)

# excluded folders here
find .                               \
    -path "./arch/*" -prune -o         \
    -path "./tmp*" -prune -o           \
    -path "./Documentation*" -prune -o \
    -path "./scripts*" -prune -o       \
    -path "./drivers*" -prune -o       \
    -path "./tools*" -prune -o       \
    -name "*.[chxsS]" -print > cscope.files

# included folders under arch/
find "./arch/arm/include/"    \
     "./arch/arm/kernel/"     \
     "./arch/arm/common/"     \
     "./arch/arm/boot/"       \
     "./arch/arm/lib/"        \
     "./arch/arm/mm/"         \
     "./arch/arm/mach-tegra/" \
     -name "*.[chxsS]" -print >> cscope.files

# included folders under drivers/
find "./drivers/acpi/"  \
     "./drivers/base/"  \
     "./drivers/gpio/"  \
     "./drivers/i2c/"   \
     "./drivers/misc/"  \
     "./drivers/power/" \
     "./drivers/usb/"   \
     "./drivers/tty/"   \
     "./drivers/rtc/"   \
     "./drivers/cpufreq/"   \
     -name "*.[chxsS]" -print >> cscope.files

file_count=`wc -l cscope.files | cut -d' ' -f1`
echo "File count:${file_count}"

# create db now
echo "Creating cscope databases..."
time /usr/bin/cscope -bkqU
#/usr/bin/cscope -bkqRU #regular command for all folder
echo "Done"

