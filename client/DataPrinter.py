from Message import Msg

class Printer():

    @staticmethod
    def check_200(res):
        Msg.info("正在进行结果过滤.")
        len_list={}

        for i in res['result200']:
            if i['status_code']==200:
                key_list=len_list.keys()
                if i['length'] not in key_list:
                    len_list[i['length']]=1
                if i['length'] in key_list:
                    len_list[i['length']]+=1

        for v in len_list:
            if len_list[v]>10:
                for i in res['result200']:
                    if i['length']==v:
                        i['status_code']=0
        return  res
        pass

    @staticmethod
    def deal_data(i):
        data="Statues: " + str(i['status_code']) + "      Len: " + str(i['length']) + "      Url: " + i['url']
        print(data)

    @classmethod
    def print_data(cls,*args):
        for i in args:
            for res in i:
                cls.deal_data(res)
    @classmethod
    def show_data(cls,res):
            Msg.info("结果获取成功")
            print("---------------------------------------------------------------------------------------------------")
            res200 = res['result200']
            res300 = res['result300']
            res400 = res['result400']
            res500 = res['result500']
            cls.print_data(res200,res300,res400,res500)
            # for i in res200:
            #     cls.deal_data(i)
            # for i in res300:
            #     cls.deal_data(i)
            # for i in res400:
            #     cls.deal_data(i)
            # for i in res500:
            #     cls.deal_data(i)
