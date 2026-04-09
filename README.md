# Cisco Stock Price Monitor 📈

Monitor Cisco (CSCO) stock price from the terminal. No API key needed — uses Yahoo Finance.

## Features

- Current price, daily change & % move
- 52-week high / low
- Market cap
- **Alerts** when price moves ±X% in a day
- Optional CSV price history log

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python monitor.py
```

## Configuration (env vars)

| Variable             | Default            | Description                          |
|----------------------|--------------------|--------------------------------------|
| `STOCK_TICKER`       | `CSCO`             | Stock ticker symbol                  |
| `ALERT_THRESHOLD_PCT`| `3.0`              | Alert when daily move exceeds ±X%    |
| `SAVE_CSV`           | `true`             | Save price snapshot to CSV           |
| `CSV_FILE`           | `price_history.csv`| Path to the CSV history file         |

### Examples

```bash
# Monitor a different stock
STOCK_TICKER=AAPL python monitor.py

# Set a tighter alert threshold (1%)
ALERT_THRESHOLD_PCT=1.0 python monitor.py

# Disable CSV logging
SAVE_CSV=false python monitor.py
```

## Sample Output

```
Fetching CSCO stock data...

==================================================
  Cisco Systems, Inc. (CSCO)
==================================================
  Price:        USD 52.34
  Change:       ▼ -0.41 (-0.78%)
  Prev Close:   USD 52.75
  52-Wk High:   USD 60.12
  52-Wk Low:    USD 44.50
  Market Cap:   $212.50B
  As of:        2026-04-09T15:00:00
==================================================
```
