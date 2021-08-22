
import os
from Message import  Msg
import sys
from init import init_config
'''
字典组成数组上传
判断字典大小 字典切分
'''

class Dict_oprater():
    def __init__(self,filename):
        self.config=init_config.readdir()
        self.dir_list=[]
        self.cut_size=int(self.config['cut_size'])
        filename=filename
        file_path = os.path.join(os.path.abspath('./dictionary'), filename)
        try:
            with open(file_path) as f:
                tmp=f.readlines()
                for i in tmp:
                    i=i.replace("\n","")
                    self.dir_list.append(i)
            self.dir_len=len(self.dir_list)
            Msg.info("目录加载成功")
        except:
            Msg.error("目录读取失败，请检查文件是否在当前目录中！")
            sys.exit()
        pass
    def creat_list(self):
        if(len(self.dir_list)<self.cut_size):
            return self.dir_list,0
        else:
            cut_dir_list=[]
            cut_times=len(self.dir_list)//self.cut_size
            tmp2 = len(self.dir_list) // cut_times
            tmp3 = len(self.dir_list) // cut_times
            tmp = 0
            for i in range(0, cut_times):
                dir_for_use=self.dir_list[tmp:tmp2]
                tmp = tmp2
                if (tmp2 < len(self.dir_list)):
                    tmp2 = tmp2 + tmp3
                else:
                    tmp2 = len(self.dir_list)
                cut_dir_list.append(dir_for_use)
            return  cut_dir_list,1

    def creat_list_for_hidden(self,cut_times):
        cut_dir_list=[]
        tmp2 = len(self.dir_list) // cut_times
        tmp3 = len(self.dir_list) // cut_times
        tmp = 0
        for i in range(0, cut_times):
            dir_for_use = self.dir_list[tmp:tmp2]
            tmp = tmp2
            if (tmp2 < len(self.dir_list)):
                tmp2 = tmp2 + tmp3
            else:
                tmp2 = len(self.dir_list)
            cut_dir_list.append(dir_for_use)
        return cut_dir_list
