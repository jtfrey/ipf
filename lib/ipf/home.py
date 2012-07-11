
###############################################################################
#   Copyright 2012 The University of Texas at Austin                          #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
###############################################################################

import os
import sys

#######################################################################################################################

#### for with distutils ####

# use the environment variable if set (during development)
#IPF_HOME = os.environ.get("IPF_HOME")

# use the location of the Python install otherwise (e.g. installed into a virtualenv)
#if IPF_HOME == None:
#    IPF_HOME = sys.prefix

#### for with custom install.py ####

path = os.path.abspath(__file__)
path = os.path.split(path)[0]
path = os.path.split(path)[0]
path = os.path.split(path)[0]
IPF_HOME = path
