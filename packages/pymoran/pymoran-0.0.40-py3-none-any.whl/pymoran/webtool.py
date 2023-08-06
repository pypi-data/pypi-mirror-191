from pymoran import strtool

class MsgClass:
    def __init__(self):
        self.msgdata = {
            'code': -1,
            'msg': '',
            'data': {},
            'other': {}
        }
        self.jsonclass = strtool.JsonClass()

    # def change_datatype(self, byte):
    #     if isinstance(byte, bytes):
    #         return str(byte, encoding='utf-8')
    #     return json.JSONEncoder.default(byte)

    def successMsg(self, msg: str = '', data: dict or list = {}):
        '''
        成功消息
        :param msg 提示内容，默认空
        :param data 回传的内容，默认空字典
        :return {str} Json字符串
        '''
        self.msgdata['code'] = 0
        self.msgdata['msg'] = msg
        self.msgdata['data'] = data
        return self.jsonclass.jsonToDumps(self.msgdata)

    def errorMsg(self, msg: str = ''):
        '''
        错误消息
        :param msg 提示内容，默认空
        :return {str} Json字符串
        '''
        self.msgdata['code'] = -1
        self.msgdata['msg'] = msg
        return self.jsonclass.jsonToDumps(self.msgdata)

    def abnormalMsg(self, msg: str = ''):
        '''
        异常消息
        :param msg 提示内容，默认空
        :return {str} Json字符串
        '''
        self.msgdata['code'] = -2
        self.msgdata['msg'] = msg
        return self.jsonclass.jsonToDumps(self.msgdata)

    def loginMsg(self, data: dict or list = {}):
        '''
        登录成功消息
        :param msg 提示内容，默认空
        :return {str} Json字符串
        '''
        self.msgdata['code'] = 1000
        self.msgdata['msg'] = 'success'
        self.msgdata['data'] = data
        return self.jsonclass.jsonToDumps(self.msgdata)

    def logoutMsg(self):
        '''
        未登录消息
        :return {str} Json字符串
        '''
        self.msgdata['code'] = 1001
        self.msgdata['msg'] = '登录状态已失效，请重新登录！'
        return self.jsonclass.jsonToDumps(self.msgdata)

    def customMsg(self, code: int = 0, msg: str = '', data: dict or list = {}, other: dict or list = {}):
        '''
        自定义消息
        :param code 消息代码，默认0
        :param msg 提示内容，默认空
        :param data 回传的内容，默认空字典
        :param other 其他内容，默认空字典
        :return {str} Json字符串
        '''
        self.msgdata['code'] = code
        self.msgdata['msg'] = msg
        self.msgdata['data'] = data
        self.msgdata['other'] = other
        # if d:
        #     # d参数为True则不进行json转换
        #     return msgdata
        return self.jsonclass.jsonToDumps(self.msgdata)

# class FormCheckClass:
#     '''
#     表单字段验证类
#     '''
#     def __init__(self):
#         self.msgclass = MsgClass()
#         self.return_msg = self.msgclass.abnormalMsg()
#         self.re = strtool.RegularClass()
#         self.strdeal = StrDeal()

#     def check(self, data, **kw):
#         '''
#         表单验证并清洗数据

#         @param data {dict} 需要验证的数据

#         @param cdt_data {dict} 额外的判定条件：

#             “key_maxlength”:允许的字符串最大长度

#             “key_msgtitle”:返回的错误信息标题

#         return {dict} 验证后的信息
#         '''
#         if kw and kw['cdt_data']:
#             self.cdt_data = kw['cdt_data']
#         for key in data:
#             if key == 'name':
#                 self.return_msg = self.name(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'sort':
#                 self.return_msg = self.sort(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'title':
#                 self.return_msg = self.title(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'language':
#                 self.return_msg = self.language(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'digest':
#                 self.return_msg = self.digest(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'tag':
#                 self.return_msg = self.tag(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'email':
#                 self.return_msg = self.email(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#             if key == 'content':
#                 self.return_msg = self.content(data[key])
#                 if self.return_msg == True:
#                     continue
#                 return self.return_msg
#         return data

#     def name(self, val):
#         '''
#         各类名称/姓名
#         '''
#         returnMsg = True
#         max_length = self.cdt_data['name_maxlength'] or 50
#         msg_title = self.cdt_data['name_msgtitle'] or '名称'
#         # if self.cdt_data['name_maxlength']:
#         #     max_length = self.cdt_data['name_maxlength']
#         # if self.cdt_data['name_msgtitle']:
#         #     msg_title=self.cdt_data['name_msgtitle']
#         if val == '':
#             returnMsg = self.msgManage.creat_abnormalMsg(
#                 msg=msg_title+'不能为空'
#             )
#         if len(val) > max_length:
#             returnMsg = self.msgManage.creat_abnormalMsg(
#                 msg=msg_title+'过长，限制'+max_length/2+"字"
#             )
#         val = self.strdeal.filter_str(val)
#         return returnMsg

#     def sort(self, val):
#         '''
#         排序字段
#         '''
#         returnMsg = True
#         if self.re.check_num(val) == False:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='排序值必须为0或正整数')
#         return returnMsg

#     def title(self, val):
#         '''
#         标题
#         '''
#         returnMsg = True
#         if val == '':
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='标题不能为空')
#         if len(val) > 500:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='标题过长')
#         return returnMsg

#     def language(self, val):
#         '''
#         文章语言版本
#         '''
#         returnMsg = True
#         laArr = ['zh', 'en']
#         if val not in laArr:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='错误的操作')
#         return returnMsg

#     def digest(self, val):
#         '''
#         文章摘要
#         '''
#         returnMsg = True
#         if len(val) > 500:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='摘要内容过长')
#         return returnMsg

#     def tag(self, val):
#         '''
#         标签
#         '''
#         returnMsg = True
#         if len(val) > 255:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='标签内容过长')
#         return returnMsg

#     def email(self, val):
#         '''
#         邮箱
#         '''
#         returnMsg = True
#         if val == '':
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='邮箱不能为空')
#         b = self.re.email(val)
#         if b == False:
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='邮箱格式错误')
#         return returnMsg

#     def content(self, val):
#         '''
#         内容
#         '''
#         returnMsg = True
#         if val == '':
#             returnMsg = self.msgManage.creat_abnormalMsg(msg='内容不能为空')
#         val = self.strdeal.filter_str(val)
#         return returnMsg


# class Net_Request:
#     def __init__(self):
#         pass

#     def get(self, url, params):
#         res = requests.get(url=url, params=params)
#         return res.text

#     def post_text(self, url, data):
#         res = requests.post(url=url, data=data)
#         return res.text

#     def post_content(self, url, data):
#         res = requests.post(url=url, data=data)
#         return res.content