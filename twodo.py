#!/usr/bin/env python

'''A library for creating 2Do-compatible tasks'''

__author__ = 'spencer@trbc.org'
__version__ = '0.2-devel'

from random import randint
import smtplib
from email.mime.text import MIMEText

class Task(object):
    def __init__(self,
                 cal=None,
                 uid=0,
                 t=None,
                 n=None,
                 u=None,
                 p=0,
                 comp=0,
                 due=None):
        '''An object to hold and correctly format a 2Do task

        Args:
            cal:    REQUIRED: The calendar which the task will be created in
            t:      REQUIRED: The 'title' field of the created task
            u:      The 'URL' field of the created task
            n:      The 'note' field of the created task
            p:      The 'priority' field of the created task. Either 0, 9, 5, or 1. 0 if no priority.
            comp:   The 'completed' field of the created task. Boolean field: 0 = incomplete, 1 = complete
            due:    The 'due date' field of the created task. Something in the form of: 2009-12-22
        
        Example:
            t1 = twodo.Task(cal='TRBC', t='This is a test', n='test test test', p='1', due='2009-12-22')
        '''
        self.cal = cal
        self.uid = self.GenerateUID()
        self.t = t
        self.u = u
        self.n = n
        self.p = p
        self.comp = comp
        self.due = due
    
    def GenerateUID(self):
        '''Generate a Unique IDentifier'''
        return '2DoDEADBEEF-1234-5678-9012-%s' % randint(100000000000, 999999999999)
    
    def FormatURL(self):
        '''Correctly format the URL to be opened on the iPhone or iPod Touch'''
        url = 'twodo://share|_;_|cal|_:_|%s|_;_|uid|_:_|%s|_;_|t|_:_|%s|_;_|p|_:_|%s|_;_|comp|_:_|%s|_;_|actt|_:_|-1|_;_|recfrom|_:_|0|_;_|recval|_:_|0|_;_|rectype|_:_|0|' % (self.cal, self.uid, '%20'.join(self.t.split()), self.p, self.comp)
        if(self.due):
            url += '_;_|due|_:_|%s|' % self.due
        if(self.u):
            url += '_;_|u|_:_|%s|' % '%20'.join(self.u.split())
        if(self.n):
            url += '_;_|n|_:_|%s' % '%20'.join(self.n.split())
        return url
    

class Email(object):
    def __init__(self,
                 server=(None, None),
                 username=None,
                 password=None,
                 sender=None,
                 recipients=None,
                 task=None):
        '''Format and send an Email containing the task
        
        Args:
            server:     REQUIRED: A tuple containing the address and port of the smtp server
            username:   The username (if required) to authenticate to the smtp server
            password:   The password (if required) to authenticate to the smtp server
            sender:     REQUIRED: The email address from which the email will be sent
            recipients: REQUIRED: The email address(es) to which the email will be delivered
            task:       REQUIRED: The Task object to include in the email
        
        Example:
            e1 = twodo.Email(server=('mail.trbc.org',465), username='spencer@trbc.org', password='********', sender='spencer@trbc.org', recipients=['spencer@trbc.org',], task=t1)
        '''
        self.server = server
        self.username = username
        self.password = password
        self.body = '''
        <html>
        <head></head>
        <body>
            <p>Hi,<br/>
            <br/>
            I would like to share a ToDo task with you. If you have the <b><a href="http://ax.search.itunes.apple.com/WebObjects/MZSearch.woa/wa/search?entity=software&media=all&restrict=false&submit=seeAllLockups&term=2do">2Do App</a></b> installed, click on the following link:<br/>
            <a href="%s">Add: %s</a>
            </p>
            <p>To Do: <i>%s</i><br/>
            Due Date: <i>%s</i><br/>
            URL: <i>%s</i></p>
            <p>%s</p>
            <p><b>Sent using the twodo library (%s) by %s</b></p>
        </body>
        </html>
        ''' % (task.FormatURL(), task.t, task.t, task.due, task.u, task.n, __version__, __author__)
        
        self.msg = MIMEText(self.body, 'html')
        self.msg['Subject'] = 'To Do: %s' % task.t
        self.msg['From'] = sender
        self.msg['To'] = ', '.join(recipients)
    
    def SendEmail(self):
        server = smtplib.SMTP_SSL(self.server[0], self.server[1])
        if(self.username != 'None'):
            server.login(self.username, self.password)
        server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        server.quit()
    
