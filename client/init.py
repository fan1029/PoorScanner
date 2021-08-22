import argparse
import sys
from  Message import Msg
import configparser
import os




class Args():


        parser = argparse.ArgumentParser()
        parser.add_argument("-u", help="输入扫描的目标 e.g http://www.baidu.com/", type=str)
        parser.add_argument("-d", help="输入要使用的自定义字典路径", type=str, default="Default.txt")
        parser.add_argument("-s",  help="扫描速度 ", type=str,  default='30')
        parser.add_argument("-m",  help="请求方式 head(这个快点) get  默认为get", type=str,  default="get")
        parser.add_argument("-t",  help="模式默认为普通模式扫描 传参为hidden为隐蔽扫描", type=str,  default="normal")
        parser.add_argument("-cut_times", help="隐蔽扫描模式下使用，讲字典切割的片段数，默认为 10个", type=int, default=10)
        parser.add_argument("-wait_time", help="每个片段扫描完成后延时的时间默，认为60S", type=int, default=60)
        parser.add_argument("--getid", help="获取requestID的报告", type=str)
        args=parser.parse_args()

        @classmethod
        def get_args(cls):
                if (cls.args.u==None):
                    Msg.error("语法错误，请输入-h获取帮助")
                    sys.exit()
                elif("http" not in cls.args.u):
                    Msg.warn("请在url前面加上http")
                    sys.exit()
                if cls.args.t=="normal":
                        Msg.show("URL："+cls.args.u+"     Dir:"+cls.args.d+"     Speed:"+cls.args.s+"     Method:"+cls.args.m+"     Type:"+cls.args.t)
                elif cls.args.t=="hidden":
                        Msg.show("URL：" + cls.args.u + "     Dir:" + cls.args.d + "     Speed:" + cls.args.s + "     Method:" + cls.args.m + "     Type:" + cls.args.t+"     cut_times:"+ cls.args.cut_times+"     wait_time:"+cls.args.wait_time)
                else:
                        Msg.warn("你选的是啥子模式??")
                        sys.exit()
                return cls.args.u,cls.args.d,cls.args.s,cls.args.m,cls.args.t,cls.args.cut_times,cls.args.wait_time

class init_config():

    @staticmethod
    def check_None(*args):
        for value in args:
            if value=="":
                Msg.warn("配置文件读取错误，请检查配置文件是否全部填写！")
                sys.exit()

    @classmethod
    def readserver(cls):
        reader=configparser.ConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'config.ini')
        if not os.path.exists(file_path):
            sys.exit()
        reader.read(file_path)
        id=reader.get('Server','id')
        key=reader.get('Server','key')
        function_name=reader.get('Server','function_name')
        region=reader.get('Server','reigon')
        cls.check_None(id,key,function_name,region)
        return {'id': id, 'key': key , 'function_name': function_name , 'region':region}

    @classmethod
    def readgitee(cls):
        reader = configparser.ConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'config.ini')
        reader.read(file_path)
        owner=reader.get("Gitee","owner")
        repo=reader.get("Gitee","repo")
        brach=reader.get("Gitee","brach")
        cls.check_None(owner,repo,brach)
        return {'owner': owner, 'repo': repo , 'barch': brach}
        pass

    @classmethod
    def readdir(cls):
        reader = configparser.ConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'config.ini')
        reader.read(file_path)
        cut_size=reader.get("Dir","cut_size")
        cycle_time=reader.get("Dir","cycle_time")
        cls.check_None(cut_size,cycle_time)
        return {"cut_size":cut_size,"cycle_time":cycle_time}


class Banner():

    @staticmethod
    def showbanner():
        banner = '''
  _____                     _____                                       
 |  __ \                   / ____|                                      
 | |__) |___    ___   _ __| (___    ___  __ _  _ __   _ __    ___  _ __ 
 |  ___// _ \  / _ \ | '__|\___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
 | |   | (_) || (_) || |   ____) || (__| (_| || | | || | | ||  __/| |   
 |_|    \___/  \___/ |_|  |_____/  \___|\__,_||_| |_||_| |_| \___||_|   

        '''
        header = '''
- PoorScanner v1.0 Beta    ->   贫穷扫描器 一款不需要买代理来减少扫目录被封概率的工具
- By M4PL3
---------------------------------------------------------------------------------------------------
        '''
        print(banner)
        print(header)