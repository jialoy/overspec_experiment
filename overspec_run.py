#!/usr/bin/env python

import pygame, random, sys
from pygame.locals import *
import overspec_stimgen, overspec_exp

subjNo = sys.argv[1]

if __name__ == "__main__":
    
    overspec_stimgen.generate_stim_spreadsheet(subjNo)
    
    overspec_exp.build_experiment(subjNo)
    
    