import pandas as pd

liste4exos = ['Squat (Barbell)', 'Deadlift (Barbell)', 'Overhead Press (Barbell)', 'Bench Press (Barbell)']

#Read le fichier XLSX
strong_df = pd.read_excel ('gym/raw_data/strong.xlsx')

#Enlever les colonnes inutiles
strong_df = strong_df.drop(columns=['Workout Name', 'Notes', 'RPE', 'Workout Notes', 'Seconds', 'Distance', 'Set Order', 'Duration'])

#Clean colonne date
strong_df["Date"] = strong_df["Date"].astype(str)
strong_df["Date"] = strong_df["Date"].str[:-9]
strong_df["Date"] = pd.to_datetime(strong_df["Date"])

#Remove rows that do not contain OHP, Squat, Bench & Deadlift
strong_df = strong_df[strong_df['Exercise Name'].isin(liste4exos)]


#Calculer OneRM pour chaque série et arrondir à l'unité
strong_df["OneRM"] = (strong_df['Weight'] * 36)/(37 - strong_df["Reps"])
strong_df["OneRM"] = strong_df["OneRM"].round(decimals=0)


#Merge OneRM with the same date
strong_df = strong_df.astype(str)
strong_df = strong_df.groupby(['Date', 'Exercise Name'])['OneRM'].apply(', '.join).reset_index()
strong_df_dates = strong_df['Date'].copy()
strong_df = pd.concat([strong_df['Exercise Name'], strong_df['OneRM'].str.split(', ', expand=True)], axis=1)
strong_df = pd.concat([strong_df_dates, strong_df], axis=1)

#Supprimer lorsque plus de 13 valeurs par exercice et par jour
strong_df = strong_df.drop(strong_df.columns[14:29], axis =1)

#Convertir toutes valeurs des OneRM en int
strong_df[[0,1,2,3,4,5,6,7,8,9,10,11]] = strong_df[[0,1,2,3,4,5,6,7,8,9,10,11]].apply(pd.to_numeric)

#Trouver valeur maximale 
strong_df["OneRM"] = strong_df[[2, 3]].max(axis=1)

#Drop les colonnes en trop
strong_df = strong_df.drop(strong_df.columns[2:14], axis =1)

#Exporter en XLSX
strong_df.to_excel('gym/clean_data/clean_strong.xlsx', index=False)

#Line Plot
strong_df.plot.line(x='Date', y='OneRM')
