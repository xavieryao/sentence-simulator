import json
import codecs
import argparse

from numpy import random

from utils.tag import tag_iob2
from utils.hierarchy import hierarchy, link_entity, str_stat
from utils.output import Output


def map_labels(filename, out):

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
      with open(out, 'w', encoding='utf8') as of:
        json.dump(mapping, of)


random.seed(0)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, help='input file')
parser.add_argument('-w', '--lv_word', help='word level output')
parser.add_argument('-s', '--lv_sentence', help='sentence level')
parser.add_argument('-m', '--lv_map', help='mapping file')
parser.add_argument('-c', '--count', type=int, help='sentence count', default=1000)

args = parser.parse_args()

with codecs.open(args.file, 'r', encoding='utf-8') as fin:
  setting = json.load(fin)
  result = hierarchy(setting['rule'])
  if result[0]:
    root = result[1]
    entity_map = link_entity(result[2], setting['entity'])
    print(str_stat(result[2], entity_map))
    output = Output(root, entity_map)
    if args.lv_word is not None:
      output.addOutput(Output.WORD_LEVEL, args.lv_word, tag_iob2)
    if args.lv_sentence is not None:
      output.addOutput(Output.SENTENCE_LEVEL, args.lv_sentence, tag_iob2)
    output.generate(args.count)
    map_labels(args.lv_sentence, args.lv_map)