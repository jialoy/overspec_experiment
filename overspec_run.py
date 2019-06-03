#!/usr/bin/env python

import pygame, random, sys
from pygame.locals import *
import overspec_stimgen_v2, overspec_exp

subjNo, gender = sys.argv[1], sys.argv[2]

if __name__ == "__main__":
    
    overspec_stimgen_v2.generate_stim_spreadsheet(subjNo)
    
    overspec_exp.build_experiment(subjNo, gender)
    
    