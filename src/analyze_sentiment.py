from mistralai.client import MistralClient
import pandas as pd
import os
from dotenv import load_dotenv

# Charge les clés API
load_dotenv()

# Initialise le client Mistral
client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

def analyze_sentiment(text):
    """Analyse le sentiment d'un texte avec Mistral et retourne uniquement 'positif', 'négatif' ou 'neutre'."""
    prompt = f"""
    Analyse le sentiment de ce tweet sur une crypto-monnaie.
    Réponds UNIQUEMENT par l'un des trois mots suivants : 'positif', 'négatif', 'neutre'.
    Ne donne aucune explication, aucun commentaire, ni aucun autre mot.
    Tweet : {text}
    """
    response = client.chat(
        model="mistral-tiny",
        messages=[{"role": "user", "content": prompt}]
    )
    # On récupère la réponse et on extrait le premier mot (au cas où)
    sentiment = response.choices[0].message.content.strip().lower()
    # On standardise la réponse pour s'assurer qu'elle est valide
    if "positif" in sentiment:
        return "positive"
    elif "négatif" in sentiment:
        return "negative"
    elif "neutre" in sentiment:
        return "neutral"
    else:
        return "neutre"  # Valeur par défaut si la réponse est inattendue

# Charge les tweets
tweets_df = pd.read_csv("tweets_bitcoin.csv")

# Ajoute une colonne "Sentiment"
tweets_df["Sentiment"] = tweets_df["Tweet"].apply(analyze_sentiment)

# Enregistre les résultats
tweets_df.to_csv("tweets_with_sentiment.csv", index=False)
print("Analyse terminée. Résultats enregistrés dans tweets_with_sentiment.csv")
