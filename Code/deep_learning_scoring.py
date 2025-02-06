from transformers import pipeline
import time


def compute_negativity(L):
    '''
    Return the ESG score of a company : negative scores are bad, positive score are good
    input : L, a list of strings
    output : a list of tuple (negative/positive/neutral,score)
    '''
    pipe = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
    results = pipe(L)

    scores = []
    for result in results:
        if result['label']=='positive':
            scores.append(result['score'])
        elif result['label']=='negative':
            scores.append(-1*result['score'])
        else:
            scores.append(0)    # neutral score

    return(scores)

def compute_ESG_bool(L):
    '''
    Return if the text is related to ESG or not
    input : a list of strings
    output : a list of TRUE/FALSE, TRUE if the text is ESG related, FALSE if it is not
    '''
    pipe = pipeline("text-classification", model="yiyanghkust/finbert-esg")
    results = pipe(L)
    scores = []

    for result in results:
        if result['label']=='None':
            scores.append(False)
        else:
            scores.append(True)
    return(scores)

def compute_ratings(L):
    '''
    compute the esg ratings of a list, as they are used in the app
    '''
    esg_bool = compute_ESG_bool(L)
    usefull_texts = [L[k] for k in range(len(L)) if esg_bool[k]]
    print("esg_bool",esg_bool)
    print("usefull_texts=",usefull_texts,len(usefull_texts))
    scored_texts = compute_negativity(usefull_texts)
    print("ici",scored_texts)
    scores = []
    for k in range(len(L)):
        if esg_bool[k]==False:
            scores.append(0)
        else:
            print("scores_texts=",scored_texts)
            scores.append(scored_texts[0])
            scored_texts = scored_texts[1:]
    return(scores)

# pipe_esg = pipeline("text-classification", model="yiyanghkust/finbert-esg")
# pipe_sentiment = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

#texts = ["j'aime les pates","kill all jews","je sauve les animaux et je plante des arbres","Je suis fatigué"]
text = ['''En 2023, Amazon a non seulement atteint son objectif d'utilisation d'énergie renouvelable avec sept ans d'avance, mais a également lancé de nouvelles ressources pour aider ses fournisseurs à décarboniser leurs opérations, apprend-on du rapport annuel ESG du géant américain de l’e-commerce.


Amazon a désormais des parcs éoliens et solaires aux quatre coins du globe
Amazon utilise désormais uniquement de l’énergie renouvelable
Le 10 juillet 2024, Amazon a annoncé avoir réussi à couvrir 100% de sa consommation électrique globale avec des achats d'énergie renouvelable, atteignant cet objectif sept ans avant la date limite initialement fixée pour 2030. Cette réalisation est le résultat d'une combinaison de contrats d'achat d'énergie (PPA), de tarifs préférentiels et de production sur site. Amazon est ainsi devenu le plus grand acheteur d'énergie renouvelable au monde, soutenant plus de 500 projets d'énergie renouvelable dans 27 pays.

Cette approche proactive inclut des projets d'envergure tels que des parcs solaires et éoliens en Inde, en Grèce, au Japon, en Afrique du Sud, en Indonésie, en Chine, aux États-Unis et aux Pays-Bas. Ces initiatives permettent non seulement de réduire les émissions directes (Scope 2) de l'entreprise, mais aussi de soutenir les réseaux énergétiques locaux en diversifiant les sources d'énergie.

Cependant, la nt sur la décarbonisation de sa chaîne d'approvisionnement, qui représente la majeure partie de son empreinte carbone totale (Scope 3). En 2023, Amazon a généré près de 52 millions de tonnes d'émissions de Scope 3, comparé à environ 17 millions de tonnes provenant de ses opérations et achats d'électricité.
Pour aider ses fournisseurs, en particulier les PME, à surmonter les obstacles à la décarbonisation, Amazon a lancé la plateforme « Sustainability Exchange ». Ce centre de ressources en ligne offre des directives, des modèles scientifiques et des outils pour mesurer les émissions, développer des stratégies d'achat d'énergie renouvelable, améliorer l'efficacité énergétique des bâtiments et débuter des initiatives de gestion de l'eau.

Kara Hurst, vice-présidente pour la durabilité mondiale chez Amazon, a exprimé le souhait que cette plateforme devienne un outil largement adopté par les entreprises de toutes tailles pour avancer dans leur parcours de durabilité. Les fournisseurs les plus émetteurs devront fournir des plans de décarbonisation et démontrer des progrès annuels réels.
''']

# text = ["j'aime les pates","kill all jews","je sauve les animaux et je plante des arbres","Je suis fatigué"]
# start = time.time()
print(compute_ratings(text))
# print(pipe_esg(texts))
# print(pipe_sentiment(texts))
# print(time.time()-start)
