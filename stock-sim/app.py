#!/usr/bin/env python3
"""
万能小汪 · 虚拟模拟盘 后端服务
"""
import json, os, datetime, threading, time
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, 'data', 'portfolio.json')

app = Flask(__name__, static_folder=BASE)
CORS(app)

# ── 数据读写 ──────────────────────────────────────────────
def load():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── 价格抓取（yfinance）────────────────────────────────────
def fetch_prices(tickers):
    """返回 {ticker: price} dict，失败返回 None"""
    try:
        import yfinance as yf
        result = {}
        for t in tickers:
            tk = yf.Ticker(t)
            hist = tk.history(period='2d')
            if not hist.empty:
                result[t] = round(float(hist['Close'].iloc[-1]), 2)
        return result
    except Exception as e:
        print(f"[price fetch error] {e}")
        return {}

# ── 更新持仓现价 & 快照 ───────────────────────────────────
def refresh_prices():
    data = load()
    positions = data.get('positions', {})
    if not positions:
        return
    tickers = list(positions.keys())
    prices = fetch_prices(tickers)
    if not prices:
        return

    total_market = 0
    for ticker, pos in positions.items():
        if ticker in prices:
            pos['cur_price'] = prices[ticker]
            pos['market_value'] = round(pos['shares'] * prices[ticker], 2)
            pos['pnl'] = round(pos['market_value'] - pos['cost_basis'], 2)
            pos['pnl_pct'] = round((pos['cur_price'] - pos['cost_price']) / pos['cost_price'] * 100, 2)
        total_market += pos.get('market_value', 0)

    total = round(data['account']['cash'] + total_market, 2)
    data['account']['total_value'] = total
    data['account']['invested'] = round(total_market, 2)

    initial = data['meta']['initial_capital']
    ret_pct = round((total - initial) / initial * 100, 2)

    # 追加快照（每天一条）
    today = datetime.date.today().strftime('%Y-%m-%d')
    snaps = data.get('snapshots', [])
    if not snaps or snaps[-1]['date'] != today:
        snaps.append({
            'date': today,
            'total_value': total,
            'cash': data['account']['cash'],
            'invested': total_market,
            'return_pct': ret_pct
        })
        data['snapshots'] = snaps

    save(data)
    print(f"[{datetime.datetime.now():%H:%M:%S}] prices refreshed: {prices}")

# ── 后台定时刷新（每30分钟）──────────────────────────────
def background_refresh():
    while True:
        try:
            refresh_prices()
        except Exception as e:
            print(f"[bg refresh error] {e}")
        time.sleep(1800)  # 30 min

# ── API 路由 ─────────────────────────────────────────────

@app.route('/api/portfolio')
def api_portfolio():
    data = load()
    positions = data.get('positions', {})
    tickers = list(positions.keys())

    # 实时价格（可选，加 ?live=1）
    if request.args.get('live') == '1' and tickers:
        prices = fetch_prices(tickers)
        for t, pos in positions.items():
            if t in prices:
                pos['cur_price'] = prices[t]
                pos['market_value'] = round(pos['shares'] * prices[t], 2)
                pos['pnl_pct'] = round((prices[t] - pos['cost_price']) / pos['cost_price'] * 100, 2)

    # 重算总资产
    total_market = sum(p.get('market_value', 0) for p in positions.values())
    total = round(data['account']['cash'] + total_market, 2)
    initial = data['meta']['initial_capital']
    ret_pct = round((total - initial) / initial * 100, 4)
    max_dd = calc_max_drawdown(data.get('snapshots', []))

    return jsonify({
        'meta': data['meta'],
        'account': {
            **data['account'],
            'total_value': total,
            'invested': total_market,
            'return_pct': ret_pct,
            'max_drawdown': max_dd,
        },
        'positions': positions,
        'trades': data.get('trades', []),
        'snapshots': data.get('snapshots', []),
        'pending_plan': data.get('pending_plan', []),
        'market_context': data.get('market_context', {}),
        'refreshed_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/trade', methods=['POST'])
def api_trade():
    """执行交易：buy / sell"""
    body = request.json
    action = body.get('action')  # buy | sell
    ticker = body.get('ticker', '').upper()
    shares = float(body.get('shares', 0))
    price  = float(body.get('price', 0))
    note   = body.get('note', '')

    if not ticker or shares <= 0 or price <= 0:
        return jsonify({'error': 'invalid params'}), 400

    data = load()
    amount = round(shares * price, 2)

    if action == 'buy':
        if data['account']['cash'] < amount:
            return jsonify({'error': 'insufficient cash'}), 400
        data['account']['cash'] = round(data['account']['cash'] - amount, 2)
        if ticker not in data['positions']:
            data['positions'][ticker] = {
                'shares': 0, 'cost_price': price,
                'cost_basis': 0, 'cur_price': price,
                'market_value': 0, 'pnl': 0, 'pnl_pct': 0
            }
        pos = data['positions'][ticker]
        total_shares = pos['shares'] + shares
        pos['cost_price'] = round((pos['cost_basis'] + amount) / total_shares, 4)
        pos['shares'] = total_shares
        pos['cost_basis'] = round(pos['cost_basis'] + amount, 2)
        pos['cur_price'] = price
        pos['market_value'] = round(total_shares * price, 2)
        pos['pnl'] = 0
        pos['pnl_pct'] = 0

    elif action == 'sell':
        if ticker not in data['positions']:
            return jsonify({'error': 'no position'}), 400
        pos = data['positions'][ticker]
        if pos['shares'] < shares:
            return jsonify({'error': 'insufficient shares'}), 400
        data['account']['cash'] = round(data['account']['cash'] + amount, 2)
        pos['shares'] = round(pos['shares'] - shares, 6)
        pos['cost_basis'] = round(pos['shares'] * pos['cost_price'], 2)
        if pos['shares'] <= 0:
            del data['positions'][ticker]

    # 记录交易
    trade_id = len(data['trades']) + 1
    data['trades'].insert(0, {
        'id': trade_id,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'type': action,
        'ticker': ticker,
        'shares': shares,
        'price': price,
        'amount': amount,
        'note': note
    })
    save(data)
    return jsonify({'ok': True, 'trade_id': trade_id})

@app.route('/api/refresh')
def api_refresh():
    """手动触发价格刷新"""
    refresh_prices()
    return jsonify({'ok': True, 'time': datetime.datetime.now().isoformat()})

@app.route('/api/snapshot', methods=['POST'])
def api_snapshot():
    """手动追加每日快照"""
    data = load()
    body = request.json or {}
    today = datetime.date.today().strftime('%Y-%m-%d')
    total = data['account']['total_value']
    initial = data['meta']['initial_capital']
    ret_pct = round((total - initial) / initial * 100, 2)
    snap = {
        'date': body.get('date', today),
        'total_value': total,
        'cash': data['account']['cash'],
        'invested': data['account']['invested'],
        'return_pct': ret_pct,
        'note': body.get('note', '')
    }
    snaps = data.get('snapshots', [])
    # 更新或追加
    existing = [i for i, s in enumerate(snaps) if s['date'] == snap['date']]
    if existing:
        snaps[existing[0]] = snap
    else:
        snaps.append(snap)
    data['snapshots'] = snaps
    save(data)
    return jsonify({'ok': True, 'snapshot': snap})

# ── 最大回撤计算 ─────────────────────────────────────────
def calc_max_drawdown(snapshots):
    if len(snapshots) < 2:
        return 0.0
    values = [s['total_value'] for s in snapshots]
    peak = values[0]
    max_dd = 0.0
    for v in values:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100
        if dd > max_dd:
            max_dd = dd
    return round(max_dd, 2)

# ── 静态文件 ─────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE, filename)

if __name__ == '__main__':
    # 后台刷新线程
    t = threading.Thread(target=background_refresh, daemon=True)
    t.start()
    print("🐕 万能小汪模拟盘服务启动 → http://0.0.0.0:18899")
    app.run(host='0.0.0.0', port=18899, debug=False)
