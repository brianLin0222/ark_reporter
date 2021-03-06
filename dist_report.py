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
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
SAVE_PATH = os.path.join(BASE_PATH,"report")
TOKEN_PATH = os.path.join(BASE_PATH,'token.pickle')
CRED_PATH = os.path.join(BASE_PATH,'credentials.json')
REPORT_PATH = os.path.join(BASE_PATH,"report")


def find_token():
    try:
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH,'rb') as tk:
                creds = pickle.load(tk)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED_PATH, API)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'wb') as token:
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
            for pictures in img:
                with open(pictures, 'rb') as pic:
                    image_b = MIMEImage(pic.read())
                    cid = pictures.split("\\")[-1].split(".")[0]
                    image_b.add_header('Content-ID', '<{}>'.format(cid))
                    image_b.add_header('Content-Disposition','inline',filename=f'{cid}.png')
                msg.attach(image_b)
        if attach:
            for file in attach:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(os.path.join(REPORT_PATH,f'{file}.xlsx'), "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',filename=f"{file}.xlsx")
                msg.attach(part)
            
        return self._msgEncode(msg)
