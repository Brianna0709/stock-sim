#!/usr/bin/env python3
"""Update portfolio.json with 2026-07-21 closing prices and recalculate metrics."""
import json
import os

BASE = '/root/.openclaw/workspace/stock-sim'
DATA = os.path.join(BASE, 'data', 'portfolio.json')

def load():
    with open(DATA, 'r') as f:
        return json.load(f)

def save(d):
    with open(DATA, 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def update_portfolio(today_prices, index_data, note):
    d = load()
    
    # Update positions
    total_invested = 0
    for ticker, price in today_prices.items():
        if ticker in d['positions']:
            p = d['positions'][ticker]
            prev_price = p['cur_price']
            p['cur_price'] = price
            p['market_value'] = round(p['shares'] * price, 2)
            p['pnl'] = round(p['market_value'] - p['cost_basis'], 2)
            p['pnl_pct'] = round((p['pnl'] / p['cost_basis']) * 100, 2)
            p['today_chg_pct'] = round(((price - prev_price) / prev_price) * 100, 2)
            p['unrealized_pnl'] = p['pnl']
            p['unrealized_pnl_pct'] = p['pnl_pct']
            total_invested += p['market_value']
    
    # Update account
    d['account']['invested'] = round(total_invested, 2)
    d['account']['total_value'] = round(d['account']['cash'] + total_invested, 2)
    
    # Update market context
    d['market_context'] = {
        'sp500': index_data['sp500'],
        'sp500_change_pct': index_data['sp500_change_pct'],
        'nasdaq': index_data['nasdaq'],
        'nasdaq_change_pct': index_data['nasdaq_change_pct'],
        'dow': index_data['dow'],
        'dow_change_pct': index_data['dow_change_pct'],
        'note': note
    }
    
    # Add snapshot (avoid duplicate dates)
    return_pct = round((d['account']['total_value'] - d['meta']['initial_capital']) / d['meta']['initial_capital'] * 100, 2)
    snapshot = {
        'date': index_data['date'],
        'total_value': round(d['account']['total_value'], 2),
        'cash': d['account']['cash'],
        'invested': round(d['account']['invested'], 2),
        'return_pct': return_pct,
        'note': note
    }
    
    # Remove existing snapshot for same date
    d['snapshots'] = [s for s in d['snapshots'] if s['date'] != index_data['date']]
    d['snapshots'].append(snapshot)
    
    save(d)
    return d

if __name__ == '__main__':
    # 2026-07-21 美股收盘数据
    today_prices = {
        'NVDA': 207.5,   # 芯片板块强势反弹
        'MSFT': 390.5,   # 温和上涨
        'QQQ': 743.0     # 跟随纳指大涨
    }
    
    index_data = {
        'date': '2026-07-21',
        'sp500': 7509.20,
        'sp500_change_pct': 0.89,
        'nasdaq': 25837.21,
        'nasdaq_change_pct': 1.29,
        'dow': 52224.64,
        'dow_change_pct': 0.74
    }
    
    note = "收盘复盘：NVDA $207.5 (+1.22%) | MSFT $390.5 (+0.39%) | QQQ $743.0 (+1.50%) | 标普500 7509.20(+0.89%) 纳指25837.21(+1.29%) 道指52224.64(+0.74%) | 芯片板块强势反弹，存储多股涨超10%，三大指数集体收涨"
    
    d = update_portfolio(today_prices, index_data, note)
    
    print(f"Portfolio updated for {index_data['date']}")
    print(f"Total value: ${d['account']['total_value']:,.2f}")
    print(f"Return: {(d['account']['total_value'] - 100000) / 100000 * 100:.2f}%")
    for ticker, p in d['positions'].items():
        print(f"  {ticker}: ${p['cur_price']:.2f} ({p['today_chg_pct']:+.2f}%) | PnL: {p['pnl_pct']:+.2f}%")
