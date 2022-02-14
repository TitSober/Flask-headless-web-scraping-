import smtplib



def sendMail(receipient,site):
    content = "Posodobitev strani "+ site +" .\n "


    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    sender='pythonanytime@gmail.com'
    
    mail.login('email@site.com','geslo')

    header='To:'+receipient+'\n'+'From:'\
    +sender+'\n'+'subject:Novo obvestilo\n'
    content=header+content
    mail.sendmail(sender,receipient, content)
    mail.close()
