import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
import os

def load_and_clean_data():
    # Read the CSV file with specified encoding
    df = pd.read_csv('Virgin_StartHack_Sample_Initiatives.csv', encoding='latin1')
    
    # Clean the data
    df = df.fillna('')
    
    # Create a combined text field for analysis
    df['combined_text'] = df['Initiaitive'] + ' ' + df['Challenge'] + ' ' + df['What Virgin is doing']
    
    return df

def analyze_initiatives(df):
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Create TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)
    
    # Get feature names (keywords)
    feature_names = vectorizer.get_feature_names_out()
    
    # Create similarity matrix
    similarity_matrix = pd.DataFrame(cosine_sim, 
                                   index=df['Initiaitive'],
                                   columns=df['Initiaitive'])
    
    return similarity_matrix, feature_names

def generate_insights(df, similarity_matrix):
    insights = {
        'total_initiatives': len(df),
        'companies': df['Virgin Company'].unique().tolist(),
        'top_keywords': get_top_keywords(df),
        'similarity_analysis': get_similarity_analysis(similarity_matrix),
        'categories': categorize_initiatives(df)
    }
    
    return insights

def get_top_keywords(df):
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    
    # Get feature names and their importance
    feature_names = vectorizer.get_feature_names_out()
    importance = np.array(tfidf_matrix.sum(axis=0)).flatten()
    
    # Create dictionary of keywords and their importance
    keywords = dict(zip(feature_names, importance))
    
    # Sort by importance
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords

def get_similarity_analysis(similarity_matrix):
    # Find most similar initiatives
    similar_pairs = []
    for i in range(len(similarity_matrix.columns)):
        for j in range(i+1, len(similarity_matrix.columns)):
            if similarity_matrix.iloc[i,j] > 0.5:  # Threshold for similarity
                similar_pairs.append({
                    'initiative1': similarity_matrix.columns[i],
                    'initiative2': similarity_matrix.columns[j],
                    'similarity': float(similarity_matrix.iloc[i,j])
                })
    
    return similar_pairs

def categorize_initiatives(df):
    # Define categories based on keywords
    categories = {
        'environmental': ['climate', 'sustainable', 'recycle', 'planet', 'ocean'],
        'social': ['community', 'education', 'healthcare', 'people'],
        'technology': ['digital', 'connectivity', 'mobile', 'devices'],
        'conservation': ['wildlife', 'biodiversity', 'protection', 'preserve']
    }
    
    categorized = {}
    for category, keywords in categories.items():
        initiatives = []
        for idx, row in df.iterrows():
            text = row['combined_text'].lower()
            if any(keyword in text for keyword in keywords):
                initiatives.append({
                    'name': row['Initiaitive'],
                    'company': row['Virgin Company'],
                    'challenge': row['Challenge']
                })
        categorized[category] = initiatives
    
    return categorized

def save_insights(insights):
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Save insights to JSON file
    with open('output/insights.json', 'w') as f:
        json.dump(insights, f, indent=4)

def main():
    # Load and clean data
    df = load_and_clean_data()
    
    # Analyze initiatives
    similarity_matrix, feature_names = analyze_initiatives(df)
    
    # Generate insights
    insights = generate_insights(df, similarity_matrix)
    
    # Save insights
    save_insights(insights)
    
    print("Analysis complete! Check output/insights.json for results.")

if __name__ == "__main__":
    main() 