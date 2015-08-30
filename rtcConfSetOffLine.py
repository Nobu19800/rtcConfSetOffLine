#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file rtcConfSetOffLine.py
#   @brief rtc.conf作成ツール



import thread


import optparse
import sys,os,platform
import re
import time
import random
import commands
import math
import imp



import rtctree.tree

import RTC
import OpenRTM_aist

from OpenRTM_aist import CorbaNaming
from OpenRTM_aist import RTObject
from OpenRTM_aist import CorbaConsumer
from omniORB import CORBA
import CosNaming

from PyQt4 import QtCore, QtGui

import SettingRTCOffLine_Lib.MainWindow






        
##
# @brief メイン関数
def main():
    #mgrc = ManagerControl("")
    
    
    app = QtGui.QApplication([""])
    mainWin = SettingRTCOffLine_Lib.MainWindow.MainWindow()
    mainWin.show()
    app.exec_()
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    #mgrc.createComp("MyFirstComponent",[".\\MyFirstComponent"])
    
    
    
    
    

    
    
    
if __name__ == "__main__":
    main()
