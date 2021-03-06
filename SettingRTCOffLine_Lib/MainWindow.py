#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file MainWindow.py
#   @brief メインウインドウ



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



from SettingRTCConf.ConfigWidget import ConfigWidget
from SettingRTCConf.CorbaWidget import CorbaWidget
from SettingRTCConf.ExecCxtWidget import ExecCxtWidget
from SettingRTCConf.LoggerWidget import LoggerWidget

from SettingRTCConf.ManagerWidget import ManagerWidget
from SettingRTCConf.NamingWidget import NamingWidget
from SettingRTCConf.TimerWidget import TimerWidget


from SettingRTCOffLine_Lib.ManagerControl import ManagerControl


##
# @class MainWindow
# @brief メインウインドウ
#
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        

        self.tab_widget = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.createAction()
        self.createMenus()

        #self.mgrc = ManagerControl("")
        self.mgrc = None
        self.curFile = ""

	

        #self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])
        #self.mgrc.CreateComp("MyFirstComponent",[".\\MyFirstComponent"])
        
    ##
    # @brief アクションの作成の関数
    # @param self
    def createAction(self):

        self.newAct = QtGui.QAction("&New...",self)
        self.newAct.setShortcuts(QtGui.QKeySequence.New)
        self.newAct.triggered.connect(self.newFile)
        


        self.openAct = QtGui.QAction("&Open...",self)
        self.openAct.setShortcuts(QtGui.QKeySequence.Open)
        self.openAct.triggered.connect(self.open)


        self.saveAct = QtGui.QAction("&Save",self)
        self.saveAct.setShortcuts(QtGui.QKeySequence.Save)
        self.saveAct.triggered.connect(self.save)

        self.saveAsAct = QtGui.QAction("&Save &As",self)
        self.saveAsAct.setShortcuts(QtGui.QKeySequence.SaveAs)
        self.saveAsAct.triggered.connect(self.saveAs)

    ##
    # @brief メニューの作成の関数
    # @param self
    def createMenus(self):

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)


    ##
    # @brief タブの作成の関数
    # @param self
    def createTabs(self):
        self.Tabs = []
        self.ManagerTab = ManagerWidget(self.mgrc)
        self.tab_widget.addTab(self.ManagerTab, u"マネージャ")
        self.Tabs.append(self.ManagerTab)
        self.CorbaTab = CorbaWidget(self.mgrc)
        self.tab_widget.addTab(self.CorbaTab, u"CORBA")
        self.Tabs.append(self.CorbaTab)
        self.ConfigTab = ConfigWidget(self.mgrc)
        self.tab_widget.addTab(self.ConfigTab, u"一般的")
        self.Tabs.append(self.ConfigTab)
        self.NamingTab = NamingWidget(self.mgrc)
        self.tab_widget.addTab(self.NamingTab, u"ネームサービス")
        self.Tabs.append(self.NamingTab)
        self.LoggerTab = LoggerWidget(self.mgrc)
        self.tab_widget.addTab(self.LoggerTab, u"ロガー")
        self.Tabs.append(self.LoggerTab)
        self.TimerTab = TimerWidget(self.mgrc)
        self.tab_widget.addTab(self.TimerTab, u"タイマ")
        self.Tabs.append(self.TimerTab)
        self.ExecCxtTab = ExecCxtWidget(self.mgrc, self.ManagerTab)
        self.tab_widget.addTab(self.ExecCxtTab, u"実行コンテキスト")
        self.Tabs.append(self.ExecCxtTab)


    ##
    # @brief ファイル読み込みスロット
    # @param self
    def open(self):
        if self.mgrc == None:
            fileName = QtGui.QFileDialog.getOpenFileName(self,u"開く","","Config File (*.conf);;All Files (*)")
            if fileName.isEmpty():
                return
            ba = str(fileName.toLocal8Bit())
            #ba = ba.replace("/","\\")
            self.mgrc = ManagerControl(ba)
            self.createTabs()

            
            self.curFile = ba
            
        else:
            self.mesBox(u"既にコンフィギュレーションファイルは開いています")

    ##
    # @brief ファイル保存のスロット
    # @param self
    # @return 成功でTrue、失敗でFalse
    def save(self):
        if self.curFile == "":
            return self.saveAs()
        else:
            self.saveFile(self.curFile)
            return True

    ##
    # @brief ファイル保存の関数
    # @param self
    # @param filename ファイル名
    def saveFile(self, filename):
        f = open(filename, "w")

        for t in self.Tabs:
            for k,j in t.WidList.items():
                s = k + ": "
                v = ""
                if j["Type"] == ManagerControl.TextBox:
                    v += str(j["Widget"].text().toLocal8Bit())
                elif j["Type"] == ManagerControl.TextCombox or j["Type"] == ManagerControl.Combox:
                    
                    
                    if k == "manager.modules.load_path" or k == "manager.modules.preload" or k == "manager.components.precreate" or k == "corba.endpoints":
                        for c in range(0, j["Widget"].count()):
                            v += str(j["Widget"].itemText(c).toLocal8Bit()).replace("\\","/")
                            if c < j["Widget"].count()-1:
                                v += ","
                    else:
                        v += str(j["Widget"].currentText().toLocal8Bit())
                elif j["Type"] == ManagerControl.SpinBox or j["Type"] == ManagerControl.DoubleSpinBox:
                    v += str(j["Widget"].value())
                if v != "":
                    s += v + "\n"
                    f.write(s)
        f.close()
    ##
    # @brief ファイル別名で保存するときのスロット(未実装)
    # @param self 
    def saveAs(self):

        fileName = QtGui.QFileDialog.getSaveFileName(self,u"保存", "","Config File (*.conf);;All Files (*)")
        if fileName.isEmpty():
            return False

        ba = str(fileName.toLocal8Bit())

        self.saveFile(ba)

	

	

    ##
    # @brief 初期化のスロット
    # @param self 
    def newFile(self):
        if self.mgrc == None:
            self.mgrc = ManagerControl("")
            self.createTabs()

            
            """for c in self.mgrc.mgr.getComponents():
                print c.get_sdo_id()
                for l in c.get_configuration().get_configuration_sets():
                    print l.id
                    print l.description
                    #prop = OpenRTM_aist.SDOPackage.NVList
                    #OpenRTM_aist.toProperties(prop,l.configuration_data)
                    #print prop
                    for d in l.configuration_data:
                        print d.name
                        print d.value.value()"""
                
        else:
            self.mesBox(u"既にコンフィギュレーションファイルは開いています")


        
    ##
    # @brief メッセージボックス表示
    # @param self 
    # @param mes 表示する文字列
    def mesBox(self, mes):
        msgbox = QtGui.QMessageBox( self )
        msgbox.setText( mes )
        msgbox.setModal( True )
        ret = msgbox.exec_()
