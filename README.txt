[ 程序使用说明 ]
1. 本程序需要python3 解释器运行
2. 运行前需安装以下python 软件包
	sudo apt-get install python3-pip
	sudo python3 -m pip install pycryptodome
	sudo python3 -m pip install psutil
3. 将软件包拷贝到安装目录 比如 ~
4. 执行 run.sh 命令即可

5. 按 Ctrl+C 结束程序运行

[ 程序工作目录 ]
run.sh 脚本读取当前目录为工作目录，
也可以修改脚本指定工作目录。
运行是产生的文件会放到工作目录下。

[配置文件]
程序从工作目录的一下文件中读取车载设备信息：
	devlist.json
文件的格式为：
    {
        "rfidList": [ { "name": "rfid1", "ip": "ip_addr1"  },  { "name": "rfid2", "ip": "ip_addr2"  }  ],
        "camList": [  { "name": "cam1", "ip": "ip_addr1"  },  { "name": "cam2", "ip": "ip_addr2"  }  ],
        "apList": [   { "name": "ap1", "ip": "ip_addr1"  },  { "name": "ap2", "ip": "ip_addr2"  }  ],
        "brList": [   { "name": "br1", "ip": "ip_addr1"  },  { "name": "br2", "ip": "ip_addr2"  }  ]
    }
