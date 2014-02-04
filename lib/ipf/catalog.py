
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

import logging
import os
import traceback

from ipf.data import Data,Representation
from ipf.home import IPF_HOME
from ipf.step import Step

#######################################################################################################################

logging.config.fileConfig(os.path.join(IPF_HOME,"etc","logging.conf"))
logger = logging.getLogger(__name__)

#######################################################################################################################

class Catalog(object):
    def __init__(self):
        # step class name -> Step for when reading workflows
        self.steps = {}

        self.data = {}             # class name -> [Data,]
        self.representations = {}  # class name -> [Representation,]

        # Data/Representation -> [Step]
        self.producers = {}

        # Data -> [Representations]
        self.reps_for_data = {}

        # use sys.path somehow?
        path = os.path.join(IPF_HOME,"lib")
        mod_path = ""
        modules = self._readModules(path, mod_path)
        #modules = self._readPackages(path, mod_path)

        for module in modules:
            logger.debug("loading %s",module)
            try:
                __import__(module)
            except:
                logger.debug(traceback.format_exc())
                pass  # ignore modules that can't be loaded

        self._addSubclasses(Step,self.steps)
        self._addSubclasses(Data,self.data)
        self._addSubclasses(Representation,self.representations)

        for rep in self.representations.values():
            if rep.data_cls not in self.reps_for_data:
                self.reps_for_data[rep.data_cls] = []
            self.reps_for_data[rep.data_cls].append(rep)
        for step_class in self.steps.values():
            step = step_class()
            for data in step.produces:
                # add Data to producers
                if not data in self.producers:
                    self.producers[data] = []
                self.producers[data].append(step_class)
                # add Representations of this Data to producers
                try:
                    for rep in self.reps_for_data[data]:
                        if not rep in self.producers:
                            self.producers[rep] = []
                        self.producers[rep].append(step_class)
                except KeyError:
                    pass

        #print("data:")
        #for key in self.data:
        #    print(key+": "+str(self.data[key]))

        #print("representations:")
        #for key in self.representations:
        #    print(key+": "+str(self.representations[key]))

        #print("producers:")
        #for key in self.producers:
        #    print(str(key)+": "+str(self.producers[key]))

    def _readModules(self, path, mod_path):
        modules = []
        for file in os.listdir(path):
            if os.path.isdir(os.path.join(path,file)):
                if mod_path == "":
                    new_mod_path = file
                else:
                    new_mod_path = mod_path+"."+file
                mods = self._readModules(os.path.join(path,file),new_mod_path)
                modules.extend(mods)
            elif os.path.isfile(os.path.join(path,file)):
                if file.endswith(".py") and file != "__init__.py":
                    mod,ext = os.path.splitext(file)
                    if mod_path == "":
                        modules.append(mod)
                    else:
                        modules.append(mod_path+"."+mod)
        return modules

    def _readPackages(self, path, mod_path):
        packages = []
        for file in os.listdir(path):
            if not os.path.isdir(os.path.join(path,file)):
                continue
            if mod_path == "":
                new_mod_path = file
            else:
                new_mod_path = mod_path+"."+file
            packages.append(new_mod_path)
            packs = self._readPackages(os.path.join(path,file),new_mod_path)
            packages.extend(packs)
        return packages

    def _addSubclasses(self, cls, dict):
        stack = cls.__subclasses__()
        while len(stack) > 0:
            cls = stack.pop(0)
            cls_name = cls.__module__+"."+cls.__name__
            if cls_name in dict:
                logger.warn("multiple classes with name %s - ignoring all but first",cls_name)
            else:
                dict[cls_name] = cls
            stack.extend(cls.__subclasses__())

catalog = Catalog()
