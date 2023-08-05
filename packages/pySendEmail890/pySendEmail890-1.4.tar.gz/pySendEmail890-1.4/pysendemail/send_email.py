import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# class SendEmail 参数: mail_user, mail_pass, sender, port=25
# def send_email 参数： title, content, receivers, chaosong=[], file=None
# 样例:
# m = SendEmail('smtp.qq.com', '1165423664', 'taegmjtxhmfmjcci', '1165423664@qq.com')
# m.send_email('title', 'context', ['w35516192@tom.com'], file='main.py')
def file_pd(file):
    t = 1
    if not file:
        return t + 1
    try:
        f = open(file, 'rb').read()
    except Exception as e:
        t = t - 1
        raise Exception('附件打不开！！！！%s' % e)
    return t


class SendEmail:
    def __init__(self, mail_host, mail_user, mail_pass, sender, port=25):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.smtpObj = smtplib.SMTP()
        self.port = port

    def send_email(self, title, content, receivers, chaosong=[], file=None):
        t = 1

        message = MIMEMultipart()  # 创建一个可以同时添加正文和附件的msg
        # 邮件内容设置
        message.attach(MIMEText(content, 'plain', 'utf-8'))  # 邮件内容
        # 邮件主题
        message['Subject'] = title  # 邮件标题
        # 发送方信息
        message['From'] = self.sender  # 邮件发送方邮箱地址
        # 接受方列表
        message['To'] = ','.join(receivers)  # 接收方邮件地址列表，默认第一个
        # 抄送方列表
        message["Cc"] = ";".join(chaosong)
        # 检查文件
        t = file_pd(file)
        if t == 1:
            message.attach(self.dy_file(file))  # 将附件添加到邮件内容当中
        self.send(receivers, message)

    def dy_file(self, file):
        # 添加附件
        file_name = os.path.split(file)[-1]  # 只取文件名，不取路径
        att1 = MIMEText(str(open(file, 'rb').read()), 'base64', 'utf-8')  # 添加附件，由于定义了中文编码，所以文件可以带中文
        att1["Content-Type"] = 'application/octet-stream'  # 数据传输类型的定义
        att1["Content-Disposition"] = f'attachment;filename="{file_name}"'  # 定义文件在邮件中显示的文件名和后缀名，名字不可为中文
        return att1

    def send(self, receivers, message):
        try:
            # 连接到服务器
            self.smtpObj.connect(self.mail_host, self.port)  # 邮箱服务器地址
            # 登录到服务器
            self.smtpObj.login(self.mail_user, self.mail_pass)  # 用户名# 密码(部分邮箱为授权码)
            # 发送
            self.smtpObj.sendmail(
                self.sender, receivers, message.as_string())  # 邮件发送方邮箱地址 # 接收方地址
            # 退出
            self.smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误


# m = SendEmail('smtp.qq.com', '1165423664', 'taegmjtxhmfmjcci', '1165423664@qq.com')
#
# for i in range(10):
#     m.send_email('title', 'context', ['w35516192@tom.com'], file='main.py')
