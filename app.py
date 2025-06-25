from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load data
DATA_PATH = 'data/tamilnadu_crime_2014_2022.csv'
df = pd.read_csv(DATA_PATH)

@app.route('/')
def index():
    years = sorted(df['Year'].unique())
    districts = sorted(df['District'].unique())
    return render_template('index.html', years=years, districts=districts)

@app.route('/analyze', methods=['POST'])
def analyze():
    year = int(request.form['year'])
    district = request.form['district']

    filtered = df[(df['Year'] == year) & (df['District'] == district)]

    # Generate and save plot
    yearly_data = df.groupby('Year')[['Total Complaints', 'Total Cases']].sum()
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=yearly_data)
    plt.title('Crime Trend Over the Years')
    plt.tight_layout()
    plot_path = os.path.join('static', 'trend.png')
    plt.savefig(plot_path)
    plt.close()

    return render_template('results.html',
                           year=year,
                           district=district,
                           total_complaints=int(filtered['Total Complaints'].sum()),
                           total_cases=int(filtered['Total Cases'].sum()),
                           plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
