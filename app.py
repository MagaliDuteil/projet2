# Importation des bibliothèques
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Connection aux fichier csv
df_nyc = pd.read_csv("C:/Users/Administrateur/Desktop/projet data analyst/cleaned_new_york_city.csv")
df_nyc = pd.DataFrame(df_nyc) # New York City

df_wash = pd.read_csv("C:/Users/Administrateur/Desktop/projet data analyst/cleaned_washington_city.csv")
df_wash = pd.DataFrame(df_wash) # Washington

df_chi = pd.read_csv("C:/Users/Administrateur/Desktop/projet data analyst/cleaned_chicago_city.csv")
df_chi = pd.DataFrame(df_chi) # Chicago


# Convertir au format DateTime
df_nyc['Start Time'] = pd.to_datetime(df_nyc['Start Time'])
df_chi['Start Time'] = pd.to_datetime(df_chi['Start Time'])
df_wash['Start Time'] = pd.to_datetime(df_wash['Start Time'])


def jour_activite_max(data):
    # Convertir la colonne 'Start Time' en datetime
    data['Start Time'] = pd.to_datetime(data['Start Time'], errors='coerce')
    # Extraire le jour de la semaine (0 = Lundi, 1 = Mardi, ..., 6 = Dimanche)
    data['Day of Week'] = data['Start Time'].dt.dayofweek
    # Trouver le jour avec le plus d'activité
    count = data['Day of Week'].value_counts()
    jour_max = count.idxmax() if not count.empty else None
    
    return jour_max

def heure_demarrage_courante(data):
    # Convertir la colonne 'Start Time' en datetime
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    # Extraire l'heure de démarrage
    data['Hour'] = data['Start Time'].dt.hour
    # Trouver l'heure de démarrage la plus courante
    count = data['Hour'].value_counts()
    heure_courante = count.idxmax() if not count.empty else None
    return heure_courante

def duree_voyage_moyenne(data):
    # Calculate trip duration in seconds
    data['Trip Duration'] = pd.to_numeric(data['Trip Duration'], errors='coerce')
    
    # Drop rows with missing trip duration values
    data = data.dropna(subset=['Trip Duration'])
    
    # Calculate average trip duration in seconds
    mean_duration = data['Trip Duration'].mean()
    
    # Convert average duration to minutes
    mean_duration_minutes = mean_duration / 60
    
    return round(mean_duration_minutes, 2)

def total_categorie_user(data):
    # Compter les occurrences de chaque catégorie
    total_categorie = data['User Type'].value_counts()
    return total_categorie

def nombre_femmes_hommes(data):
    # Compter les occurrences de chaque sexe
    data['Gender'] = data['Gender'].replace({0: 'femme', 1: 'homme', 2: 'autre'})
    nombre_sexe = data['Gender'].value_counts()
    return nombre_sexe

def annee_naissance(data):
    # Supprimer les lignes avec des valeurs manquantes
    data = data.dropna(subset=['Birth Year'])
    # Convertir la colonne 'Birth Year' en entier
    data['Birth Year'] = data['Birth Year'].astype(int)
    # Calculer l'année la plus ancienne, la plus récente et la plus courante
    annee_ancienne = data['Birth Year'].min()
    annee_recente = data['Birth Year'].max()
    annee_courante = data['Birth Year'].value_counts()
    annee_courante = data['Birth Year'].value_counts().sort_values(ascending=False).index[0]
        
    return annee_ancienne, annee_recente, annee_courante

def afficher_donnees(data):
    print(data.head(10))

@app.route('/recherche_city', methods=["GET", "POST"])
def recherche_city ():
    name = ""
    month = ""
    if request.method == "POST":
        name = request.form.get('name_city')
        month = request.form.get('month')
        if name == 'New York City':
            data = df_nyc
            # Convertir la colonne 'Start Time' en datetime
            data['Start Time'] = pd.to_datetime(data['Start Time'])

            # Extraire le mois au format "mm"
            data['Month'] = data['Start Time'].dt.strftime('%m')
        
            # Filtrer les données pour le mois sélectionné
            if month:
                data = data[data['Month'] == month]
                jour_max = jour_activite_max(data)
                heure_courante = heure_demarrage_courante(data)
                duree_moyenne = duree_voyage_moyenne(data)
                total_categorie = total_categorie_user(data)
                nombre_sexe = nombre_femmes_hommes(data)
                annee_ancienne, annee_recente, annee_courante = annee_naissance(data)
            # Traitement des données filtrées...
            return render_template('city_flask.html', jour_max=jour_max, heure_courante=heure_courante, duree_moyenne=duree_moyenne, total_categorie=total_categorie, nombre_sexe=nombre_sexe, annee_ancienne=annee_ancienne, annee_recente=annee_recente, annee_courante=annee_courante)
        elif name == 'Chicago':
            data = df_chi
            # Convertir la colonne 'Start Time' en datetime
            data['Start Time'] = pd.to_datetime(data['Start Time'])

            # Extraire le mois au format "mm"
            data['Month'] = data['Start Time'].dt.strftime('%m')
        
            # Filtrer les données pour le mois sélectionné
            if month:
                data = data[data['Month'] == month]
                jour_max = jour_activite_max(data)
                heure_courante = heure_demarrage_courante(data)
                duree_moyenne = duree_voyage_moyenne(data)
                total_categorie = total_categorie_user(data)
                nombre_sexe = nombre_femmes_hommes(data)
                annee_ancienne, annee_recente, annee_courante = annee_naissance(data)
            # Traitement des données filtrées...
            return render_template('city_flask.html', jour_max=jour_max, heure_courante=heure_courante, duree_moyenne=duree_moyenne, total_categorie=total_categorie, nombre_sexe=nombre_sexe, annee_ancienne=annee_ancienne, annee_recente=annee_recente, annee_courante=annee_courante)
        elif name == 'Washington':
            data = df_wash   
            # Convertir la colonne 'Start Time' en datetime
            data['Start Time'] = pd.to_datetime(data['Start Time'])

            # Extraire le mois au format "mm"
            data['Month'] = data['Start Time'].dt.strftime('%m')
        
            # Filtrer les données pour le mois sélectionné
            if month:
                data = data[data['Month'] == month]
                jour_max = jour_activite_max(data)
                heure_courante = heure_demarrage_courante(data)
                duree_moyenne = duree_voyage_moyenne(data)
                total_categorie = total_categorie_user(data)
                nombre_sexe = nombre_femmes_hommes(data)
                annee_ancienne, annee_recente, annee_courante = annee_naissance(data)
            # Traitement des données filtrées...
            return render_template('city_flask.html', jour_max=jour_max, heure_courante=heure_courante, duree_moyenne=duree_moyenne, total_categorie=total_categorie, nombre_sexe=nombre_sexe, annee_ancienne=annee_ancienne, annee_recente=annee_recente, annee_courante=annee_courante)
        return render_template('city_flask.html', name=name, month=month)
    return render_template('city_flask.html', name=name, month=month)
  
if __name__ == "__main__":
    app.run(debug=True) 