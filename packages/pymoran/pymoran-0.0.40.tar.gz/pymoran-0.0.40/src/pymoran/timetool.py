import time
import datetime


class TimeClass:
    def __init__(self) -> None:
        pass

    def localdate(self):
        '''
        获取格式化的当前日期
        return {str} 示例：2000-12-12
        '''
        return time.strftime('%Y-%m-%d', time.localtime())

    def localtime(self):
        '''
        获取格式化的当前时间
        return {str} 示例：2000-12-12 18:18:18
        '''
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def timestamp(self):
        '''
        获取当前时间的时间戳
        return {str}
        '''
        return int(time.time())

    def tampToDate(self,tamp):
        '''
        将时间戳转化为指定时间格式
        return {str} 示例：2000-12-12
        '''
        local_time=time.localtime(tamp/1000)
        return time.strftime('%Y-%m-%d', local_time)

    # def timediff(time1, time2):
    #     '''
    #     计算time1与time2的时间差
    #     :param time1 time1
    #     :param time2 time2
    #     return {str}
    #     '''
    #     time1 = time.strptime('%Y-%m-%d %H:%M:%S', time1)
    #     time2 = time.strptime('%Y-%m-%d %H:%M:%S', time2)
    #     timeStamp1 = int(time.mktime(time1))
    #     timeStamp2 = int(time.mktime(time2))
    #     return timeStamp2-timeStamp1

class DateClass:
    def __init__(self):
        pass

    def get_timestamp(self):
        '''
        获取当前时间戳
        '''
        return int(time.time())

    def compare_date(self, startdate, enddate):
        '''比较日期大小，计算结果为结束日期减起始日期

        :param startdate {string}  起始日期
        :param enddate {string}  结束日期
        return {number} 相差天数
        '''
        starttime = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        endtime = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        delta = endtime-starttime
        return delta.days

    def compare_time(self, starttime, endtime):
        '''比较时间大小，计算结果为结束时间减起始时间

        :param starttime {string}  起始时间
        :param endtime {string}  结束时间
        return {number} 相差秒
        '''
        starttime = datetime.datetime.strptime(starttime, '%H:%M:%S')
        endtime = datetime.datetime.strptime(endtime, '%H:%M:%S')
        delta = endtime-starttime
        if delta.days < 0:
            return -1
        return delta.seconds

    def add_date(self, initdate, days):
        """
        从指定日期添加天数
        :param initdate 初始日期
        :param days 需要添加的天数
        return 字符串格式日期
        """
        d = datetime.datetime.strptime(initdate, '%Y-%m-%d')
        d = d+datetime.timedelta(days=days)
        return d.strftime('%Y-%m-%d')

    def get_nowDate(self):
        '''获取当前日期，格式yyyy-MM-dd'''
        return time.strftime('%Y-%m-%d', time.localtime())

    def datestrFormate(self, date):
        '''将日期字符串转化为日期对象'''
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def timestrFormate(self, time):
        '''将时间字符串转化为时间对象'''
        return datetime.datetime.strptime(time, '%H:%M:%S')

    def checkTimeSection(self, time, starttime, endtime):
        '''判断时间是否在指定范围内(等于前后时间)，日期格式HH:mm:ss\n
        :param time {str} 需要判断的时间\n
        :param starttime {str} 起始时间\n
        :param endtime {str} 结束时间\n
        return {bool} True/False
        '''
        if len(time) == 5:
            time = time+':00'
        if len(starttime) == 5:
            starttime = starttime+':00'
        if len(endtime) == 5:
            endtime = endtime+':00'
        leftS = self.compare_time(starttime, time)
        rightS = self.compare_time(time, endtime)
        if leftS >= 0 and rightS >= 0:
            return True
        return False



if __name__=='__main__':
    pass
