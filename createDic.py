#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import getopt
import platform

from translate import Translator


def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print "Time: %f" % (time.time() - t)
        return res

    return tmp


def usage():
    print 'Help:'
    print ' -s <source>   -- text file for analizing'
    print ' -o <outfile>  -- text file for output'


def checkOS():
    os = platform.platform()
    if 'Linux' or 'linux' in os:
        return '/'
    elif 'Win' or 'win' in os:
        return '\\'


@timer
def main(argv=None):
    if argv is None:
        argv = sys.argv
    source = sys.path[0] + checkOS() + 'source.txt'
    outfile = sys.path[0] + checkOS() + 'dic.txt'
    filter = sys.path[0] + checkOS() + 'filter.txt'
    # Разбираем аргументы командной строки
    try:
        #opts, args = getopt.getopt( sys.argv[1:], "h", ["help"])
        opts, args = getopt.getopt(argv[1:], "hs:o:", ["help", "source=", "outfile="])
        # opts - опции и их значения [('-h', ''), ('-s', '<source>'), ...]
        # print opts, args
    except getopt.error, msg:
        print msg
        print "Use --help for more information"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        if o in ("-s", "--source"):
            source = a
            # sys.exit(0)
        if o in ("-o", "--outfile"):
            outfile = a
    # Анализируем
    # print args
    process(source, outfile, filter)
    # for arg in args:
    #    process(arg) # process() определен в другом месте


def normalize(source):
    bad = ['.', ',', '\n', ':', '(', ')', '`', "’", '‘']
    source = source.lower()
    for rep in bad:
        source = source.replace(rep, '')
    return source


def invert_dict(d):
    inv = dict()
    for key in d:
        val = d[key]
        if val not in inv:
            inv[val] = [key]
        else:
            inv[val].append(key)
    return inv


def process(source, outfile, _filter):
    if os.path.isfile(source):
        deny = []
        with open(_filter, 'r') as filter:
            for line in filter:
                deny.append(line.replace('\n', '').replace('\r', ''))
        tmp = []
        words = {}
        with open(source, 'r') as source:
            with open(outfile, 'w') as dic:
                for str in source:
                    tmp = normalize(str).split(' ')
                    for word in tmp:
                        if len(word) > 2:
                            if words.get(word):
                                words[word] += 1
                            else:
                                words[word] = 1
                # print words
                translator = Translator(to_lang="ru")
                for key, value in sorted(words.iteritems(), key=lambda (k, v): (v, k)):
                    if key not in deny:
                        dic.write(key + ' - ' + translator.translate(key).encode("utf8") + '\n')
                        # print "%s: %s" % (key, value)
    else:
        print 'Plese input correctly data for <source>!'


if __name__ == '__main__':
    sys.exit(main())
