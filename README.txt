一、程序使用说明 
1. 本程序需要python3 解释器运行
2. 运行前需安装以下python 软件包
	sudo apt-get install python3-pip
	sudo python3 -m pip install pycryptodome
	sudo python3 -m pip install psutil
3. 将软件包(cihang目录)拷贝到安装目录, 比如home目录 
4. 执行 run.sh 命令即可
5. 输入 q 结束程序运行
6. 输入 h 可查看帮助

二、程序工作目录 
主程序的唯一参数是工作目录，其他参数从工作目录下的配置文件读取。
run.sh 脚本自动设置当前目录下的workdir为工作目录，
也可以修改脚本 run.sh 指定工作目录。
运行时产生的文件会放到工作目录下。

三、配置文件
程序从工作目录的以下文件配置文件
1. 车载设备信息文件  devlist.json
文件的格式为：
{
    "rfidList": [ { "name": "rfid1", "ip": "ip_addr1"  },  { "name": "rfid2", "ip": "ip_addr2"  }  ],
    "camList": [  { "name": "cam1", "ip": "ip_addr1"  },  { "name": "cam2", "ip": "ip_addr2"  }  ],
    "apList": [   { "name": "ap1", "ip": "ip_addr1"  },  { "name": "ap2", "ip": "ip_addr2"  }  ],
    "brList": [   { "name": "br1", "ip": "ip_addr1"  },  { "name": "br2", "ip": "ip_addr2"  }  ]
}

2. 程序配置 config.json
文件的格式为：
{
	"patch_root":"/",           # 补丁文件安装的根目录
	"report_interval": 30,      # 设备信息的上报周期
	"patch_interval":  60       # 下载安装补丁的周期
}

"patch_root":        # 补丁文件安装的根目录
"report_interval":   # 设备信息的上报周期
"patch_interval":    # 下载安装补丁的周期

四、日志文件

程序运行中的异常信息会写入工作目录下的 cihang.log 文件中

五、其他说明

1. 集成开发环境
程序目录下包含有Eclipse 工程文件。
安装Eclipse + PyDev工具包即可打开进行开发调试
也可以配置 python IDLE 集成开发工具进行开发调试

2. ubuntu 开启root 账号
如果需要以root 方式运行，可以开启root 账号：
sudo passwd root
# enter new password for root
sudo -i # switch to root account
