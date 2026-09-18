p = '/root/.openclaw/workspace/weekly_report_ics.md'
lines = open(p, encoding='utf-8').read().split('\n')
# revert accidental appends on monthly table (lines 14-19, 0-indexed 13-18): remove last cell
for i in range(13, 19):
    ln = lines[i]
    assert ln.rstrip().endswith('|'), ln
    # remove trailing ' <val> |'
    idx = ln.rstrip().rfind('| ', 0, len(ln.rstrip()) - 1)
    lines[i] = ln.rstrip()[:idx + 1]
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('\n'.join(lines[12:19]))
