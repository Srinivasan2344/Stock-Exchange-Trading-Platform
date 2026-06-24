# AI-Powered Stock Exchange Trading Platform

## Overview

An AI-powered stock trading platform that provides stock price prediction, trading signals, sentiment analysis, portfolio analytics, fraud detection, and real-time monitoring.

## Features

* Stock Price Prediction using XGBoost
* AI Trading Signal Engine
* Market Sentiment Analysis
* Portfolio Risk Analytics
* Fraud Detection System
* Model Drift Monitoring
* Automated Model Retraining
* Kafka Real-Time Streaming
* FastAPI Backend
* PostgreSQL Database
* Streamlit Dashboard

## Technologies

* Python
* FastAPI
* Streamlit
* PostgreSQL
* XGBoost
* Scikit-learn
* TextBlob
* Kafka
* Docker
* Pandas
* NumPy
* SQLAlchemy

## Project Structure

src/
├── api.py
├── prediction.py
├── trading_signal.py
├── sentiment_analysis.py
├── news_sentiment.py
├── fraud_detection.py
├── backtesting.py
├── retrain_model.py
├── model_monitoring.py
├── kafka_producer.py
├── kafka_consumer.py

## Run Dashboard

streamlit run dashboard.py

## Run API

uvicorn src.api:app --reload

## Run Kafka

python src/kafka_consumer.py
python src/kafka_producer.py
