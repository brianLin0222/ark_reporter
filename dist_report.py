# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
# from email.mime.base import MIMEBase
# # from google.oauth2 import service_account
# # from googleapiclient.discovery import build
# from apiclient import errors
# import base64
# import os
# import mimetypes


import pickle
import os.path
import base64
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


API = ["https://www.googleapis.com/auth/gmail.send"]

REPORT_PATH = r"./report"


def find_token():
    try:
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as tk:
                creds = pickle.load(tk)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', API)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    
    except:
        raise Exception("API token unavailable, please run gmail_auth.py...")
        


def service_login(creds):
    try:
        return build('gmail','v1',credentials=creds)
    except Exception as err:
        raise Exception(f"Unable to initiate Gmail API, error:{err}")
        
        

class create_content():
    
    def __init__(self,sender, recip, subject):
        self.sender = sender
        self.recip = recip
        self.sub = subject
    
    
    def _basicInfo(self,mime_object):
        mime_object['from'] = self.sender
        mime_object['to'] = self.recip
        mime_object['subject'] = self.sub
        return mime_object
    
    
    def _msgEncode(self,msg):
        return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}
    
    def simple_html(self,messsage):
        msg = MIMEText(messsage,'html')
        msg = self._basicInfo(msg)
        # return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode()}
        return self._msgEncode(msg)
    
    
    def multi_content(self,message,img=None,attach=None,html=True):
        msg = MIMEMultipart()
        msg = self._basicInfo(msg)
        if html:
            html = MIMEText(message,'html')
            msg.attach(html)
        if img:
            with open(img, 'rb') as pic:
                image_b = MIMEImage(pic.read())
            msg.attach(image_b)
        if attach:
            for file in attach:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(os.path.join(REPORT_PATH,f'{file}.xlsx'), "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',filename=f"{file}.xlsx")
                msg.attach(part)
            
        return self._msgEncode(msg)


    