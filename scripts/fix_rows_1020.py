import re

with open('standalone.html', 'r') as f:
    html = f.read()

# QQQ
html = html.replace('<td class="py-3 px-4">$731.00</td><td class="py-3 px-4">25.9884</td>',
                    '<td class="py-3 px-4">$717.63</td><td class="py-3 px-4">25.9884</td>')
html = html.replace('<td class="py-3 px-4">$18,997.52</td><td class="py-3 px-4 text-green-400">+26.65%</td><td class="py-3 px-4 text-red-400">-2.00%</td>',
                    '<td class="py-3 px-4">$18,650.06</td><td class="py-3 px-4 text-green-400">+24.33%</td><td class="py-3 px-4 text-red-400">-0.10%</td>')
# NVDA
html = html.replace('<td class="py-3 px-4">$221.51</td><td class="py-3 px-4">86.0092</td>',
                    '<td class="py-3 px-4">$216.47</td><td class="py-3 px-4">86.0092</td>')
html = html.replace('<td class="py-3 px-4">$19,051.90</td><td class="py-3 px-4 text-green-400">+27.01%</td><td class="py-3 px-4 text-red-400">-3.07%</td>',
                    '<td class="py-3 px-4">$18,618.41</td><td class="py-3 px-4 text-green-400">+24.12%</td><td class="py-3 px-4 text-red-400">-0.29%</td>')
# MSFT
html = html.replace('<td class="py-3 px-4">$533.69</td><td class="py-3 px-4">54.0292</td>',
                    '<td class="py-3 px-4">$531.87</td><td class="py-3 px-4">54.0292</td>')
html = html.replace('<td class="py-3 px-4">$28,834.84</td><td class="py-3 px-4 text-green-400">+44.17%</td><td class="py-3 px-4 text-red-400">-1.80%</td>',
                    '<td class="py-3 px-4">$28,736.51</td><td class="py-3 px-4 text-green-400">+43.68%</td><td class="py-3 px-4 text-red-400">-0.31%</td>')

with open('standalone.html', 'w') as f:
    f.write(html)
print('rows fixed')
