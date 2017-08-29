#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "441629632@qq.com"  # 用户名
mail_pass = "qdicjwbsnduabhji"  # 口令

sender = mail_user
receivers = ['coolcoolad@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def sendEmail(subject, content):
	msg = MIMEText(content, 'plain', 'utf-8')
	msg['Subject'] = Header(subject, 'utf-8')
	msg['From'] = sender
	msg['To'] = receivers[0]

	try:
		smtpObj = smtplib.SMTP_SSL(mail_host, 465)
		smtpObj.login(mail_user, mail_pass)
		smtpObj.sendmail(sender, receivers, msg.as_string())
		print "邮件发送成功"
	except smtplib.SMTPException:
		print "Error: 无法发送邮件"
