#!/usr/bin/env python3
"""
Cisco (CSCO) Stock Price Monitor
Fetches current price, daily change, 52-week range, and optional CSV logging.
Alerts when price moves beyond a configured threshold.
"""

import os
import csv
import datetime
import yfinance as yf

# --- Config (override via env vars) ---
TICKER = os.getenv("STOCK_TICKER", "CSCO")
ALERT_THRESHOLD_PCT = float(os.getenv("ALERT_THRESHOLD_PCT", "3.0"))  # alert on ±3% move
CSV_FILE = os.getenv("CSV_FILE", "price_history.csv")
SAVE_CSV = os.getenv("SAVE_CSV", "true").lower() == "true"


def fetch_stock_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="2d")

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
    week_52_high = info.get("fiftyTwoWeekHigh")
    week_52_low = info.get("fiftyTwoWeekLow")
    company_name = info.get("longName", ticker)
    currency = info.get("currency", "USD")
    market_cap = info.get("marketCap")

    change = current_price - prev_close if current_price and prev_close else None
    change_pct = (change / prev_close * 100) if change and prev_close else None

    return {
        "ticker": ticker,
        "company": company_name,
        "currency": currency,
        "price": current_price,
        "prev_close": prev_close,
        "change": change,
        "change_pct": change_pct,
        "week_52_high": week_52_high,
        "week_52_low": week_52_low,
        "market_cap": market_cap,
        "timestamp": datetime.datetime.now().isoformat(),
    }


def format_market_cap(cap) -> str:
    if cap is None:
        return "N/A"
    if cap >= 1_000_000_000:
        return f"${cap / 1_000_000_000:.2f}B"
    if cap >= 1_000_000:
        return f"${cap / 1_000_000:.2f}M"
    return f"${cap:,.0f}"


def print_summary(data: dict):
    change_sign = "+" if (data["change"] or 0) >= 0 else ""
    change_arrow = "▲" if (data["change"] or 0) >= 0 else "▼"
    pct = data["change_pct"]

    print("=" * 50)
    print(f"  {data['company']} ({data['ticker']})")
    print("=" * 50)
    print(f"  Price:        {data['currency']} {data['price']:.2f}")
    if data["change"] is not None:
        print(f"  Change:       {change_arrow} {change_sign}{data['change']:.2f} ({change_sign}{pct:.2f}%)")
    print(f"  Prev Close:   {data['currency']} {data['prev_close']:.2f}")
    print(f"  52-Wk High:   {data['currency']} {data['week_52_high']:.2f}")
    print(f"  52-Wk Low:    {data['currency']} {data['week_52_low']:.2f}")
    print(f"  Market Cap:   {format_market_cap(data['market_cap'])}")
    print(f"  As of:        {data['timestamp']}")
    print("=" * 50)


def check_alerts(data: dict, threshold_pct: float):
    pct = data.get("change_pct")
    if pct is None:
        return
    if abs(pct) >= threshold_pct:
        direction = "UP" if pct > 0 else "DOWN"
        print(f"\n⚠️  ALERT: {data['ticker']} is {direction} {abs(pct):.2f}% today "
              f"(threshold: ±{threshold_pct}%)\n")


def save_to_csv(data: dict, filepath: str):
    file_exists = os.path.isfile(filepath)
    fieldnames = ["timestamp", "ticker", "price", "change", "change_pct",
                  "prev_close", "week_52_high", "week_52_low", "market_cap"]
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: data.get(k) for k in fieldnames})
    print(f"  [CSV] Saved to {filepath}")


def main():
    print(f"\nFetching {TICKER} stock data...\n")
    data = fetch_stock_data(TICKER)
    print_summary(data)
    check_alerts(data, ALERT_THRESHOLD_PCT)
    if SAVE_CSV:
        save_to_csv(data, CSV_FILE)


if __name__ == "__main__":
    main()
