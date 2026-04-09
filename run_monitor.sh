#!/bin/bash
set -e

REPO_DIR="/home/elidrisi/projects/cisco-stock-monitor"
cd "$REPO_DIR"

# Install deps quietly
/usr/bin/python3 -m pip install -q -r requirements.txt

# Run monitor (appends to price_history.csv)
/usr/bin/python3 monitor.py 2>&1 | tee -a /tmp/cisco_stock.log

# Commit and push price_history.csv to GitHub
git config user.email "melidrisi@github.com"
git config user.name "Strongmad Bot"

git add price_history.csv
# Only commit if there's something new
if ! git diff --cached --quiet; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M %Z')
    git commit -m "data: CSCO price snapshot $TIMESTAMP"
    git push origin main
    echo "[git] Pushed price_history.csv to GitHub" | tee -a /tmp/cisco_stock.log
else
    echo "[git] No new data to push" | tee -a /tmp/cisco_stock.log
fi
