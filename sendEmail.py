#! python3

#You need to enable less secure app access for this to work
import smtplib
conn = smtplib.SMTP('smtp.gmail.com', 587)
conn.ehlo()
conn.starttls()
conn.login('ishanaraina@gmail.com', '27HermioneGranger511$')
conn.sendmail('ishanaraina@gmail.com', 'ishanaraina@gmail.com', 'Subject: I love Python\n\nDear Ishana,\n This email was sent by Python!\n\n -Ishana')
conn.quit()