import sys
import json

filename = sys.argv[1]

i = 0
mapping = {}
with open(filename, encoding='utf8') as f:
    for line in f:
        label = line.split('\t')[0]
        if label not in mapping:
            mapping[label] = i
            i += 1
    f.seek(0)
    with open(filename + '.mapped', 'w', encoding='utf8') as of:
        for line in f:
            label, sent = line.split('\t')
            of.write("{}\t{}".format(mapping[label], sent))
    with open('mapping.json', 'w', encoding='utf8') as of:
        json.dump(mapping, of)
