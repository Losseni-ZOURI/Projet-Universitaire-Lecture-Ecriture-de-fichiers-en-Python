# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
"""

#-------------------------Ouverture du fichier pour la lecture-------------------------
file = open("../data_base/groupe12E_data.txt", "r", encoding="utf-8")
text = file.read()

#-------------------------Séparation en liste de chaines de caracteres où chaque chaîne correspond à un film-------------------------
list_films = text.split("%")

#-------------------------Création de la liste de films final, en supprimant les chaines vides causées par la succession %%-------------------------
final_list = []

for film in list_films:
    film_formatOK = film.strip()
    if film_formatOK != "":
        final_list.append(film_formatOK)

#-------------------------Liste des champs pour chaque film-------------------------
champs = ["title", "nbvotes", "score", "duration", "year", "type", "restriction", "desc"]

#-------------------------Organisation de chaque film en dictionnaire-------------------------
films_dataset = []
for _ in champs:
    films_dataset.append([])

for i in range(len(champs)):
    for film in final_list:

        champ =champs[i]
        start = film.find(champ+"=") + len(champ)+1
        if i < (len(champs) - 1):
            end = film.find(champs[i+1]+"=", start)
        else:
            end = len(film)
       
        res = film[start:end].strip()
        films_dataset[i].append(res)


#-------------------------Organisation avec les bons types de données-------------------------
final_dataset = []
for _ in champs:
    final_dataset.append([])

for i in range(len(films_dataset)):
    for j in range(len(films_dataset[i])):
        if  isinstance(films_dataset[i][j], str):
            films_dataset[i][j] = films_dataset[i][j].rstrip(",").strip()
        if i == 0 or i==6: #title et restriction
            final_dataset[i].append(films_dataset[i][j].title() if films_dataset[i][j] else '')
        elif i == 1: #nbvotes
            final_dataset[i].append(int(films_dataset[i][j]) if films_dataset[i][j] else None)
        elif i == 2: #score
            final_dataset[i].append(float(films_dataset[i][j]) if films_dataset[i][j] else None)
        elif i == 3 or i == 4: #duration et year
            final_dataset[i].append(int(float(films_dataset[i][j])) if films_dataset[i][j] else None)
        elif i == 5: #type
            final_dataset[i].append(films_dataset[i][j])
        elif i == 7: #desc
            final_dataset[i].append(films_dataset[i][j].strip() if films_dataset[i][j] else '')
       


#-------------------------Création du csv-------------------------
groupe = "12E"
colonnes = ['Référence', 'Titre', 'Durée', 'Année', 'Restriction', 'Nombre de votes', 'Score', 'Description']

result = open("../data_res/groupe12E_data.csv", "w", encoding='cp1252')
result.write(';'.join(colonnes)+'\n')
compteur = 1
nb_films = len(final_dataset[0])

for i in range(nb_films):
    ref = f"F-{groupe}-{compteur}-{final_dataset[4][i]}"
    compteur+=1

    ligne = [
        ref,
        final_dataset[0][i],
        final_dataset[3][i],
        final_dataset[4][i],
        final_dataset[6][i],
        final_dataset[1][i],
        final_dataset[2][i],
        final_dataset[7][i]
    ]
    ligne_str = []
    for x in ligne:
        ligne_str.append(str(x))
    result.write(';'.join(ligne_str)+'\n')
   
result.close()

#-------------------------Fonctions pour le calcul des infos-------------------------
def score_min(data):
    score = data[2]
    min = score[0]
    for d in score:
        if d <= min :
            min = d
    return min

def score_max(data):
    score = data[2]
    max = score[0]
    for d in score :
        if d >= max :
            max = d
    return max

def score_mean(data):
    total = 0.0
    score = data[2]
    for d in score:
        total += d
   
    return round(total/len(score), 2)

def drama_percent(data):
    types = data[5]
    total = 0
    for d in types:
        genres = []
        for g in d.split('|'):
            genres.append(g.strip().lower())
        if 'drama' in genres:
            total += 1
    return round((total/len(types)*100), 2)  

def action_percent(data):
    types = data[5]
    total = 0
    for d in types:
        genres = []
        for g in d.split('|'):
            genres.append(g.strip().lower())
        if 'action' in genres:
            total += 1
    return round((total/len(types)*100), 2)  
 


#-------------------------Création du fichier d'infos-------------------------
file_name = "groupe12E_infos.txt"
info = open(f"../data_res/{file_name}", "w", encoding="utf-8")

info.write(f"Nom du fichier : {file_name}\n")
info.write(f"Nombre de films : {len(final_dataset[0])}\n")
info.write(f"Score minimum : {score_min(final_dataset)}\n")
info.write(f"Score maximum : {score_max(final_dataset)}\n")
info.write(f"Score moyen : {score_mean(final_dataset)}\n")
info.write(f"Taux de drames : {drama_percent(final_dataset)}\n")
info.write(f"Taux de films d'action : {action_percent(final_dataset)}\n")

info.close()
file.close()
