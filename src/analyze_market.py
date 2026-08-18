import pandas as pd
import requests
import pandas_ta as ta
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# 1. Charger la clé API et les tweets
load_dotenv()
api_key = os.getenv('COINGECKO_API_KEY')
tweets = pd.read_csv('tweets_with_sentiment.csv', parse_dates=['Date'])
tweets = tweets.rename(columns={'Date': 'date'})
tweets = tweets.sort_values('date')

# 2. Calculer le score de sentiment moyen par heure
sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
tweets['sentiment_score'] = tweets['Sentiment'].map(sentiment_map)

# Normaliser les scores entre 0 et 1
min_score = tweets['sentiment_score'].min()
max_score = tweets['sentiment_score'].max()
tweets['sentiment_score'] = (tweets['sentiment_score'] - min_score) / (max_score - min_score)

# Regrouper par heure 
tweets['hour'] = tweets['date'].dt.floor('h')  
daily_sentiment = tweets.groupby('hour')['sentiment_score'].mean().reset_index()
daily_sentiment = daily_sentiment.rename(columns={'hour': 'date'})
daily_sentiment.set_index('date', inplace=True)

# 3. Initialiser le DataFrame pour stocker les résultats
results = pd.DataFrame(columns=['date', 'sentiment_score', 'price', 'price_change_percent', 'rsi', 'divergence'])

# 4. Fonctions pour récupérer les données
def get_historical_data(start_date, end_date):
    if not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())
    if not isinstance(end_date, datetime):
        end_date = datetime.combine(end_date, datetime.min.time())

    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': start_timestamp,
        'to': end_timestamp,
        'x_cg_demo_api_key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms', utc=True)  # Forcer UTC
    prices.set_index('date', inplace=True)

    # Calculer le RSI sur les données horaires
    prices['rsi'] = ta.rsi(prices['price'], length=14)
    return prices

def get_price_at_time(historical_data, target_time):
    # Convertir target_time en UTC pour correspondre à historical_data
    if target_time.tzinfo is None:
        target_time = target_time.tz_localize('UTC')
    else:
        target_time = target_time.tz_convert('UTC')

    # Trouver la donnée la plus proche de l'heure cible
    idx = historical_data.index.get_indexer([target_time], method='nearest')[0]
    return historical_data.iloc[idx]

# 5. Récupérer les dates uniques (à l'heure près)
unique_dates = daily_sentiment.index.unique()

# 6. Récupérer les données historiques une seule fois pour toute la période
start_date = unique_dates.min() - timedelta(days=14)
end_date = unique_dates.max()
historical_data = get_historical_data(start_date, end_date)

# 7. Analyser chaque heure
for date in unique_dates:
    print(f"\nTraitement de l'heure : {date}")

    # Récupérer les données pour l'heure cible (la plus proche)
    try:
        current_data = get_price_at_time(historical_data, date)
        current_price = current_data['price']
        current_rsi = current_data['rsi']
    except (IndexError, TypeError) as e:
        print(f"Aucune donnée historique proche de l'heure {date}: {e}")
        current_price = None
        current_rsi = None

    # Récupérer les données pour l'heure précédente
    previous_hour = date - timedelta(hours=1)
    try:
        previous_data = get_price_at_time(historical_data, previous_hour)
        previous_price = previous_data['price']
    except (IndexError, TypeError) as e:
        print(f"Aucune donnée historique proche de l'heure {previous_hour}: {e}")
        previous_price = None

    # Calculer le changement de prix par rapport à l'heure précédente
    price_change_percent = ((current_price - previous_price) / previous_price) * 100 if (current_price and previous_price) else None

    # Récupérer le score de sentiment pour cette heure
    sentiment_score = daily_sentiment.loc[date, 'sentiment_score']

    # Détecter les divergences
    divergence = 'none'
    if current_rsi is not None and current_price is not None and previous_price is not None:
        if sentiment_score > 0.7 and price_change_percent is not None and price_change_percent < 0 and current_rsi > 70:
            divergence = 'positive_divergence'
        elif sentiment_score < 0.3 and price_change_percent is not None and price_change_percent > 0 and current_rsi < 30:
            divergence = 'negative_divergence'

    # Ajouter les résultats
    results.loc[len(results)] = {
        'date': date,
        'sentiment_score': sentiment_score,
        'price': current_price,
        'price_change_percent': price_change_percent,
        'rsi': current_rsi,
        'divergence': divergence
    }

# 8. Sauvegarder le fichier CSV
results.to_csv("tweets_with_market_analysis.csv", index=False)
print(f"Analyse terminée. Résultats enregistrés dans tweets_with_market_analysis.csv")
