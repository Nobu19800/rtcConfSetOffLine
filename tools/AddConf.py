#!/bin/env python
# -*- encoding: utf-8 -*-

##
#   @file AddConf.py
#   @brief コンフィギュレーションパラメータ設定ファイル作成
# -c RTCのパス
# -f 設定ファイル(rtc.conf)名
# コンフィギュレーションパラメータ設定ファイルはRTC名.confで保存

import optparse
import rtctree.tree
import sys
import os




##
# @brief RTCコンフィギュレーションパラメータ設定ファイルを生成する
# @param path RTCのパス
# @param dname 保存ディレクトリ
# @return カテゴリ名、RTC名
def saveRTCConf(path,dname="."):
    
        
    
    tree = rtctree.tree.RTCTree(servers=path[0])
    d = ["/"]
    for p in path:
        if p != "":
            d.append(p)

    
    c = tree.get_node(d)
    if c == None:
        print u"RTCが見つかりませんでした"
        return "",""

    filename = c.object.get_sdo_id() + ".conf"
    f = open(filename, "w")

    

    s = "configuration.active_config: "
    s += str(c.active_conf_set_name)
    s += "\n"

    f.write(s)

    confList = c.conf_sets
    for k, v in confList.items():
        #print k
        for i,j in v.data.items():
            s = "conf."
            s += str(k)
            s += "."
            s += str(i)
            s += ": "
            s += str(j)
            s += "\n"
            f.write(s)

    
    ec = c.owned_ecs[0]
    s = "exec_cxt.periodic.rate: "
    s += str(ec.rate)
    s += "\n"

    f.write(s)
    

    f.close()
    
    
    return c.category, c.object.get_sdo_id()


##
# @brief メイン関数
def main():
  usage = ''' '''
  version = 1.0
  parser = optparse.OptionParser(usage=usage, version=version)

  parser.add_option('-c', '--comp', dest='comp', action='store',
            type='string', default="",
            help='Component Path')
  parser.add_option('-f', '--file', dest='filepath', action='store',
            type='string', default="",
            help='File Path')

  try:
        options, args = parser.parse_args()
  except optparse.OptionError as e:
        return 1
  
  cpath = options.comp.split("/")
  file_name = options.filepath
  
  #print cpath,file_name
  
  
  if len(cpath) < 2:
    print u"RTCのパスを入力してください"
    return

  if file_name == "":
    saveRTCConf(cpath)
    return
  
  

  
  

  fname = os.path.basename(file_name)
  name, ext = os.path.splitext(fname)
  dname = os.path.dirname(os.path.relpath(file_name))


  f = open(file_name, "a")
  
  
  category,id = saveRTCConf(cpath,dname)
  
  
  s = category + "." + id + ".config_file: " + id + ".conf\n"
  f.write(s)
  

  f.close()
  

  return

if __name__ == "__main__":
  main()
