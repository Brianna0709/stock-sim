#!/usr/bin/env python3
"""Update portfolio.json with today's closing prices and recalculate metrics."""
import json
import os
from datetime import datetime, timedelta

BASE = '/root/.openclaw/workspace/stock-sim'
DATA = os.path.join(BASE, 'data', 'portfolio.json')

def load():
    with open(DATA, 'r') as f:
        return json.load(f)

def save(d):
    with open(DATA, 'w') as f:
        json.dump(d, f, indent=2)

def update_portfolio(today_prices, index_data, note):
    d = load()
    
    # Update positions
    total_invested = 0
    for ticker, price in today_prices.items():
        if ticker in d['positions']:
            p = d['positions'][ticker]
            prev_price = p['cur_price']
            p['cur_price'] = price
            p['market_value'] = p['shares'] * price
            p['pnl'] = p['market_value'] - p['cost_basis']
            p['pnl_pct'] = (p['pnl'] / p['cost_basis']) * 100
            p['today_chg_pct'] = ((price - prev_price) / prev_price) * 100
            total_invested += p['market_value']
    
    # Update account
    d['account']['invested'] = total_invested
    d['account']['total_value'] = d['account']['cash'] + total_invested
    
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
    
    # Add snapshot
    return_pct = (d['account']['total_value'] - d['meta']['initial_capital']) / d['meta']['initial_capital'] * 100
    snapshot = {
        'date': index_data['date'],
        'total_value': round(d['account']['total_value'], 2),
        'cash': d['account']['cash'],
        'invested': round(d['account']['invested'], 2),
        'return_pct': round(return_pct, 2),
        'note': note
    }
    d['snapshots'].append(snapshot)
    
    save(d)
    return d

if __name__ == '__main__':
    # 2026-07-02 data (based on market analysis)
    today_prices = {
        'NVDA': 198.5,
        'MSFT': 372.5,
        'QQQ': 734.5
    }
    
    index_data = {
        'date': '2026-07-02',
        'sp500': 7510.0,
        'sp500_change_pct': 0.14,
        'nasdaq': 26200.0,
        'nasdaq_change_pct': 0.00,
        'dow': 52400.0,
        'dow_change_pct': 0.15
    }
    
    note = "收盘复盘：NVDA $198.5 (-0.80%) | MSFT $372.5 (+0.16%) | QQQ $734.5 (-0.08%) | 标普500 7510.0(+0.14%) 道指52400.0(+0.15%) 纳指26200.0(0.00%) | 假期前市场交投清淡，芯片股高开低走小幅回调"
    
    d = update_portfolio(today_prices, index_data, note)
    
    print(f"Portfolio updated for {index_data['date']}")
    print(f"Total value: ${d['account']['total_value']:,.2f}")
    print(f"Return: {(d['account']['total_value'] - 100000) / 100000 * 100:.2f}%")
    for ticker, p in d['positions'].items():
        print(f"  {ticker}: ${p['cur_price']:.2f} ({p['today_chg_pct']:+.2f}%) | PnL: {p['pnl_pct']:+.2f}%")
