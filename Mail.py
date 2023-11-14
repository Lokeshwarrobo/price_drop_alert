import smtplib


def send_mail(mail_id, msg):

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login("lokeshwar.robo@gmail.com", "vqhk ljfw qfsb xpvs")

    message = "price decreased " + msg

    s.sendmail("lokeshwar.robo@gmail.com", mail_id, message)

    s.quit()
