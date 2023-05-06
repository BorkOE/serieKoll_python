'''
INSTRUKTIONER: Lägg programmet i mappen med videofiler. En csv skapas automatiskt som håller koll på vilka 
avsnitt som tittats på. Starta programmet för att fortsätta på rätta avsnitt. 
'''

from pathlib import Path
import os, statistics, pyinputplus
import csv

def read_csv_to_dict(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = {col: [] for col in csv_reader.fieldnames}
        for row in csv_reader:
            for col in csv_reader.fieldnames:
                data[col].append(row[col])
        return data

def write_dict_to_csv(file_path, data_dict):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_dict.keys())
        csv_writer.writeheader()
        for i in range(len(data_dict[list(data_dict.keys())[0]])):
            row = {col: data_dict[col][i] for col in data_dict.keys()}
            csv_writer.writerow(row)

# Folder för videos
folder = Path(os.getcwd())

# Läs in filer
filer = list(folder.glob('*')) # Lägger filnamnen i en lista

filändelse = [f.suffix for f in filer if f.suffix]
vanligasteFiltyp = statistics.mode(filändelse)  # Ta fram vanligaste filtyp
allaFiltyper = set(filändelse)  # alla filtyper

if os.path.exists(f'{folder.name}.csv'):
    print('Hittade sparfil!')
    tittadeVideos = read_csv_to_dict(f'{folder.name}.csv').get('avklarade')
    print('csv laddad...')
    filtyp = Path(tittadeVideos[0]).suffix

else: # Om det inte finns en fil
    tittadeVideos = []
    print('Det verkar som att du tittar på den här serien första gången...')
    print('Är videon av filtypen: '+ str(vanligasteFiltyp) + '?')
    svar = pyinputplus.inputMenu(['Ja', 'Nej'], numbered=True)

    if svar == 'Ja':
        filtyp = vanligasteFiltyp
    else:
        print('Vilken filtyp är videofilerna av?')
        svar = pyinputplus.inputMenu(allaFiltyper, numbered=True)
        filtyp = str(svar)


# loopar över filer
videoLista = [f.name for f in filer if f.suffix == filtyp]

# Starta while-loop här
while True:
    if tittadeVideos: 
        for v in tittadeVideos:  # Loopa över tittade videos
            if v in videoLista: 
                print(str(v) +' har du redan sett. Jag tar fram nästa video...') # Plockar ut filnamnet från filepath 
                videoLista.remove(videoLista[0])                                 # Ta bort först elementet i listan med alla videos 
    else:
        print('Du har inte sett några videos än...')
        print('Startar första videon...')

    körFil = videoLista[0] # Plocka ut första elementet i videoListan som körfil.
    
    print('\nKörfilen är: '+ körFil)
    input('Tryck enter när du är redo...')
    # Lägg till den körda filen i excelfilen

    # Kör igång filen. OBS! Koden väntar på att videofönstret stängs innan den fortsätter.  
    res = os.system('"' + körFil + '"') 
    if res != 0:    # Felmeddelande mac os
        res = os.system('open "' + körFil + '"') 

    print('Sparar fil...')
    tittadeVideos.append(körFil)
    write_dict_to_csv(f'{folder.name}.csv', {'avklarade':tittadeVideos})

    print('\n\nVill du se ett avsnitt till?')
    slutMeny = ['Spela en till', 'Avsluta']
    slutVal = pyinputplus.inputMenu(slutMeny, numbered=True)
    if slutVal == 'Avsluta':
        break
    else:
        print('Ok, då kör vi en till...')

print('DONE!')

