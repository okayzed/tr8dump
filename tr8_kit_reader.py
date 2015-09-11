
import re
import sys
from collections import defaultdict


INSTRUMENTS = [
    "BD",
    "SD",
    "LT",
    "MT",
    "HT",
    "RS",
    "HC",
    "CH",
    "OH",
    "CC",
    "RC",
];

VARS = [
    "NUM", # kit number
    "PAN", # pan for it
    "ACC", # respond to accents?
    "GR", # has reverb
    "SE", # has delay
    "LEV" # level of the instrument
]



RULE_RE = re.compile("(\w*_*)\((\d*)\)");
def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

class TR8Kit(object):
    def __init__(self, *args, **kwargs):
        self.misc = defaultdict(int)


    def printKit(self):
        for inst in INSTRUMENTS:
            values = {}
            for rule in VARS:
                values[rule] = self.misc["%s_%s" % (inst, rule)]

            after_str = ""
            if values['ACC'] == 1:
                after_str += "A"
            if values['GR'] == 1:
                after_str += "R"
            if values['SE'] == 1:
                after_str += "D"
                

            print "%s (%s):\tlvl: %s pan: %s" % (inst, values['NUM'], values['LEV'], values['PAN']), after_str

    def readRules(self, lines):
        for line in lines:
            match = RULE_RE.match(line)
            if match:
                self.misc[match.group(1)] = int(match.group(2))
                continue
        pass

def main():
    lines = sys.stdin.readlines()

    pattern = TR8Kit()
    pattern.readRules(lines)
    pattern.printKit()

if __name__ == "__main__":
    main()
