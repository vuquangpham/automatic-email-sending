import smtplib
from PIL import Image
import pathlib
from email.message import EmailMessage
from string import Template
import sys

def initializeEmailService(name):
  email = EmailMessage()
  email['from'] = name
  email['subject'] = 'Automatic email'
  return email
  

def readFile(file_name):
  return pathlib.Path(file_name).read_text()

def creating_smtp_server(sending_info):
  user_name = sending_info['user']
  password = sending_info['password']
  content = sending_info['content']
  user_list = sending_info['user_list']

  if '.html' in content:
    path = sending_info['content']
    content = Template(pathlib.Path(path).read_text())

  try:
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
      # Hello -> can be omitted
      server.ehlo()
      # Secure connection
      server.starttls()
      # Login to server
      server.login(user_name, password)
      # Sending to each of users_list
      for user in user_list:
        email = initializeEmailService('PythonBot')
        email['to'] = user
        email.set_content(content.substitute(name = user, src = './img/avenger.jpg'), 'html')
        print(content.substitute(name = user))
        server.send_message(email)
      # Close connection
      server.quit() 
  except:
    return False
  else:
    return True  

def main(user, password, content):
  # Getting list of user
  user_list = readFile('.users').splitlines()
  # Sending information
  sending_info = {
    'user': user,
    'password': password,
    'content': content,
    'user_list': user_list,
  }
  # Creating SMTP server
  isSuccess = creating_smtp_server(sending_info)

  if (isSuccess):
    print('Sent successfully')
  else:
    print('Something went wrong!!!')  

if __name__ == '__main__':
  main(*sys.argv[1:])