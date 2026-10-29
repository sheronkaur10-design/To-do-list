import os
from datetime import date
import smtplib
from email.message import EmailMessage

def skicka_gmail(text):
    avsandare = 'sheronkaur10@gmail.com'
    mottagare = 'sheronkaur10@gmail.com'
    applosenord =  os.getenv("GMAIL_APP_PASSWORD")

    if not applosenord:
        raise ValueError("Miljövariabeln GMAIL_APP_PASSWORD saknas")

    mejl = EmailMessage()
    mejl['Subject'] = 'Min att-göra-sammanfattning'
    mejl['From'] = avsandare
    mejl['To'] = mottagare
    mejl.set_content(text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(avsandare, applosenord)
        server.send_message(mejl)

print ('Välkommen till din Att-Göra-Lista!')

filnamn = 'todo.txt'

while True:
    val = input('\nVad vill du göra idag?\n'
    'r: Läsa\n'
    'a: Skriva\n'
    'k: Markera som klar\n'
    'd: Radera\n'
    's: Sammanfattning av dagen\n'
    'e: Exit\n'
    'Svar: ')
    if val == 'r':
        with open(filnamn, 'r', encoding='utf-8') as f:
            innehall = f.readlines()
            print('\nDin att-göra-lista:')
            print(innehall)
    elif val == 'a':
        ny_uppgift = input('Vad vill du skriva?: ')
        with open(filnamn, 'a', encoding='utf-8') as f:
            f.write(ny_uppgift + '\n')
        print('Uppgiften har sparats!')
    elif val == 'k':
        with open(filnamn, 'r', encoding='utf-8') as f:
            pass
        with open(filnamn, 'r', encoding='utf-8') as f:
            uppgifter = f.readlines()
        if len(uppgifter) == 0:
            print('Det finns inga uppgifter att markera.')
        else:
            for i, uppgift in enumerate(uppgifter, start=1):
                print(i, uppgift.strip())
            try:
                nummer = int(input('Vilken uppgift är klar?'))
                if 1 <= nummer <= len(uppgifter):
                    uppgift = uppgifter[nummer - 1]
                    if uppgift.startswith('✅'):
                        print('Uppgiften är redan klar!')
                    else:
                        uppgifter[nummer - 1] = ('✅ ' + uppgift.replace('☐ ', '', 1))
                        with open(filnamn, 'w',encoding='utf-8' ) as f:
                            f.writelines(uppgifter)
                            print('Uppgiften är nu klar! ✅')
                else:
                    print('Ogiltigt nummer!')
            except ValueError:
                print('Skriv ett giltigt nummer!')
    elif val == 'd':
        while True:
            with open(filnamn, 'r', encoding='utf-8') as f:
                uppgifter = f.readlines()
            if len(uppgifter) == 0:
                    print('Det finns inga uppgifter att radera.')
                    break
            print('\nDina uppgifter:')
            for i, uppgift in enumerate(uppgifter, start=1):
                print(i, uppgift.strip())
            val_radera = input('Vilken uppgift vill du radera?' '(Skriv 0 för att avsluta):')
            try:
                nummer = int(val_radera)
                if nummer == 0:
                    print('Tillbaka till menyn.')
                    break
                if 1 <= nummer <= len(uppgifter):
                    borttagen = uppgifter.pop(nummer - 1)
                    with open(filnamn, 'w',encoding='utf-8') as f:
                        f.writelines(uppgifter)
                    print('Uppgiften har readerats:', borttagen.strip())
                else:
                    print('Ogiltigt nummer!' 'Försök igen.')
            except ValueError:
                print('Skriv ett giltigt nummer!')
    elif val == 's':
        with open(filnamn, 'r', encoding='utf-8') as f:
            uppgifter = f.readlines()
        klara = sum(1 for uppgift in uppgifter if uppgift.startswith('✅'))
        totalt = len(uppgifter)

        text_sammanfattning = (
            '--- Sammanfattning ---\n'
            f'Datum: {date.today().strftime("%Y-%m-%d")}\n\n'
            f'Totalt antal uppgifter: {totalt}\n'
            f'Klara: {klara}\n'
            f'Kvar: {totalt - klara}\n\n'
            'Dagens uppgifter:\n'
            + ''.join(uppgifter)
        )
        print(text_sammanfattning)
        try:
            skicka_gmail(text_sammanfattning)
            print('Sammanfattning har skickats via Gmail')
        except Exception as fel:
            print('Mejlet kunde inte skickas:', fel)

    elif val == 'e':
        print('Hej då')
        break
    else:
        print('Fel val! Försök igen.')