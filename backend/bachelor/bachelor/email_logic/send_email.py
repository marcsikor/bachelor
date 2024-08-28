import smtplib
from email.mime.text import MIMEText
from .email_credentials import *

def send_email(email, option, name = ""):

   if option == 'new-user':
      subject = "Witaj nowy użytkowniku"
      body = '''Drogi użytkowniku,

Został ci przydzielony dostęp do systemu. 
Wejdź na swój profil i utwórz swoje konto.

Z wyrazami szacunku,
Obsługa'''
   elif option == 'approved':
      subject = 'Zatwierdzono raport "' + name + '"'
      body = '''Drogi użytkowniku,

Twój raport o nazwie "''' + name + '''" został zatwierdzony.
W przypadku wszelkich pytań skontaktuj się z zarządem swojej jednostki.

Z wyrazami szacunku,
Obsługa'''
   elif option == 'rejected':
      subject = 'Odrzucono raport "' + name + '"'
      body = '''Drogi użytkowniku,

Twój raport o nazwie "''' + name + '''" został odrzucony.
Możesz go znaleźć w sekcji "Aktywne zgłoszenia"
W przypadku wszelkich pytań skontaktuj się z zarządem swojej jednostki.

Z wyrazami szacunku,
Obsługa'''
   elif option == 'payout':
      subject = 'Wydano środki z raportu "' + name + '"'
      body = '''Drogi użytkowniku,

Status twojego raportu o nazwie "''' + name + '''" został zmieniony.
Oznacza to, że środki z niego wynikające powinny zostać wypłacone.
W przypadku wszelkich pytań skontaktuj się z zarządem swojej jednostki.

Z wyrazami szacunku,
Obsługa'''
   
   sender = SENDER_EMAIL_ADDRESS
   password = SENDER_EMAIL_PASSWORD

   msg = MIMEText(body)
   print(subject)
   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = email
   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
      smtp_server.login(sender, password)
      smtp_server.sendmail(sender, email, msg.as_string())
   print("Message sent!")
