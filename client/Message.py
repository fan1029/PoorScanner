from colorama import  Fore, Back, Style,init
import time

class Msg():
    init(autoreset=True)


    @classmethod
    def info(cls,text):
        time1 = time.strftime("%H:%M:%S", time.localtime())
        time1 = "[" + time1 + "]"
        print(Fore.GREEN+'[+]'+time1+Style.RESET_ALL+text)

    @classmethod
    def warn(cls,text):
        time1 = time.strftime("%H:%M:%S", time.localtime())
        time1 = "[" + time1 + "]"
        print(Fore.YELLOW+'[!]'+time1+text+Style.RESET_ALL)

    @classmethod
    def error(cls,text):
        time1 = time.strftime("%H:%M:%S", time.localtime())
        time1 = "[" + time1 + "]"
        print(Fore.RED+'[-]'+time1+ text+Style.RESET_ALL)

    @classmethod
    def show(cls,text):
        print(Fore.LIGHTBLUE_EX+text+Style.RESET_ALL)