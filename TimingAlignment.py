#!/usr/bin/env python

"""
Study timing between pixel and pad detectors.

Also produce tracking based analysis plots.
"""

###############################
# Imports
###############################

import os
import sys
import array
import math
import argparse

import ROOT

import TimingAlignmentHelpers as TAH


###############################
# Configuration
###############################

parser = argparse.ArgumentParser(description='Timing Alignment of DRS4-Board with CMS - PixelTestboard.',
                                  epilog="Example  python {0} 70 0".format(sys.argv[0]))

parser.add_argument('run',metavar='R', type=int,help='run: run number (int)')
parser.add_argument('action',metavar='A', type=int,help='action: 0=analyze    1=run on small sample     2=find alignment    3=do everything')
parser.add_argument('-diamond',type=str,help='only needed for action=3')
parser.add_argument('-voltage',type=int,help='only needed for action=3')
args = parser.parse_args()

run = args.run
action = args.action
if action ==3:
  diamond = args.diamond
  bias_voltage = args.voltage

print 'Run',args.run
print 'action',args.action
print 'diamond',args.diamond
print 'voltag',args.voltage


###############################
# Init ROOT
###############################
ROOT.gStyle.SetPalette(53)

ROOT.gStyle.SetPadLeftMargin(0.15)
ROOT.gStyle.SetPadRightMargin(0.14)
ROOT.gStyle.SetPadBottomMargin(0.12)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gROOT.ForceStyle()
c = ROOT.TCanvas("","",800,800)

print "Going to process run {0} with action = {1}".format(run, action)


###############################
# Diamonds
###############################

TAH.Diamond("dummy", -1., 1., -1., 1.)
TAH.Diamond("IIa-2", -0.2, 0.2, 0., 0.4)
TAH.Diamond("IIa-3", -0.25, 0.15, -0.05, 0.35)
TAH.Diamond("IIa-3-wide-open", -0.5, 0.5, -0.25, 0.65)
TAH.Diamond("IIa-5-pedestal", -0.4, 0.4, 0.4, 0.6)
TAH.Diamond("2A87-E", -0.2, 0.1, -.05, 0.3)


###############################
# Run Timing Info
###############################

TAH.RunTiming(6  ,  0.0003045,  2.155918e-06, 0, 0)
TAH.RunTiming(12 , -0.00030472, 1.955999e-06, 0, 0)
TAH.RunTiming(38 ,  0.00052454, 1.9e-06,      4, 0)
TAH.RunTiming(63 , -0.00030911, 1.837389e-06, 0, 0)
TAH.RunTiming(65 ,  0.00034346, 1.864050e-06, 0, 0)
TAH.RunTiming(68 , -0.00085284, 2.026819e-06, 6, 0)
TAH.RunTiming(70 , -0.00028498, 1.910828e-06, 6, 0)
TAH.RunTiming(109, 0.000323963498273, 1.81841520034e-06, 15, 1)
TAH.RunTiming(131, -0.000191132147971, 1.93697727798e-06, 13, 2)
TAH.RunTiming(134, -3.1728796239e-05, 1.64755689822e-06, 14, 0)

# IIa-2, positive voltage
TAH.RunTiming(354, 0, 1.66190809094e-06, 7, 0, "IIa-2")
TAH.RunTiming(355, -0.000314315985828, 1.66190809094e-06, 2, 1, "IIa-2", 500)
TAH.RunTiming(356, -0.000695592438193, 1.61339888272e-06, 7, 0, "IIa-2", 500)
TAH.RunTiming(358, 0.000249032875294, 1.61704852897e-06, 12, 1, "IIa-2", 500)
TAH.RunTiming(360, -0.000185791051023, 1.59938328397e-06, 5, 1, "IIa-2", 500)
TAH.RunTiming(362, 0.00042190730171, 1.64763938056e-06, 1, 1, "IIa-2", 500)

# IIa-3, positive voltage
TAH.RunTiming(457, 1.81812073529e-05, 1.57043424908e-06, 0, 0, "IIa-3", 1000)
TAH.RunTiming(463, 0.000150546696306, 1.66309765368e-06, 1, 1, "IIa-3", 500)
#RunTiming(467, -0.000353750981164, 1.60187924305e-06, 10, 1, "IIa-3", 500)

# IIa-3, negative voltage
TAH.RunTiming(528, -0.000415933095508, 1.60475855132e-06, 6, 1, "IIa-3", -25)
TAH.RunTiming(532, -5.38246743255e-05, 1.97836071279e-06, 14, 1, "IIa-3", -50)
TAH.RunTiming(534, -0.00016191126604, 1.64201756052e-06, 0, 0, "IIa-3", -75)
TAH.RunTiming(546, 1.52929003315e-05, 1.69038314973e-06, 0, 0, "IIa-3", -500)
TAH.RunTiming(558, 0.000554312131921, 1.75928791575e-06, 0, 0, "IIa-3", -500)
TAH.RunTiming(565, 0.000486774113148, 1.69386102118e-06, 13, 1, "IIa-3-wide-open", -1000)
TAH.RunTiming(566, -9.5862348191e-05, 1.64943513686e-06, 16, 1, "IIa-3", -1000)
TAH.RunTiming(568, 0.000443434862615, 1.57788860683e-06, 11, 1, "IIa-3-wide-open", -1000)
TAH.RunTiming(630, 0.00028963428651, 1.70790800374e-06, 0, 0, "IIa-5-pedestal", 500)


#2A87-E
#TAH.RunTiming(835, -0.000389567120076, 1.82800169927e-06, 12, 1, "2A87-E", -500)
TAH.RunTiming(835, -0.000407923105343, 1.78550487335e-06, 12, 1, "2A87-E", -500)




###############################
# Branch names
###############################

branch_names = {
    # Event Numbers
    "n_pad"   : "n",
    "n_pixel" :"ievent",
    # Time
    "t_pad"   : "time_stamp",  # [seconds]
    "t_pixel" :"time",  # clock-ticks (25 ns spacing)
    # Pixel only:
    # - Hit plane bits 
    "plane_bits_pixel": "hit_plane_bits",
    # -Tracks
    "track_x" : "track_x",
    "track_y" : "track_y",
    
    # Pad only:
    # - Calibration flag
    "calib_flag_pad" : "calibflag",
    # - Integral50
    "integral_50_pad" : "Integral50"
}


###############################
# Prepare Output Directory
###############################

try:
    os.mkdir("run_{0}".format(run))
except:
    pass


###############################
# Get Trees
###############################

basedir_pad = "../../padreadout-devel/data/output/"
basedir_pixel = "../plots/"

format_pad = "{0}run_2014_09r{1:06d}.root"
format_pixel = "{0}{1:06d}/histos.root"

filename_pad = format_pad.format(basedir_pad, run)
filename_pixel = format_pixel.format(basedir_pixel, run)

f_pad = ROOT.TFile.Open(filename_pad)
f_pixel = ROOT.TFile.Open(filename_pixel)

tree_pad = f_pad.Get("rec")
tree_pixel = f_pixel.Get("time_tree")

print "Read:"
print "PAD Tree: ", tree_pad.GetEntries(), "entries"
print "Pixel Tree: ", tree_pixel.GetEntries(), "entries"


###############################
# Actual work
###############################

if (action == 0) or (action == 1):
    TAH.print_run_info(run, tree_pixel, tree_pad, branch_names)
    TAH.analyze(run, 
                action,
                tree_pixel, 
                tree_pad, 
                branch_names, 
                c)

elif action == 2:
    TAH.print_run_info(run, tree_pixel, tree_pad, branch_names)
    TAH.find_alignment(run, 
                       tree_pixel, 
                       tree_pad, 
                       branch_names, 
                       c)

elif action == 3:

    TAH.RunTiming(run, diamond_name = diamond, bias_voltage = bias_voltage)

    TAH.find_alignment(run, 
                       tree_pixel, 
                       tree_pad, 
                       branch_names, 
                       c)

    TAH.analyze(run, 
                1,
                tree_pixel, 
                tree_pad, 
                branch_names, 
                c)

    TAH.analyze(run, 
                0,
                tree_pixel, 
                tree_pad, 
                branch_names, 
                c)

