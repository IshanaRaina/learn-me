#! python3

#You need to enter your email credentials and enable less secure app access for this to work
import imapclient, email, requests, os, PyPDF2
from bs4 import BeautifulSoup

conn = imapclient.IMAPClient('imap.gmail.com', ssl = True)
conn.login('emailaddress', 'password')
conn.select_folder('INBOX', readonly = True)
messages = conn.search(['SINCE', '01-Jan-2019', 'SUBJECT', 'trip with Uber'])
i = 1
for msgid, message_data in conn.fetch(messages, 'RFC822').items():
    email_message = email.message_from_bytes(message_data[b'RFC822'])
    print("-------------------------------------------------------------")
    print("Msg ID: ", msgid, "\nFrom: ", email_message.get('From'), "\nSubject: ", email_message.get('Subject'), "\nLength of email message payload: ", len(email_message.get_payload()))
#email_message.get_payload() returns a list of 3 objects belonging to class email.message.Message    
    attachment = email_message.get_payload()[0]
    print("Content Type[0]: ", attachment.get_content_type())
#index 0 has type: text/html with filename: None and index 1 & 2 have type: image/png with filename: map
    html_doc = attachment.get_payload(decode = True)
#On inspecting text/html, we find <a href="link"> Download PDF </a>
#Store the entire text/html in a document and then parse it for the required tag
    soup = BeautifulSoup(html_doc, 'html.parser')
    a_tag = soup.find('a', text = ' Download PDF ')
    url = a_tag.attrs['href']
    
#wget.download(url, 'C:\\Users\\iraina\\Downloads\\UberReceipts')
#Throws an error when running more than once

    r = requests.get(url)
    with open('C:\\Users\\iraina\\Downloads\\UberReceipts\\Receipt'+str(i)+'.pdf', 'wb') as file:
        file.write(r.content)
#Doesn't throw an error when running more than once but overwrites the file to reflect the last one
    i+=1
print("-------------------------------------------------------------")
print("The value of is:", i)
conn.logout()









