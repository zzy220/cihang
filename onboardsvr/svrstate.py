'''
Created on Nov 25, 2017

@author: zhenyu

This module is used to collect system state of the onboard server
'''
import psutil

def get_onboardsvr_state():
    '''
    return some system states, as an property array:
    [
     { "name": "cpuUsage", "status":10 },
     { "name": "memUsage",  "status":20 },
     { "name": "diskUsage",  "status":20 },
     { "name": "disk2Usage",  "status":20 }
    ]    
    '''
    
    state = []
    # print partition states
    #s = psutil.disk_partitions()
    #print(s)
    # cpu usage
    cpusta = psutil.cpu_times_percent()
    state.append( { "name": "cpuUsage", "status": int(100 - cpusta.idle) } ) # total cpu usage

    # memory usage
    memsta = psutil.virtual_memory()
    state.append( { "name": "memUsage", "status": int(memsta.percent)} ) # this is just the mem usage

    # disk usage
    disksta = psutil.disk_usage('/')
    state.append( { "name": "diskUsage", "status": int(disksta.percent)} ) # this is just the disk usage
    
    # disk2 usage
    # to do: need to know the mountpoint of disk2
    # s = psutil.disk_usage('/') 
    state.append( { "name": "disk2Usage", "status": 0} ) # this is just the mem usage
    
    # return the list
    return state

# some UT code
if __name__=="__main__":
    print(get_onboardsvr_state())

    