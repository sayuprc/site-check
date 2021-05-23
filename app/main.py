import sys
import os
import re
import utils

from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

from Crawler import Crawler
from Mail import Mail

from dotenv import load_dotenv
load_dotenv()

absolute_path = os.path.dirname(os.path.abspath(__file__))
f = open('target_urls', 'r')
urls = f.readlines()
f.close()

mail = Mail()
from_address = os.getenv('FROM_ADDRESS')
to_address = os.getenv('TO_ADDRESS')

for url in urls:
    site_name = re.sub('http(s)?://', '', url).replace('/', '').rstrip()

    current_file_path = os.path.join(absolute_path, 'image/' + site_name + '/current')
    previous_file_path = os.path.join(absolute_path, 'image/' + site_name + '/previous')

    current_file_name = current_file_path + '/screen.png'
    previous_file_name = previous_file_path + '/screen.png'

    utils.mkdir(current_file_path)
    utils.mkdir(previous_file_path)

    if utils.is_file_exists(current_file_name):
      utils.move_file(current_file_name, previous_file_name)

    selenium_crawler = Crawler()

    selenium_crawler.get_screenshot(url, current_file_name)

    if utils.is_file_exists(current_file_name) and utils.is_file_exists(previous_file_name):
        if not utils.diff_image(current_file_name, previous_file_name):
          message = MIMEMultipart()
          message['Subject'] = '差分検知[' + site_name + ']'
          message['From'] = from_address
          message['To'] = to_address
          message['Date'] = formatdate()

          current_file_size = os.path.getsize(current_file_name) / 1000 / 1000
          previous_file_size = os.path.getsize(previous_file_name) / 1000 / 1000

          if current_file_size + previous_file_size <= 25:
            message.attach(MIMEText('今回'))
            current = MIMEBase('image', 'png')
            file = open(current_file_name, 'rb+')
            current.set_payload(file.read())
            file.close()
            encoders.encode_base64(current)
            message.attach(current)

            message.attach(MIMEText('---------------------------------------------'))

            message.attach(MIMEText('前回'))
            previous = MIMEBase('image', 'png')
            file = open(previous_file_name, 'rb+')
            previous.set_payload(file.read())
            file.close()
            encoders.encode_base64(previous)
            message.attach(previous)
          else:
            message.attach(MIMEText('差分あり(ファイルサイズが大きいため添付不可)'))

          mail.send_mail(to_address, message)