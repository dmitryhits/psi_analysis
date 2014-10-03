#!/usr/bin/env python

"""
Class RunInfo for 2014 September PSI Testbeam Analysis.
"""


###############################
# Imports
###############################

import json
import types as t

from Initializer import initializer
from MaskInfo import MaskInfo
from DataTypes import data_types

def signum(x):
    return (x > 0) - (x < 0)


MaskInfo.load("masks.json")

###############################
# MaskInfo
###############################

class RunInfo:

  # Dictionary with possible values for data_type field
#  data_types = {
#    0 : "DATA",
#    1 : "PEDESTAL",
#    2 : "VOLTAGESCAN",
#    3 : "OTHER"
#  }

  # Dictionary of all available runs
  #  -newly created objects register automatically
  #  -keys = run number
  runs= {}

  # initializer - a member variable is automatically created
  #  for each argument of the constructor
  @initializer
  def __init__(self,
               number,                  # [int]
               begin_date,              # [string] (example: 2014-09-25)
               begin_time,              # [int] (example: 2030)
               end_time,                # [int] (example: 2035)
               diamond,                 # [string] (example: "S30")
               data_type,               # [int] (key from data_types dictionary)
               bias_voltage,            # [int] (in Volts)
               mask_time,               # [int] (example: 2030)
               fsh13,                   # [int]
               fs11,                    # [int]
               rate_raw,                # [int] (Hz)
               rate_ps,                 # [int] (Hz, ps = prescaled)
               rate_trigger,            # [int] (Hz, used for triggering)
               events_nops,             # [int] (total events, nops = no prescale)
               events_ps,               # [int] (total events, ps = prescale)
               events_trig,             # [int] (total events, used for triggering)
               pedestal_run,            # [int] run from which to take pedestal information
                                        #         (set to -1 for pedestal runs or if no pedestal run is available)

               pedestal = float('nan'), # [float] for data runs: which pedestal value to subtract
               comment = "",            # [string] free text
               # Next four parameters can be measured using TimingAlignment.py
               align_ev_pixel = -1,     # [int] pixel event for time-align
               align_ev_pad = -1,       # [int] pad event for time align
               time_offset = 0.,        # float (seconds)
               time_drift = -1.9e-6):   # drift between pixel and pad clock

    # Validate
    assert (type(number) is t.IntType and 0 < number < 1000), "Invalid run number"
    assert (type(begin_date) is t.StringType or type(begin_date) is t.UnicodeType ), "Invalid begin_date"
    assert (type(begin_time) is t.IntType and (0 < begin_time and begin_time/100 < 24 and begin_time%100 < 60) or begin_time==-1), "Invalid begin_time"
    assert (type(end_time) is t.IntType and (0 < end_time and end_time/100 < 24 and end_time%100 < 60) or end_time==-1), "Invalid end_time"
    assert (type(diamond) is t.StringType or type(diamond) is t.UnicodeType), "Invalid diamond"
    assert (data_type in data_types.keys()), "Invalid data_type"
    assert (type(bias_voltage) is t.IntType and -2000 < bias_voltage < 2000)
    assert (type(mask_time) is t.IntType and 0 <= mask_time), "Invalid mask_time"
    assert (type(fsh13) is t.IntType and -200 <= fsh13 <= -1), "Invalid fsh13"
    assert (type(fs11) is t.IntType and 0 < fs11 <= 200), "Invalid fs11"
    assert (type(rate_raw) is t.IntType), "Invalid rate_raw"
    assert (type(rate_ps) is t.IntType), "Invalid rate_ps"
    assert (type(rate_trigger) is t.IntType), "Invalid rate_trigger"
    assert (type(events_nops) is t.IntType), "Invalid events_nops"
    assert (type(events_ps) is t.IntType), "Invalid events_ps"
    assert (type(events_trig) is t.IntType), "Invalid events_trig"
    assert (type(pedestal_run) is t.IntType), "Invalid pedestal_run"
    assert (type(pedestal) is t.FloatType), "Invalid pedestal"
    assert (type(comment) is t.StringType or type(comment) is t.UnicodeType), "Invalid comment"
    assert (type(align_ev_pixel) is t.IntType), "Invalid align_ev_pixel"
    assert (type(align_ev_pad) is t.IntType), "Invalid align_ev_pad"
    assert (type(time_offset) is t.FloatType), "Invalid time_offset"
    assert (type(time_drift) is t.FloatType), "Invalid time_drift"

    # Add to runs dictionary
    RunInfo.runs[self.number] = self

  # End of __init__
  @staticmethod
  def update_timing(run,align_ev_pixel,align_ev_pad, time_offset, time_drift):
      RunInfo.runs[run].align_ev_pixel = align_ev_pixel
      RunInfo.runs[run].align_ev_pad = align_ev_pad
      RunInfo.runs[run].time_offset = time_offset
      RunInfo.runs[run].time_drift = time_drift

  def get_mask(self):
      #diamond, bias_sign,MaskInfo.data_types[data_type],str(mask_time))
      key = MaskInfo.create_name(self.diamond, signum(self.bias_voltage), self.data_type,self.mask_time)
      if key in MaskInfo.masks:
        return MaskInfo.masks[key]
      else:
        raise Exception('cannot find key {key} in {keys}'.format(key=key,keys=MaskInfo.masks.keys()))


  # Dump all RunInfos (the content of the runs dictionary)
  #  to a file using json
  @classmethod
  def dump(cls, filename):
    print 'write new json file'
    f = open(filename, "w")
    f.write(json.dumps(cls.runs,
                       default=lambda o: o.__dict__,
                       sort_keys=True,
                       indent=4))
    f.close()
  # End of to_JSON

  # Read all RunInfos from a file and use to intialize objects
  @classmethod
  def load(cls, filename):

    # first get the dictionary from the file..
    f = open(filename, "r")
    data = json.load(f)
    f.close()

    # ..then intialize the individual RunInfo objects from it
    for k,v in data.iteritems():
      RunInfo(**v)

  # End of to_JSON

# End of class RunInfo
