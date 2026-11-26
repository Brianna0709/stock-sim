import json
p='/root/.openclaw/workspace/stock-sim/data/portfolio.json'
d=json.load(open(p))
prices={'QQQ':650.38,'NVDA':165.73,'MSFT':496.58}
chg={'QQQ':6.89,'NVDA':32.02,'MSFT':2.49}
cash=d['account']['cash']
prev_total=d['account']['total_value']
total=0
for t,pos in d['positions'].items():
    px=prices[t]
    pos['prev_price']=pos['cur_price']
    pos['cur_price']=px
    pos['market_value']=round(pos['shares']*px,2)
    pos['pnl']=round(pos['market_value']-pos['cost_basis'],2)
    pos['pnl_pct']=round(pos['pnl']/pos['cost_basis']*100,2)
    pos['unrealized_pnl']=pos['pnl']
    pos['unrealized_pnl_pct']=pos['pnl_pct']
    pos['today_chg_pct']=chg[t]
    total+=pos['market_value']
mv=round(total,2)
acc=d['account']
acc['market_value']=mv
acc['invested']=mv
acc['total_value']=round(mv+cash,2)
acc['total_unrealized_pnl']=round(mv-sum(x['cost_basis'] for x in d['positions'].values()),2)
acc['daily_pnl']=round(acc['total_value']-prev_total,2)
acc['total_pnl']=round(acc['total_value']-100000,2)
acc['total_pnl_pct']=round(acc['total_pnl']/1000,2)
acc['return_pct']=acc['total_pnl_pct']
acc['last_update']='2026-11-23'
acc['market_context']={'sp500':7237.39,'sp500_change_pct':4.73,'nasdaq':24089.56,'nasdaq_change_pct':6.51,'dow':49595.79,'dow_change_pct':3.01}
note=("收盘复盘(2026-11-23周一)：道指49595.79(+3.01% 涨1448点) 标普500 7237.39(+4.73%) 纳指24089.56(+6.51% 标普纳指创2025年4月以来最大单日涨幅) | "
 "NVDA $165.73(+32.02% 黄仁勋复职任董事长兼CEO 单日市值+9520亿美元创纪录 2003年以来最大单日涨幅) | MSFT $496.58(+2.49%) | QQQ $650.38(+6.89%) | "
 "费半+14.03%创2025年来最大单日涨幅 SK海力士+20% 美光+19% 英特尔+16.3% 台积电+14.1% 阿斯麦+9.3% CoreWeave+22% 特斯拉+11.5% Meta+6.5% 谷歌+6.3%；Anthropic逆势-1.4%；"
 "油价大跌WTI -3.88%报80.17(三个月低点) 黄金+3.41%报3635 美元指数104.3；联储威廉姆斯称通胀仍过高、风险偏上行")
snap={'date':'2026-11-23','total_value':acc['total_value'],'cash':cash,'market_value':mv,'invested':mv,
 'daily_pnl':acc['daily_pnl'],'total_pnl':acc['total_pnl'],'total_pnl_pct':acc['total_pnl_pct'],'return_pct':acc['return_pct'],'note':note}
acc['snapshots'].append(snap)
if 'snapshots' in d: d['snapshots'].append(snap)
json.dump(d,open(p,'w'),ensure_ascii=False,indent=2)
print(json.dumps({'positions':{k:{'px':v['cur_price'],'mv':v['market_value'],'pnl':v['pnl'],'pct':v['pnl_pct'],'prev':v['prev_price']} for k,v in d['positions'].items()},
 'acc':{k:acc[k] for k in ['cash','total_value','market_value','daily_pnl','total_pnl','total_pnl_pct']}},ensure_ascii=False,indent=1))
