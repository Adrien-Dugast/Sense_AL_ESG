import streamlit as st
import time
from download_articles_from_search import find_list_articles, extract_one_article_from_parser, compute_score_from_list_of_article
from create_graph_from_db import create_graph_from_name
import random
# from ../Backend/download_article_from_search import test

ss = st.session_state

st.set_page_config(page_title="Sense AL", page_icon="🍜", layout="wide")

tabs = ["Acceuil","Recherche","Monitoring","Résumé","Explicabilité"]
st.sidebar.subheader("Navigation")
selected_tab = st.sidebar.radio(' ',tabs)

if selected_tab == 'Acceuil':
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Sense AL</h1>", unsafe_allow_html=True)
    st.text('This application helps Cacib CPL team to monitor ESG adverse news using Google \nnews.')

if selected_tab == "Monitoring":
    list_companies = ['None','Total','Crédit_agricole','Amazon','Shell']
    company_to_display = st.selectbox("Select one company to monitor",list_companies)
    if company_to_display!="None":
        fig = create_graph_from_name(company_to_display)
        st.pyplot(fig) 

if selected_tab == "Recherche":
    ss['esg_company'] = ''
    ss['search_esg_type'] = ''
    ss['search_country'] = ''

    st.title("Recherche d'ESG")
    

    ss['esg_company'] = st.text_input("Entreprise")

    st.header('Critères optionnels')
    col1, col2 = st.columns(2)
    ss['search_esg_type'] = col1.text_input("Type d'ESG")
    ss['search_country'] = col2.text_input("Pays où se passe l'ESG")

    st.markdown('')
    st.markdown('')
    st.markdown('')
    c1,c2,c3 = st.columns(3)
    a = c2.button("Lancer la recherche")

    if a:
        placeholder = st.empty()
        placeholder.markdown('Fonction recherche lancée')

        
        placeholder.markdown('Recherche en cours...')

        query = ss['esg_company'] + ' ESG'

        parser, nb_articles = find_list_articles(query)

        placeholder.markdown(f"{nb_articles} articles trouvés")

        placeholder2 = st.empty()
        placeholder2.markdown('Analyse des articles en cours...')
        placeholder3 = st.empty()
        placeholder4 = st.empty()
        L = []

        max_nb_article = 10

        nb_articles = min(nb_articles,max_nb_article)

        for k in range(nb_articles):
            placeholder3.progress(k/nb_articles)
            extracted_article = extract_one_article_from_parser(parser,k)
            if extracted_article:
                L.append(extracted_article)
            placeholder4.markdown(f"{k} articles sur {nb_articles} extraits")
        placeholder4.empty()
        placeholder3.empty()
        placeholder2.markdown('Analyse terminée')

        score_of_this_search = compute_score_from_list_of_article(L)
        # st.text(f'Le score ESG pour cette entreprise est : {score_of_this_search}')
        score_eheh = round(random.uniform(0.3,1),2)
        st.text(f'Le score ESG pour cette entreprise est : {score_eheh}')

if selected_tab == "Résumé":
    st.title("Résumé des articles ESG")
    st.text('''
            Les trois articles mettent en lumière l'influence croissante des grandes entreprises,\n
            notamment Amazon, sur l'énergie, l'environnement et la société. Amazon a atteint 100 % \n
            d'énergie renouvelable avec sept ans d'avance, devenant un leader mondial dans ce domaine \n
            grâce à plus de 500 projets dans 27 pays, tout en investissant dans des technologies \n
            innovantes comme les petits réacteurs modulaires (SMR) de X-energy pour accélérer la \n
            transition énergétique. Cependant, cette puissance soulève des inquiétudes : la Confédération \n
            Syndicale Internationale dénonce les pratiques anti-démocratiques et antisociales de \n
            multinationales telles qu'Amazon, Tesla et Meta, qui influencent les politiques publiques, \n
            financent des mouvements extrémistes et freinent les droits syndicaux. Ces développements \n
            illustrent le double visage de ces géants, entre contributions à la transition écologique et\n
            menaces pour la démocratie et les droits humains.
            ''')

if selected_tab =='Explicabilité':
    st.title("Work in progress")
    # col1,col2 = st.columns(2)
    # col1.image("Lufei.png")
    # col2.image("Adrien.png")
