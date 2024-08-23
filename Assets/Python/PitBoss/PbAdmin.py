## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
# Pitboss admin framework
# Dan McGarry 3-24-05
#

# This file is only a stub in this Mod. The main content
# can be found in 'PBs/Python'

from CvPythonExtensions import *
import sys
import os
import string
gc = CyGlobalContext()

# Extra path for extra python modules
try:
    pythonDir = os.path.join(gc.getAltrootDir(),'..','Python','v10')
    execfile( os.path.join(pythonDir,'PbAdmin.py'))
except:
    execfile( os.path.join('D:','Sid Meiers Civilization 4 Complete','PB Tools','pbmod-master','PBs', 'Python','v10','PbAdmin.py'))
