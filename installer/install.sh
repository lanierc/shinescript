#!/bin/bash

# Configuration
SOURCE_DIR="../shines"
SHARE_DEST="/usr/share/shines"
BIN_DEST="/usr/bin/shines"

# 1. Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script with sudo."
  echo "Usage: sudo ./install.sh"
  exit 1
fi

echo "Starting ShineScript Installation..."

# 2. Verify source exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Directory '$SOURCE_DIR' not found in current folder."
  exit 1
fi

# 3. Install files to /usr/share
echo "Copying assets to $SHARE_DEST..."
if [ -d "$SHARE_DEST" ]; then
    rm -rf "$SHARE_DEST"
fi
cp -r "$SOURCE_DIR" "$SHARE_DEST"

# 4. Create the global executable wrapper
echo "Creating global 'shines' command..."
cat <<EOF > "$BIN_DEST"
#!/bin/bash
# ShineScript Global Wrapper
python3 "$SHARE_DEST/main.py" "\$@"
EOF

# 5. Set Permissions
chmod +x "$BIN_DEST"
chmod -R 755 "$SHARE_DEST"

echo "ShineScript installed successfully!"
echo "You can now run code using: shines your_file.ss"
