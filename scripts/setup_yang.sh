#!/bin/bash
# ============================================================
# Day 5 — Part 1: YANG setup (Lab 8.3.5)
# Run this script inside DEVASC VM or your Linux environment
# ============================================================

set -e

YANG_DIR="artifacts/day5/yang"
mkdir -p "$YANG_DIR"

echo "=== Step 1: Install/upgrade pyang ==="
pip install pyang --upgrade --quiet
pyang --version | tee "$YANG_DIR/pyang_version.txt"

echo ""
echo "=== Step 2: Download ietf-interfaces.yang ==="
YANG_URL="https://raw.githubusercontent.com/YangModels/yang/main/vendor/cisco/xe/1693/ietf-interfaces.yang"
FALLBACK_URL="https://raw.githubusercontent.com/YangModels/yang/main/standard/ietf/RFC/ietf-interfaces.yang"

if wget -q -O "$YANG_DIR/ietf-interfaces.yang" "$YANG_URL"; then
    echo "  ✓ Downloaded from Cisco XE 1693"
elif wget -q -O "$YANG_DIR/ietf-interfaces.yang" "$FALLBACK_URL"; then
    echo "  ✓ Downloaded from IETF standard (fallback)"
else
    echo "  ERROR: Could not download ietf-interfaces.yang"
    exit 1
fi

echo ""
echo "=== Step 3: Run pyang -f tree ==="
cd "$YANG_DIR"
pyang -f tree ietf-interfaces.yang 2>&1 | tee pyang_tree.txt
cd -

echo ""
echo "=== Evidence files ==="
ls -la "$YANG_DIR/"
echo ""
echo "  ✓ YANG part done! Check artifacts/day5/yang/"
