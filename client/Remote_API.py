import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.scf.v20180416 import scf_client, models
from init import init_config
from Message import Msg
import sys
import time



class API():
    def __init__(self):
        config = init_config.readserver()
        if (config == 0):
            Msg.error("配置文件读取有误，请重新设置")
            sys.exit()
        else:
            Msg.info("配置文件读取成功！")
        access_id=config['id']
        asscee_key=config['key']
        cred = credential.Credential(access_id,asscee_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "scf.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.client = scf_client.ScfClient(cred, config['region'], clientProfile)
        self.function_name=config['function_name']
        pass

    def send_task(self,data):
        # print(data)
        # print(type(data))
        try:
            req = models.InvokeRequest()
            params = {
                "FunctionName": self.function_name,
                "InvocationType": "Event",
                "ClientContext": data
            }
            req.from_json_string(json.dumps(params))
            Msg.info('开始向服务端发起请求')
            try:
                resp = self.client.Invoke(req)
            except:
                Msg.error("请求失败，请检查密钥配置或者网络")
                sys.exit()
            res=resp.to_json_string()
            info=json.loads(res)
            request_id=info["Result"]['FunctionRequestId']
            Msg.info("请求成功,本次请求ID: "+request_id)
            return request_id

        except TencentCloudSDKException as err:
            Msg.error("数据上传失败，请检查传入参数或服务器密钥正确性")
            print(err)

    def get_log(self,request_id):
        Msg.info("开始获取ID："+request_id+"日志")
        req = models.GetFunctionLogsRequest()
        params = {
            "FunctionName": "dirsearch",
            "FunctionRequestId": request_id
        }
        req.from_json_string(json.dumps(params))

        resp = self.client.GetFunctionLogs(req)
        tmp=resp.to_json_string()
        info=json.loads(tmp)
        # print(info)
        try:
            Ret_Meg=info["Data"][0]['RetMsg']
            result=json.loads(Ret_Meg, strict=False)
            return result
        except:
            return False


'''
参数
{"search":{"method":"get","url":"http://www.baidu.com/","speed":"60","dict":["/index.jsp","/index.asp","/index.html"]}}

'''

# a=API()
# # data='{"search":{"method":"get","url":"http://www.baidu.com/","speed":"60","dict":["/index.jsp","/index.asp","/index.html"]}}'
# data="{'search': {'method': 'get', 'url': 'http://www.baidu.com/', 'speed': '20', 'dict': ['/index.html', '/index.aspx', '/index.asp', '/index.php', '/robot.txt']}}"
# a.send_task(data)
# # print(a.get_log("7709a949-a988-46ed-853a-622dd3c0a7ee"))