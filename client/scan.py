from Remote_API import API
from Dir_oprater import Dict_oprater
import time
import json
from Message import Msg
import requests
from init import init_config
import base64
from  DataPrinter import Printer

class Scan():
    def __init__(self, url, dict, method, speed,type,cut_times,cycle_time):
        self.dir_connfig=init_config.readdir()
        self.cycle_time=int(self.dir_connfig['cycle_time'])
        self.url = url
        self.dict = dict
        self.method = method
        self.speed = speed
        self.payload_sender = API()
        self.__dir_get()
        if type=='normal':
            self.base_scan()
            res=self.get_result2()
            Printer.show_data(res)
        elif type=="hidden":
            self.cut_times=cut_times
            self.cycle_time=cycle_time
            res=self.time_scan()
            Printer.show_data(res)
        # self.get_result2()


    def __dir_get(self):
        dir_op = Dict_oprater(self.dict)
        self.dir_list,self.list_flag = dir_op.creat_list()
        # return dir_list


    def __send_payload(self,dir_list):
        payload = {"search": {"method": self.method, "url": self.url, "speed": self.speed, "dict": dir_list}}
        payload = json.dumps(payload)
        function_requestid = self.payload_sender.send_task(payload)
        return function_requestid
        pass

    def __base_check_result(self,requestid):
        info = init_config.readgitee()
        while True:
            time.sleep(self.cycle_time)
            flag = requests.get("https://gitee.com/" + info['owner'] + "/" + info['repo'] + "/raw/master/" + requestid).status_code
            if (flag == 200):
                break
        res = requests.get("https://gitee.com/" + info['owner'] + "/" + info['repo'] + "/raw/master/" + requestid).text
        return res



    def base_scan(self):
        if self.list_flag==0:
            function_requestid=self.__send_payload(self.dir_list)
            self.request_id=function_requestid
            return function_requestid, 0
        elif self.list_flag==1:
            Msg.info("大字典分批上传中")
            ids = []
            for i in self.dir_list:
                function_requestid = self.__send_payload(i)
                ids.append(function_requestid)
                time.sleep(3)
            self.request_id=ids
            return ids, 1



    def time_scan(self):
        Res={}
        dir_op = Dict_oprater(self.dict)
        self.dir_list=dir_op.creat_list_for_hidden(self.cut_times)
        times_flag=1
        for small_dir in self.dir_list:
            Msg.info("当前正在发送第"+str(times_flag)+"个小字典")
            function_requestid=self.__send_payload(small_dir)
            res=self.__base_check_result(function_requestid)
            res=json.loads(base64.b64decode(res).decode('utf-8'))
            Res.update(res)
            Msg.info(function_requestid+"获取完毕")
            time.sleep(self.cycle_time)
            times_flag+=1
        return Res




    def get_result2(self,):
        if self.list_flag == 0:
            Msg.info("开始轮询结果，轮询周期："+str(self.cycle_time)+"s")
            res=self.__base_check_result(self.request_id)
            try:
                return json.loads(base64.b64decode(res).decode('utf-8'))
            except:
                Msg.error("文件解码失败(文件大小可能超过1M) ID："+self.request_id)
        elif(self.list_flag == 1):
            flag=len(self.request_id)
            Res={}
            while flag != 0:  # 以后添加获取超时选项,
                Msg.info("开始轮询结果，轮询周期："+str(self.cycle_time)+"s")
                for id in self.request_id:
                    res=self.__base_check_result(id)
                    try:
                        res=json.loads(base64.b64decode(res).decode('utf-8'))
                    except:
                        Msg.error("文件解码失败 ID："+id)
                    Res.update(res)
                    Msg.info(id+"结果获取成功！")
                    self.request_id.remove(id)
                    flag -= flag
                return Res

