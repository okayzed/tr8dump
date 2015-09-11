import re
import sys
from collections import defaultdict


EFFECTS = [
    "ECHO1",
    "ECHO2",
    "ACC1",
    "ACC2",
    "REV1",
    "REV2"
];

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

RULE_RE = re.compile("(\w*_*)\((\d*)\)");
STEP_RE = re.compile("STEP_(\w*)\((\d*)\)")
ACC_RE = re.compile("ACC_(\w*)\((\d*)\)")
FLAM_RE = re.compile("FLAM_(\w*)\((\d*)\)")

def testBit(int_type, offset):
    mask = 1 << offset
    return(int_type & mask)

class TR8Pattern(object):
    def __init__(self, *args, **kwargs):
        self.steps = defaultdict(lambda: defaultdict(int))
        self.flams = defaultdict(lambda: defaultdict(int))
        self.accents = defaultdict(lambda: defaultdict(int))
        self.misc = defaultdict(int)

    def printPattern(self):
        noBits = []
        last_step_a = self.misc['LAST_A'] + 1
        last_step_b = self.misc['LAST_B'] + 1
        scale = self.misc['SCALE']

        if scale == 0:
            divisor = 3
        if scale == 1:
            divisor = 6
        if scale == 2:
            divisor = 4
        if scale == 3:
            divisor = 8

        for instrument in INSTRUMENTS:
            a_str = ["-"] * last_step_a
            b_str = ["-"] * last_step_b
            is_on = self.steps[instrument + "1"]
            is_acc = self.accents[instrument + "1"]
            someBitSet = False

            for x in xrange(0, last_step_a):
                if testBit(is_on, x):
                    a_str[x] = 'x'
                    someBitSet = True
                    if testBit(is_acc, x):
                        a_str[x] = 'o'

            is_on = self.steps[instrument + "2"]
            is_acc = self.accents[instrument + "2"]
            for x in xrange(0, last_step_b):
                if testBit(is_on, x):
                    someBitSet = True
                    b_str[x] = 'x'
                    if testBit(is_acc, x):
                        b_str[x] = 'o'

            for i in xrange(len(a_str) - 1, 0, -1):
                if i % divisor == 0:
                    a_str.insert(i, "|")
                    b_str.insert(i, "|")

            print "%s: %s  %s" % (instrument, "".join(a_str), "".join(b_str))

            if not someBitSet:
                noBits.append(instrument)

        if len(noBits) > 0:
            print "EMPTY: %s" % (",".join(noBits))

        vari = self.misc["VARI"]
        if vari == 0:
            print "STARTS WITH A ONLY"
        if vari == 1:
            print "STARTS WITH B ONLY"
        if vari == 2:
            print "STARTS WITH A/B ON"






    def readRules(self, lines):
        for line in lines:
            match = STEP_RE.match(line)
            if match:
                self.steps[match.group(1)] = int(match.group(2))
                continue

            match = FLAM_RE.match(line)
            if match:
                self.flams[match.group(1)] = int(match.group(2))
                continue

            match = ACC_RE.match(line)
            if match:
                self.accents[match.group(1)] = int(match.group(2))
                continue

            match = RULE_RE.match(line)
            if match:
                self.misc[match.group(1)] = int(match.group(2))
                continue
        pass

def main():
    lines = sys.stdin.readlines()

    pattern = TR8Pattern()
    pattern.readRules(lines)
    pattern.printPattern()

if __name__ == "__main__":
    main()
