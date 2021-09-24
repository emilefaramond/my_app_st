import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from PIL import Image
import random
from datetime import datetime

start = datetime.now()
data_file = open('file.txt', 'w')
for seq_id in range(0, 1000000):
        num_val=random.random()
        line="%i %f\n" % (seq_id, num_val)
        data_file.write(line)

end = datetime.now()
st.write("elapsed time %s" % (end - start))

#fonction qui permet d'afficher une image plutot que de coder en dur
def afficher_une_image(file,titre) : 
    image = Image.open(file)
    return st.image(image, caption= titre)

#fonction qui permet de lire un fichier plutot que de coder en dur
@st.cache
def lire_csv(file_path) : 
    df = pd.read_csv(file_path,delimiter = ',')
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    df['dom'] = df['Date/Time'].map(get_dom)
    df['weekday']= df['Date/Time'].map(get_weekday)
    return df

#fonction qui retorune le jour du mois
def get_dom(dt):
   return dt.day 
#fonction qui retourne le jour de la sem
def get_weekday(dt):
   return dt.weekday() 

#fonction pour ecrire un titre dans st
def give_title(message):
    return st.title(message)
#fonction pour ecrire un header dans st
def give_header(message):
    return st.header(message)
#fonction pour ecrire du texte dans st
def give_text(message):
    return st.text(message)

#fonction qui donne un échentillon du df utilisé
def give_sample_of_dateframe(dateframe):
    return st.write(dateframe.head())


afficher_une_image('uber.jpg', 'Uber board')

df = lire_csv('uber-raw-data-apr14.csv')
st.write(df)


#presentation
give_title('Dashbord de données Uber')
give_header('Nous verrons dans ce dashbord différents suport visuel qui explique certaiines courses uber')
give_text('Voici un echantillon du jeu de données sur lequel nous travaillons')
give_sample_of_dateframe(df)
give_text('Suivi de la performance sur le mois en cours')

#suivre la performance du mois
col1, col2 = st.columns(2)
col1.metric("Jour du mois le plus performant", '29')
col2.metric("Jour de la semaine le plus performant",'Vendredi')
#je vais mettre des variables changeantes ici et pas des variables fixent



#Présentation d'un premier histogramme pour les jours du mois
give_text('Voici un histogramme qui présente la fréquence des courses en fonction du jour du mois')

hist_values_day_month = np.histogram(
    df['dom'], bins=30, range=(0,30))[0]

st.bar_chart(hist_values_day_month)


#Présentation d'un deuxieme histogramme pour les jours de la semaine
give_text('Voici un histogramme qui présente la fréquence des courses en fonction du jour de la semaine')

hist_values_day_week = np.histogram(
    df['dom'], bins=7, range=(0,6))[0]

st.bar_chart(hist_values_day_week)


#ajouter une carte des endroits ou il y a eu des commandes dans le mois
df = df.rename(columns = {'Lon': 'lon', 'Lat': 'lat'})
st.subheader('Carte de toutes les prises en charges du mois')
st.map(df)