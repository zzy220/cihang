'''
Created on Nov 25, 2017

@author: zhenyu
'''
import psutil

def get_onboardsvr_state():
    '''
    return some system states
    '''
    # 其中stat0-stat3分别表示: CPU占用率,内存占用率,主磁盘占用率,辅磁盘占用率
    state = {}
    # print partition states
    s = psutil.disk_partitions(True)
    print(s)
    # cpu usage
    s = psutil.cpu_times_percent()
    state["stat0"] = 100 - s.idle; # total cpu usage
    print(s)
    # memory usage
    s = psutil.virtual_memory()
    state["stat1"] = s.percent # this is just the usage
    print(s)
    # disk usage
    s = psutil.disk_usage('/')
    state["stat2"] = s.percent # this is just the usage
    print(s)
    state["stat3"] = 0;
    return state

# some UT code
if __name__=="__main__":
    print(get_onboardsvr_state())

    