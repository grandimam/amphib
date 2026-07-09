#!/usr/bin/env bash
set -euo pipefail

REPO="grandimam/amphib"
BRANCH="main"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC}   $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
err()   { echo -e "${RED}[err]${NC}  $*"; exit 1; }

# --- check python ---
PYTHON=$(command -v python3 || command -v python || true)
if [ -z "$PYTHON" ]; then
    err "Python not found. Install Python 3.12+ first."
fi

PYVER=$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYMAJ=$("$PYTHON" -c 'import sys; print(sys.version_info.major)')
PYMIN=$("$PYTHON" -c 'import sys; print(sys.version_info.minor)')

if [ "$PYMAJ" -lt 3 ] || { [ "$PYMAJ" -eq 3 ] && [ "$PYMIN" -lt 12 ]; }; then
    err "Python 3.12+ required (found $PYVER)."
fi
ok "Python $PYVER"

# --- create directory ---
INSTALL_DIR="${AMPHIB_DIR:-$HOME/.amphib}"
if [ -d "$INSTALL_DIR" ]; then
    warn "Directory $INSTALL_DIR already exists."
else
    mkdir -p "$INSTALL_DIR"
    ok "Created $INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# --- download source ---
info "Downloading amphib..."
TMP=$(mktemp -d)
trap 'rm -rf $TMP' EXIT

if command -v curl &>/dev/null; then
    curl -sSL "https://api.github.com/repos/$REPO/tarball/$BRANCH" -o "$TMP/amphib.tar.gz"
elif command -v wget &>/dev/null; then
    wget -q "https://api.github.com/repos/$REPO/tarball/$BRANCH" -O "$TMP/amphib.tar.gz"
else
    err "Need curl or wget to download."
fi

tar -xzf "$TMP/amphib.tar.gz" -C "$TMP"
SRC_DIR=$(find "$TMP" -maxdepth 2 -type d -name 'amphib-*' | head -1)
if [ -z "$SRC_DIR" ]; then
    SRC_DIR=$(find "$TMP" -maxdepth 2 -type d -name 'grandimam-amphib-*' | head -1)
fi
if [ -z "$SRC_DIR" ]; then
    err "Could not find source directory in the archive."
fi

cp -R "$SRC_DIR/"* "$INSTALL_DIR/"
ok "Downloaded to $INSTALL_DIR"

# --- create venv ---
if [ -d ".venv" ]; then
    warn "Virtual environment already exists."
else
    "$PYTHON" -m venv .venv
    ok "Created virtual environment"
fi

source .venv/bin/activate

# --- install ---
info "Installing dependencies..."
pip install -q -e .
ok "Installed"

# --- .env ---
if [ -f ".env" ]; then
    warn ".env already exists, not overwriting."
else
    cp .env.example .env
    ok "Created .env from .env.example"
fi

# --- symlink ---
LINK_TARGET="${AMPHIB_LINK:-$HOME/.local/bin}"
if [ -d "$LINK_TARGET" ]; then
    if [ -f "$LINK_TARGET/amphib" ]; then
        rm "$LINK_TARGET/amphib"
    fi
    ln -s "$INSTALL_DIR/.venv/bin/amphib" "$LINK_TARGET/amphib"
    ok "Linked amphib to $LINK_TARGET/amphib"
    echo ""
    info "Make sure $LINK_TARGET is in your PATH:"
    echo "  export PATH=\"\$PATH:$LINK_TARGET\""
else
    warn "$LINK_TARGET does not exist. Skipping symlink."
    info "Run amphib directly:"
    echo "  $INSTALL_DIR/.venv/bin/amphib --help"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  amphib installed!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "  Next steps:"
echo "  1. Edit $INSTALL_DIR/.env"
echo "     Add your OpenRouter API key:"
echo "     OPENROUTER_API_KEY=sk-or-v1-..."
echo ""
echo "  2. Run on a sample resume:"
echo "     amphib analyze $INSTALL_DIR/examples/java-engineer.pdf"
echo "     amphib extract $INSTALL_DIR/examples/java-engineer.pdf"
echo "     amphib evaluate $INSTALL_DIR/examples/java-engineer.pdf"
echo ""
