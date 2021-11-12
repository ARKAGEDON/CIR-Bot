import json
import datetime

class Event:
    #Class Event, permet de stocker les données d'un event
    def __init__(self, summary, start, end, description):
        self.summary = summary #Nom de l'event
        self.start = start #Date du début de l'event
        self.end = end #Date de fin de l'event
        self.description = description #Description de l'event

    #Fonction pour afficher le contenu de la classe event
    def show(self):
        print(self.summary,self.start,self.end,self.description)

class Calendar:
    #Class Calendar, permet de stocker une liste d'event
    def __init__(self):
        self.liste = [] #Liste d'event

    #Fonction pour clear le fichier json (admin only)
    def clear(self):
        #Clear le fichier json
        print("Fichier json cleared")

    #Fonction pour ajouter un event dans le fichier json
    def addEvent(self,Event):
        #Conversion des dates en string
        Event.start = Event.start.strftime("%m/%d/%Y")
        Event.end = Event.end.strftime("%m/%d/%Y")
        #Ouverture du fichier json
        with open('data.json', 'r+') as file:
            file_data = json.load(file)
            #Ajout des données dans un dictionnaire
            file_data["Calendar"].append({
                'summary': Event.summary,
                'start': Event.start,
                'end': Event.end,
                'description': Event.description
            })
            file.seek(0)
            #Ajout des données dans le fichier json
            json.dump(file_data, file,  sort_keys=True, ensure_ascii=False, indent=4)

    #Fonction pour récupérer la liste d'event dans le fichier json
    def get(self,start,end):
        #On clear la liste pour avoir une nouvelle liste vide à retourner
        self.liste.clear()
        #Ouverture du fichier json
        with open('data.json', 'r') as openfile:
            json_object = json.load(openfile)
            #Récupération de chaque event du fichier event
            for i in json_object['Calendar']:
                #Récupération de la date de départ
                data_start = datetime.datetime.strptime(i['start'], "%m/%d/%Y").date()
                #Récupération de la date de fin
                data_end = datetime.datetime.strptime(i['end'], "%m/%d/%Y").date()
                #Comparaison pour vérifier que la date est bien comprise dans l'intervalle donnée
                if ((data_start >= start and data_start <= end) or (data_end >= start and data_end <= end)):
                    #Ajout des event dans la liste du calendar
                    self.liste.append(Event(i['summary'], i['start'], i['end'], i['description']))
        #On retourne la liste des events qui sont dans l'intervalle
        return self.liste

