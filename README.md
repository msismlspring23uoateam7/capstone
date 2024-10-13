AgentLite POC - Capstone Project

This repository contains the proof of concept (POC) implementation for AgentLite, a fraud detection system that leverages advanced machine learning techniques and large language models (LLMs) for detecting anomalies in credit card transactions. This project demonstrates how AI agents can interact, process data, generate insights, and provide visualizations through a streamlined workflow.

Table of Contents

	•	Project Overview
	•	Features
	•	Requirements
	•	Installation
	•	Usage
	•	1. Data Processing
	•	2. LLM Insights
	•	3. Visualization
	•	Custom Visualizations
	•	Testing
	•	Contributing
	•	License

Project Overview

The AgentLite POC project aims to build an intelligent framework that can automatically detect fraudulent transactions in credit card datasets. The system performs data preprocessing, provides insights from LLMs, and generates interactive visualizations based on user inputs.

The key components are:

	•	DataProcessingAgent: Preprocesses the data and prepares it for analysis.
	•	LLMProcessor: Provides insights using large language models.
	•	VisualizationAgent: Visualizes data and insights in different forms such as histograms, correlation matrices, and more.
	•	Streamlit App: A user interface where users can upload datasets, receive insights, and interactively generate visualizations.

Features

	•	Automatic data preprocessing for fraud detection
	•	Generation of insights using LLMs (OpenAI API)
	•	Interactive data visualizations
	•	Support for custom visualizations based on user input
	•	User-friendly interface via Streamlit

Requirements

	•	Python 3.8+
	•	Streamlit for the web interface
	•	OpenAI API for generating insights using LLMs
	•	Pandas, NumPy, and Matplotlib for data manipulation and visualization
	•	Seaborn for advanced data visualizations



** Installation and Execution**

	•	pip install -e agentlite
	•	pip install -r requirements.txt
	•	export OPENAI_API_KEY=<INSERT YOUR OpenAI API KEY HERE>
	•	streamlit run agentlite_finance/streamlit_app.py