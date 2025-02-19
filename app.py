# importy bibliotek
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# odczytanie pliku csv oraz nadanie tytułu aplikacji
df=pd.read_csv("35__welcome_survey_cleaned.csv", sep=";")
st.title(":computer: Ankieta zapoznawcza")

# dodanie tekstu i lini oddzielajacej
st.markdown("""
##### Poznaj swój zespoł w najdrobniejszych szczegółach! 
 Sprawdź, czym się interesują, w jakich branżach pracują i jakie mają motywacje do ciągłego rozwoju. Odkryj, czy są bardziej kociarzami czy miłośnikami psów, a także czy sięgają po słodką czy słoną przekąskę w przerwie od pracy. 
""") 
st.write("---")

# wyswietlenie metric podzial na słodki i słony
st.markdown("""##### Na początek najważniejsze:spoon:""" )
c1,c2 = st.columns(2)
with c1:
    st.metric("Słodkożercy", len(df[df["sweet_or_salty"] == "sweet"]))
with c2:
    st.metric("Słonożercy", len(df[df["sweet_or_salty"] == "salty"]))
st.write("---")


# wykres dla wieku
age = df['age']
#licznie unikalnych wartośći
age_count=df["age"].value_counts().reset_index()
age_count.columns=['age','count']
fig=px.bar(
    age_count,
    x='age',
    y='count',
    hover_data={'count': True},
    labels={'age':'Wiek','count':'Liczba osób'},
    title=('Wiek uczestników')
)
fig.update_traces(marker_color='#FFA500')  
st.plotly_chart(fig)
st.write("---")

# wykres hobby w zależności od branży
hobbies = {
    'Sztuka': 'hobby_art',
    'Książki': 'hobby_books',
    'Filmy': 'hobby_movies',
    'Inne': 'hobby_other',
    'Sport': 'hobby_sport',
    'Gry wideo': 'hobby_video_games'
}
# dodanie pola wyboru
selected_hobby = st.selectbox('Wybierz hobby', list(hobbies.keys()))

hobby_column = hobbies[selected_hobby] #W rezultacie 'hobby_column' będzie zawierać hobby, które zostało wybrane jako 'selected_hobby'
hobby_counts = df.groupby('industry')[hobby_column].sum().reset_index() #za pomocą metody 'groupby' dataframe 'df' jest grupowany według kolumny 'industry'.
#Następnie, dla każdej grupy, kod sumuje wartości w kolumnie 'hobby_column'.
# wykres
fig = px.bar(
    hobby_counts, 
    x='industry', 
    y=hobby_column, 
    labels={'industry':'Branża',hobby_column: 'Liczba osób'}, 
    title=f'Liczba osób z branży z hobby: {selected_hobby}')
fig.update_traces(marker_color='#B22222')  #zmiana koloru
st.plotly_chart(fig)
st.write("---")


# dodanie pola wyboru dla ulubione zwierzę
animal = ["Psy","Koty","Inne", "Brak ulubionych"]
selected_animal = st.selectbox("Wybierz zwierzę",animal)
filtered_data = df[df['fav_animals'] == selected_animal]#Tworzy się nowy DataFrame, 
#zawierający tylko te wiersze z oryginalnego df, gdzie wartość kolumny 'fav_animals' jest taka sama jak wartość 'selected_animal'

gender_counts = filtered_data['age'].value_counts().reset_index() #Z ramki danych 'filtered_data' zlicza się wystąpienia różnych wartości w kolumnie 'age' 
#używając metody 'value_counts'. Wynik jest potem resetowany do standardowej numerowanej formy za pomocą metody 'reset_index'.
gender_counts.columns = ['age', 'count']
# wykres
fig = px.bar(
    gender_counts, 
    x='age', 
    y='count', 
    labels={'age': 'Wiek', 'count': 'Liczba osób'}, 
    title=f'Liczba osób, które wybrały ulubione zwierzę: {selected_animal}'
)
fig.update_traces(marker_color='#228B22')
st.plotly_chart(fig)
st.write("---")


# grupowanie po branży i lata doświadczenia by narysować wykres
years_counts = df.groupby(['industry','years_of_experience']).size().reset_index(name='count') #sum()

fig = px.bar(
    years_counts, 
    x='industry',
    y='count', 
    color='years_of_experience',  # Kolorowanie w zależności od lat doświadczenia, 
    labels={'industry':'Branża','count':'Liczba osob','years_of_experience': 'Lata doswiadczenia'}, 
    title=f'Lata doświadczenia w branży')
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)
st.write("---")


# zmiana nazw i dodanie bocznego pola wyboru
motivation = {
    "Kariera":"motivation_career",
    "Wyzwania":"motivation_challenges",
    "Kreatywność i innowacje":"motivation_creativity_and_innovation",
    "Pieniądze i praca":"motivation_money_and_job",
    "Rozwój osobisty":"motivation_personal_growth",
    "Praca zdalna":"motivation_remote"
}
selected_motivation = st.selectbox('Wybierz motywację', list(motivation.keys()))

motivation_column = motivation[selected_motivation] #Po wybraniu przez użytkownika jednej z motywacji, używamy tej motywacji jako klucza do 
#wyodrębnienia odpowiedniej kolumny z słownika motivation. Zapisujemy tę kolumnę w zmiennej motivation_column.
motivation_counts = df.groupby('industry')[motivation_column].sum().reset_index()

fig = px.bar(
    motivation_counts, 
    x='industry', 
    y=motivation_column, 
    labels={'industry':'Branża',motivation_column: 'Liczba osób'},
    title=f'Liczba osób z branży z motywacją: {selected_motivation}')
fig.update_traces(marker_color='#B8860B')
st.plotly_chart(fig)
st.write("---")


# określenie nowego df
pref_df=[
    "learning_pref_books",
    "learning_pref_chatgpt",
    "learning_pref_offline_courses",
    "learning_pref_online_courses",
    "learning_pref_personal_projects",
    "learning_pref_teaching",
    "learning_pref_teamwork",
    "learning_pref_workshops",
]
study_pref_df = df[pref_df]
# zmiana nazw - mapowanie!!
column_names = {
    "learning_pref_books": "Książki",
    "learning_pref_chatgpt": "ChatGPT",
    "learning_pref_offline_courses": "Offline Kursy",
    "learning_pref_online_courses": "Online Kursy",
    "learning_pref_personal_projects": "Projekty Osobiste",
    "learning_pref_teaching": "Nauczanie",
    "learning_pref_teamwork": "Praca zespołowa",
    "learning_pref_workshops": "Warsztaty"
}
study_pref_df = study_pref_df.rename(columns=column_names)

# Obliczanie średniej tylko dla kolumn z preferencjami (nie dla innych danych w df)
preference_columns = list(column_names.values())  # Lista nowych nazw kolumn
mean_preferences = study_pref_df[preference_columns].mean().reset_index()
mean_preferences.columns = ['Learning Preference', 'Average Intensity']


# wykres słupkowy
fig = px.bar(
    mean_preferences,
    x='Learning Preference',
    y='Average Intensity',
    title='Średnia preferencji sposobów nauki',
    labels={'Learning Preference':'Sposoby nauki','Average Intensity': 'Średnia Intensywność'},
    color='Learning Preference',  # Używanie koloru do oznaczenia różnych preferencji
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)
st.write("---")


st.markdown("#### Tak to się rozkłada")
# kolumny z iloscia uczestnikow z podzialem na kobiety i mezczyzni
c3,c4,c5 = st.columns(3)
with c3:
    st.metric('Wszyscy respondenci',(len(df)))
with c4:
    st.metric('Kobiety', len(df[df['gender']==1]))
with c5:
    st.metric('Mężczyźni',len(df[df['gender']==0]))
st.write("---")



# Tworzenie poziomego wykresu słupkowego za pomocą Plotly
df['gender'] = df['gender'].map({0: 'Mężczyźni', 1: 'Kobiety'}) #mapowanie 
fig = px.histogram(
    df, 
    x='industry', 
    color='gender', 
    barmode='group',
    labels={'industry':'Branża','count':'Liczba osób'},
    title=f'Liczba osób w każdej branży, podzielonych według płci',
    color_discrete_map={'Mężczyźni': '#800080', 'Kobiety': 'pink'})

fig.update_yaxes(title_text='Licza osób') #nazwa count nie zmienila sie uzywajac labels, wiec to jest kolejna z mozliwosci
# podobnie zmiana tytuly legendy
fig.update_legends(title_text='Płeć')
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)
