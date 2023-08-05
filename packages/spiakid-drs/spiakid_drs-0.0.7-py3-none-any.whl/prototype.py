import h5py
import sys
import numpy as np
import pandas as pd
from Functions import GUI as G
from Functions import Modelisation as mod
import os
import argparse
from pathlib import Path


def parse():
    # read in command line arguments
    parser = argparse.ArgumentParser(description='MKID Pipeline CLI')
    parser.add_argument('--init', action='store_true', help='launch the interface')
    parser.add_argument('--outp', help='output destination', dest='out_cfg', default=None)
    parser.add_argument('--inp', help='data location', dest='in_cfg' , default=None)
    parser.add_argument('--format', help='format of the plot', default='.jpg', dest='form')
    parser.add_argument('--dir', help='create input and output folder', action='store_true')
    parser.add_argument('--hello',action='store_true',help='Launch thre web interface')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse()
    if args.init:
        G.interface()
        print('Done')
        sys.exit(0)

    if args.hello:
        os.system("streamlit run hello.py")
    
    if args.out_cfg!=None and args.in_cfg!=None:
        mod.Data_read(args.in_cfg,args.out_cfg,args.form)
        print('Done')

    if args.dir:
        output = Path('Output')
        Input = Path('Data_location')
        if output.exists():
            pass
        else:
            output.mkdir()
        if Input.exists():
            pass
        else:
            Input.mkdir()
