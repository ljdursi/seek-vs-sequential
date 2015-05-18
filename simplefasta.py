#!/usr/bin/env python
import os
import argparse

class FastaReader(object):
    def __init__(self,infile):
        self.__infile = infile
        self.__havenext = False
        self.__next = ""
        self.__end = False

    def readNext(self):
        curlabel = None
        sequences = []

        done = False
        while not done:
            if self.__havenext:
                line = self.__next
                self.__havenext = False
                self.__next = ""
            else:
                line = self.__infile.readline()

            if not line:
                done = True
                self.__end = True
            elif line[0] == ">":
                if curlabel is None:
                    curlabel = line[1:]
                else:
                    self.__havenext = True
                    self.__next = line
                    done = True
            else:
                sequences.append(line.strip())

        if curlabel is None:
            return None
        else:
            return curlabel, "".join(sequences)

    def skipAhead(self, eatLine=False):
        done = False
        if eatLine:
            line = self.__infile.readline()
        while not done:
            line = self.__infile.readline()
            if not line:
                done = True
                self.__end = True
            elif line[0]=='>':
                self.__havenext = True
                self.__next = line.strip()
                break
        return

    def eof(self):
        return self.__end

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-s','--skipto',type=float)
    args = parser.parse_args()

    reader = FastaReader(args.infile)
    if args.skipto is None:
        record = reader.readNext()
        while record:
            print(record)
            record = reader.readNext()
    else:
        args.infile.seek(0, os.SEEK_END)
        size = args.infile.tell()
        if args.skipto < 1:
            loc = size * args.skipto
        else:
            loc = int(args.skipto)
        args.infile.seek(loc, os.SEEK_SET)
        reader.skipAhead()
        print(reader.readNext())
