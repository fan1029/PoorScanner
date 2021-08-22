from init import Args,Banner
from scan import Scan


if __name__ == '__main__':
    Banner.showbanner()
    url,dir,speed,method,type,cut_times,cycle_time=Args.get_args()
    new_scaner=Scan(url,dir,method,speed,type,cut_times,cycle_time)


