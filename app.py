import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("CryptoMood : Sentiment analysis of tweets about cryptocurrencies")

# Charge les données
tweets_df = pd.read_csv("tweets_with_sentiment.csv")

# Affiche les tweets et leur sentiment
st.subheader("Latest tweets analyzed")
for _, row in tweets_df.iterrows():
    st.write(f"**{row['User']}** ({row['Date']}):")
    st.write(f"- *{row['Tweet']}*")
    st.write(f"🔹 Sentiment : **{row['Sentiment']}**")
    st.write("---")

# Graphique de répartition des sentiments
st.subheader("Sentiment distribution")
sentiment_counts = tweets_df["Sentiment"].value_counts()
fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Statistiques
st.subheader("Sentiment statistics")
st.write(tweets_df["Sentiment"].value_counts())
