#!/usr/bin/env python
import argparse
import sys
import gzip
import os
import simplefasta
import random
import struct

# Reservoir sampling - pick N records out of a stream of unkonwn length
# See, eg, http://en.wikipedia.org/wiki/Reservoir_sampling
def reservoir(infile, nrecords):
    reader = simplefasta.FastaReader(infile)
    results = [0]*nrecords
    for i in range(nrecords):
        results[i] = reader.readNext()

    countsSoFar = nrecords
    while not reader.eof():
        loc = random.randint(0,countsSoFar-1)
        if loc < nrecords:
            record = reader.readNext()
            if record:
                results[loc] = record
        else:
            reader.skipAhead(True)
        countsSoFar += 1
    return results        

def randomSeek(infile, size, nrecords):
    infile.seek(0, os.SEEK_SET)

    totrecords = 0
    recordsdict = {}
    while totrecords < nrecords:
        locations = []
        for i in range(nrecords-totrecords):
            locations.append(int(random.uniform(0,size)))
        locations.sort()

        reader = simplefasta.FastaReader(infile)
        for location in locations:
            infile.seek(location,os.SEEK_SET)
            reader.skipAhead()
            record = reader.readNext()
            recordsdict[record[0]] = record[1]
        totrecords = len(recordsdict)
    records = []
    for k,v in recordsdict.items():
        records.append((k,v))
    return records

def getFileSize(filename):
    if filename.endswith(".gz"):
        with open(filename,'rb') as f:
            f.seek(-4,os.SEEK_END)
            size,  = struct.unpack('<I',f.read(4))
            f.close()
    else:
        size = os.stat(filename).st_size
    print("size = "+str(size))
    return size

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--infile', type=str)
    parser.add_argument('-n','--num_records', type=int, default=10)
    parser.add_argument('-r','--reservoir', default=False, action='store_true')
    parser.add_argument('-s','--seek', default=False, action='store_true')
    args = parser.parse_args()

    if (args.seek == args.reservoir):
        args.seek = False
        args.reservoir = False
        print('#Using reservoir sampling')

    inf = None
    if args.infile is None:
        inf = sys.stdin
        args.seek = False
        args.reservoir = True
    else:
        if args.infile.endswith('.gz'):
            inf = gzip.open(args.infile,'rb')
        else:
            inf = open(args.infile,'r')

    if args.seek:
        size = getFileSize(args.infile)
        records = randomSeek(inf, size, args.num_records)
    else:
        records = reservoir(inf, args.num_records)

    for record in records:
        print(">"+record[0])
        print(record[1])
