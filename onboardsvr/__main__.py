'''
Created on Nov 18, 2017

@author: zhenyu

This is the entry of the program

设置工作目录，启动调度器，等待用户输入......

'''

import logging
import json
import sys, os
import platform
from onboardsvr import scheduler

def main():
    #default to '~/cihang/workdir'
    workdir = ''
    subdir = os.path.join('cihang', 'workdir')
    if platform.system().lower()=="windows":
        workdir = os.path.join( os.environ['USERPROFILE'], subdir)
    elif 'HOME' in os.environ:
        workdir = os.path.join( os.environ['HOME'], subdir)
        
    # get working directory from command line
    if len (sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            workdir = sys.argv[1]
        else:
            logging.error("main: wrong workdir:" + sys.argv[1])
            return
    
    # setup logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logfile = os.path.join(workdir, 'cihang.log')
    if os.path.exists(logfile)==False:
        try:
            os.system('touch '+logfile)
        except Exception as e:
            logging.error('failed prepare log file:'+ str(e))
            
    if os.path.exists(logfile):
        # uncomment to log to the file
        #logging.basicConfig(filename=logfile, level=logging.DEBUG)
        pass
 
    # 读取配置文件   
    config_file = os.path.join(workdir, 'config.json')
    config = {}
    config ["patch_root"] = workdir
    config ["report_interval"] = 30
    config ["patch_interval"] = 60    
    try:
        with open(config_file, 'rt') as histfile:
            config = json.load(histfile)
    except Exception as e:
        logging.error('failed to load config file:'+ str(e))
        
    logging.info('now kick off the scheduler.. ')
    
    # start the scheduler
    sched = scheduler.Scheduler(workdir, config ["patch_root"], config ["report_interval"], config ["patch_interval"])
    sched.startup()
    inchr = ''
    while True:
        print('enter h for help')
        inchr = input("enter q to quit")
        if inchr == 'q':
            break
        elif inchr == 'h':
            print('please read the README.txt for reference.')
            
    logging.info('now shuting down scheduler..')
    sched.shutdown()
    
    logging.info('good bye')
    pass

if __name__ == '__main__':
    main()
    