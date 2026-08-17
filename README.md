# CryptoMood

Sentiment analysis of cryptocurrency-related tweets, cross-referenced with Bitcoin market data, to detect divergences between social media sentiment and actual price movement.

## Description

CryptoMood collects recent tweets mentioning Bitcoin, analyzes their sentiment (positive / negative / neutral) using the Mistral API, then compares the aggregated sentiment to price and RSI (Relative Strength Index) movements over the same period. The goal is to identify potential divergences between social sentiment and actual price behavior, a signal sometimes used in technical analysis.

An interactive dashboard (Streamlit) lets you visualize the analyzed tweets and the sentiment distribution.

## Project Structure

```
.
├── app.py                      # Streamlit interface
├── src/
│   ├── fetch_tweets.py         # Tweet collection via the Twitter API (Tweepy)
│   ├── analyze_sentiment.py    # Sentiment analysis via the Mistral API
│   └── analyze_market.py       # Bitcoin market data (CoinGecko) + RSI calculation + divergence detection
├── data/
│   ├── tweets_bitcoin.csv              # Raw tweets
│   ├── tweets_with_sentiment.csv       # Tweets + sentiment
│   └── tweets_with_market_analysis.csv # Tweets + sentiment + market data
├── requirements.txt
└── README.md
```

## Pipeline

1. fetch_tweets.py : retrieves recent tweets mentioning Bitcoin via the Twitter API v2.
2. analyze_sentiments.py : classifies each tweet as positive, negative, or neutral using the Mistral API.
3. analyze_market.py : retrieves Bitcoin price and RSI over the relevant period (CoinGecko + pandas_ta), aggregates sentiment by hour, and detects divergences between sentiment and price.
4. app.py : displays the results in a Streamlit dashboard (tweet list, sentiment distribution).

## Installation

1. Clone the repo:

```bash
git clone https://github.com/emmie-vinet/cryptomood.git
cd cryptomood
```

1. Create a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create a `.env` file at the root with your API keys:

```
TWITTER_BEARER_TOKEN=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
MISTRAL_API_KEY=...
COINGECKO_API_KEY=...
```

## Usage

Run the pipeline in order:

```bash
python src/fetch_tweets.py
python src/analyze_sentiment.py
python src/analyze_market.py
```

Then launch the dashboard:

```bash
streamlit run app.py
```

## Tech Stack

- **Python** (pandas, pandas_ta)
- **Tweepy** : Twitter API
- **Mistral AI** : sentiment classification
- **CoinGecko API** : Bitcoin market data
- **Streamlit** : user interface
- **Matplotlib** : data visualization

## Possible Improvements

- Extend the analysis to other cryptocurrencies
- Automate continuous data collection (scheduler)
- Backtest the detected divergence signals