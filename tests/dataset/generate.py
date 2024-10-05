import pandas as pd
import random
import os

# Load S&P 500 dataset (assumed CSV file)
df = pd.read_csv('all_stocks_5yr.csv')

# Select a subset of stocks
stocks = df['Name'].unique()

# 1. Stock Performance Questions
def stock_performance_question(stock, date):
    data = df[(df['Name'] == stock) & (df['date'] == date)]
    if not data.empty:
        price = data['close'].values[0]
        return f"What was the closing price of {stock} on {date}?", f"${price:.2f}"
    return None, None

# 2. Comparative Performance Questions
def comparative_performance_question(stock1, stock2, year):
    data1 = df[(df['Name'] == stock1) & (df['date'].str.contains(year))]
    data2 = df[(df['Name'] == stock2) & (df['date'].str.contains(year))]
    if not data1.empty and not data2.empty:
        avg1 = data1['close'].mean()
        avg2 = data2['close'].mean()
        better = stock1 if avg1 > avg2 else stock2
        return f"Which stock performed better in {year}, {stock1} or {stock2}?", f"{better} had a better performance with an average price of ${max(avg1, avg2):.2f}"
    return None, None

# 3. Event-Driven Questions
# Let's assume you have event data (like earnings report dates or major news) in the dataset.
# For simplicity, we'll randomly generate event questions from stock price spikes.

def event_driven_question(stock, event_date, event_type="earnings report"):
    # Fetch stock price around the event date
    pre_event_data = df[(df['Name'] == stock) & (df['date'] == event_date)]
    if not pre_event_data.empty:
        price_before = pre_event_data['close'].values[0]
        # Assuming stock change after 1 day (this can be modified to any time period)
        post_event_data = df[(df['Name'] == stock) & (df['date'] > event_date)].head(1)
        if not post_event_data.empty:
            price_after = post_event_data['close'].values[0]
            change = (price_after - price_before) / price_before * 100
            direction = "rose" if change > 0 else "fell"
            return f"How did {stock}'s stock react after the {event_type} on {event_date}?", f"{stock}'s stock {direction} by {abs(change):.2f}% the next day."
    return None, None

# 4. Time-Series Questions
def time_series_question(stock, start_date, end_date):
    data = df[(df['Name'] == stock) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    if not data.empty:
        avg_price = data['close'].mean()
        max_price = data['close'].max()
        min_price = data['close'].min()
        return (f"What was the average, highest, and lowest stock price of {stock} from {start_date} to {end_date}?",
                f"Average: ${avg_price:.2f}, Highest: ${max_price:.2f}, Lowest: ${min_price:.2f}")
    return None, None

evaluation_questions = dict()

# Generate 100 random questions (25 from each category)
questions_answers = []
# Stock Performance Questions (25)
for _ in range(25):
    stock = random.choice(stocks)
    date = random.choice(df['date'].unique())
    q, a = stock_performance_question(stock, date)
    if q and a:
        questions_answers.append((q, a))
new_list = []
for q, a in questions_answers:
    ques_ans = dict()
    ques_ans["prompt"] = q
    ques_ans["response"] = a
    new_list.append(ques_ans)
evaluation_questions["Stock Performance"] = new_list

questions_answers = []
# Comparative Performance Questions (25)
for _ in range(25):
    stock1 = random.choice(stocks)
    stock2 = random.choice(stocks)
    year = random.choice(df['date'].str[:4].unique())
    q, a = comparative_performance_question(stock1, stock2, year)
    if q and a:
        questions_answers.append((q, a))
new_list = []
for q, a in questions_answers:
    ques_ans = dict()
    ques_ans["prompt"] = q
    ques_ans["response"] = a
    new_list.append(ques_ans)
evaluation_questions["Comparative Performance"] = new_list
    

questions_answers = []
# Event-Driven Questions (25)
for _ in range(25):
    stock = random.choice(stocks)
    event_date = random.choice(df['date'].unique())
    event_type = random.choice(["earnings report", "product launch", "CEO announcement"])
    q, a = event_driven_question(stock, event_date, event_type)
    if q and a:
        questions_answers.append((q, a))
new_list = []
for q, a in questions_answers:
    ques_ans = dict()
    ques_ans["prompt"] = q
    ques_ans["response"] = a
    new_list.append(ques_ans)
evaluation_questions["Event-Driven"] = new_list

questions_answers = []
# Time-Series Questions (25)
for _ in range(25):
    stock = random.choice(stocks)
    date_range = random.sample(list(df['date'].unique()), 2)  # Random start and end dates
    start_date = min(date_range)
    end_date = max(date_range)
    q, a = time_series_question(stock, start_date, end_date)
    if q and a:
        questions_answers.append((q, a))
new_list = []
for q, a in questions_answers:
    ques_ans = dict()
    ques_ans["prompt"] = q
    ques_ans["response"] = a
    new_list.append(ques_ans)
evaluation_questions["Time-Series"] = new_list

import json
json.dump(evaluation_questions, open("new_ques_ans.json", 'w'))
