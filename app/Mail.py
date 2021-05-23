from dotenv import load_dotenv
load_dotenv()

import os
import smtplib

class Mail:

  def __init__(self):
    self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
    self.from_address = os.getenv('FROM_ADDRESS')
    self.password = os.getenv('PASSWORD')

  def send_mail(self, to_address, message):
      try:
          self.smtp.starttls()
          self.smtp.login(self.from_address, self.password)
          self.smtp.sendmail(self.from_address, to_address, message.as_string())
          self.smtp.close()
      except Exception as e:
          print('Error: ' + str(e))