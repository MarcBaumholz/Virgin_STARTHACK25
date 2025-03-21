from flask import Flask, render_template, jsonify, request
import json
import os
from analyze_initiatives import load_and_clean_data, analyze_initiatives, generate_insights

app = Flask(__name__)

# Load data and generate insights
df = load_and_clean_data()
similarity_matrix, feature_names = analyze_initiatives(df)
insights = generate_insights(df, similarity_matrix)

@app.route('/')
def index():
    return render_template('index.html', insights=insights)

@app.route('/api/initiatives')
def get_initiatives():
    initiatives = []
    for idx, row in df.iterrows():
        initiatives.append({
            'name': row['Initiaitive'],
            'company': row['Virgin Company'],
            'challenge': row['Challenge'],
            'action': row['What Virgin is doing'],
            'call_to_action': row['Call to Action'],
            'links': row['Links'].split(',') if row['Links'] else []
        })
    return jsonify(initiatives)

@app.route('/api/similar/<initiative_name>')
def get_similar(initiative_name):
    if initiative_name not in similarity_matrix.index:
        return jsonify({'error': 'Initiative not found'}), 404
    
    similar = similarity_matrix[initiative_name].sort_values(ascending=False)[1:4]
    return jsonify(similar.to_dict())

@app.route('/api/categories')
def get_categories():
    return jsonify(insights['categories'])

@app.route('/api/keywords')
def get_keywords():
    return jsonify(insights['top_keywords'])

if __name__ == '__main__':
    app.run(debug=True) 