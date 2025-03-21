import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json
from datetime import datetime
import os

def load_data():
    """Load and clean the data"""
    df = pd.read_csv('Virgin_StartHack_Sample_Initiatives.csv', encoding='latin1')
    df = df.fillna('')
    return df

def analyze_company_distribution(df):
    """Analyze distribution of initiatives across companies"""
    company_stats = {
        'total_initiatives': len(df),
        'companies': df['Virgin Company'].unique().tolist(),
        'initiatives_per_company': df['Virgin Company'].value_counts().to_dict(),
        'company_breakdown': {}
    }
    
    for company in df['Virgin Company'].unique():
        company_data = df[df['Virgin Company'] == company]
        company_stats['company_breakdown'][company] = {
            'total_initiatives': len(company_data),
            'initiatives': company_data['Initiaitive'].tolist(),
            'challenges': company_data['Challenge'].tolist()
        }
    
    return company_stats

def analyze_challenges(df):
    """Analyze common challenges and themes"""
    # Combine all challenge texts
    all_challenges = ' '.join(df['Challenge'].astype(str))
    
    # Create word frequency analysis
    words = all_challenges.lower().split()
    word_freq = Counter(words)
    
    # Remove common words and short words
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are', 'was', 'were', 'will', 'would', 'could', 'should', 'have', 'has', 'had', 'been', 'being', 'be', 'am', 'is', 'are', 'was', 'were', 'will', 'be', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'off', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'over', 'under', 'again', 'further', 'then', 'once'}
    
    filtered_words = {word: count for word, count in word_freq.items() 
                     if word not in stop_words and len(word) > 3}
    
    return {
        'word_frequency': dict(sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20]),
        'total_unique_challenges': len(df['Challenge'].unique()),
        'challenge_examples': df['Challenge'].head(5).tolist()
    }

def analyze_actions_and_impact(df):
    """Analyze actions taken and their potential impact"""
    actions_analysis = {
        'total_actions': len(df),
        'action_types': {},
        'impact_metrics': {
            'environmental': 0,
            'social': 0,
            'technological': 0,
            'conservation': 0
        }
    }
    
    # Analyze action types
    for action in df['What Virgin is doing']:
        action = action.lower()
        if 'recycle' in action or 'sustainable' in action:
            actions_analysis['action_types']['recycling_sustainability'] = actions_analysis['action_types'].get('recycling_sustainability', 0) + 1
        if 'community' in action or 'people' in action:
            actions_analysis['action_types']['community_development'] = actions_analysis['action_types'].get('community_development', 0) + 1
        if 'technology' in action or 'digital' in action:
            actions_analysis['action_types']['technology'] = actions_analysis['action_types'].get('technology', 0) + 1
        if 'conservation' in action or 'protection' in action:
            actions_analysis['action_types']['conservation'] = actions_analysis['action_types'].get('conservation', 0) + 1
    
    return actions_analysis

def analyze_call_to_action(df):
    """Analyze types of calls to action"""
    cta_analysis = {
        'total_ctas': len(df),
        'cta_types': {},
        'cta_examples': df['Call to Action'].unique().tolist()
    }
    
    # Categorize CTAs
    for cta in df['Call to Action']:
        cta = cta.lower()
        if 'donate' in cta:
            cta_analysis['cta_types']['donation'] = cta_analysis['cta_types'].get('donation', 0) + 1
        if 'volunteer' in cta:
            cta_analysis['cta_types']['volunteering'] = cta_analysis['cta_types'].get('volunteering', 0) + 1
        if 'sign' in cta or 'petition' in cta:
            cta_analysis['cta_types']['petition'] = cta_analysis['cta_types'].get('petition', 0) + 1
        if 'learn' in cta or 'inform' in cta:
            cta_analysis['cta_types']['education'] = cta_analysis['cta_types'].get('education', 0) + 1
    
    return cta_analysis

def generate_visualizations(df, output_dir='output/visualizations'):
    """Generate visualizations for the data"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Company distribution
    plt.figure(figsize=(12, 6))
    df['Virgin Company'].value_counts().plot(kind='bar')
    plt.title('Initiatives by Virgin Company')
    plt.xlabel('Company')
    plt.ylabel('Number of Initiatives')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/company_distribution.png')
    plt.close()
    
    # Action types distribution
    action_types = analyze_actions_and_impact(df)['action_types']
    plt.figure(figsize=(10, 6))
    plt.pie(action_types.values(), labels=action_types.keys(), autopct='%1.1f%%')
    plt.title('Distribution of Action Types')
    plt.savefig(f'{output_dir}/action_types_distribution.png')
    plt.close()

def main():
    # Load data
    df = load_data()
    
    # Generate analyses
    analytics = {
        'company_distribution': analyze_company_distribution(df),
        'challenges_analysis': analyze_challenges(df),
        'actions_analysis': analyze_actions_and_impact(df),
        'cta_analysis': analyze_call_to_action(df)
    }
    
    # Generate visualizations
    generate_visualizations(df)
    
    # Save analytics to JSON
    if not os.path.exists('output'):
        os.makedirs('output')
    
    with open('output/analytics.json', 'w') as f:
        json.dump(analytics, f, indent=4)
    
    print("Analytics generated successfully! Check output/analytics.json and output/visualizations/ for results.")

if __name__ == "__main__":
    main() 