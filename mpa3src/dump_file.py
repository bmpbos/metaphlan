#!/usr/bin/env python
#Author: Duy Tin Truong (duytin.truong@unitn.it)
#        at CIBIO, University of Trento, Italy


import sys
import argparse as ap
import bz2
import gzip
import tarfile
#import logging.config
#sys.path.append('../pyphlan')
#sys.path.append('pyphlan')
import ooSubprocess

#logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
#logger = logging.getLogger(__name__)


def read_params():
    p = ap.ArgumentParser()
    p.add_argument('--input_file', required=True, default=None, type=str)

    return vars(p.parse_args())


def dump_file(ifn):
    file_ext = ''
    if ifn[-8:] == '.tar.bz2':
        ifile = tarfile.open(ifn, 'r:bz2')
        file_ext = '.tar.bz2'
    elif ifn[-7:] == '.tar.gz':
        ifile = tarfile.open(ifn, 'r:gz')
        file_ext = '.tar.gz'
    elif ifn[-4:] == '.bz2':
        ifile = bz2.BZ2File(ifn, 'r')
        file_ext = '.bz2'
    elif ifn[-3:] == '.gz':
        ifile = gzip.GzipFile(ifn, 'r')
        file_ext = '.gz'
    elif ifn[-6:] == '.fastq':
        ifile = open(ifn, 'r')
        file_ext = '.fastq'
    elif ifn[-4:] == '.sra':
        oosp = ooSubprocess.ooSubprocess()
        ifile = oosp.ex(
                        'fastq-dump',
                        args=[
                                '-Z', ifn,
                                '--split-spot'],
                        get_out_pipe=True)
        file_ext = '.sra'
    else:
        sys.stderr.write('Unrecognized format! The format should be .bz2, .gz'\
                '.tar.bz2, .tar.gz, .sra, or .fastq\n')
        exit(1)

    try:
        if file_ext in ['.tar.bz2', '.tar.gz']:
            for tar_info in ifile:
                ifile2 = ifile.extractfile(tar_info)
                if ifile2 != None:
                    for line in ifile2:
                        sys.stdout.write(line)
        else:
            for line in ifile:
                sys.stdout.write(line)
    except:
        sys.stderr.write('Error while dumping file %s\n'%ifn)
        raise


if __name__ == "__main__":
    args = read_params()
    dump_file(args['input_file'])
