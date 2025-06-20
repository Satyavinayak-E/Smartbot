# plot_generator.py
import matplotlib.pyplot as plt
import json
import os

def generate_plot():
    with open('data/chat_logs.json') as f:
        logs = json.load(f)

    success = sum(1 for log in logs if log['success'])
    failure = len(logs) - success

    labels = ['Successful', 'Unsuccessful']
    sizes = [success, failure]
    colors = ['#28a745', '#dc3545']

    # Ensure charts folder exists
    os.makedirs('static/charts', exist_ok=True)

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.axis('equal')
    plt.title('Search Analytics')
    plt.savefig('static/charts/search_analytics.png')
    plt.close()
