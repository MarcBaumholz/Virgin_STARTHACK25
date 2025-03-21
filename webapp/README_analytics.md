# Virgin Initiatives Analytics Module

This module provides comprehensive analytics and insights from the Virgin initiatives data. It analyzes various aspects of the initiatives and generates visualizations to help understand patterns and trends.

## Features

### 1. Company Distribution Analysis
- Total number of initiatives per Virgin company
- Detailed breakdown of initiatives by company
- Company-specific challenges and focus areas

### 2. Challenges Analysis
- Word frequency analysis of challenges
- Identification of common themes
- Examples of unique challenges

### 3. Actions and Impact Analysis
- Categorization of actions taken
- Impact metrics by category:
  - Environmental
  - Social
  - Technological
  - Conservation

### 4. Call to Action Analysis
- Types of calls to action
- Distribution of engagement methods
- Examples of different CTAs

### 5. Visualizations
- Company distribution bar chart
- Action types pie chart
- Additional visualizations can be added as needed

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the analytics:
```bash
python generate_analytics.py
```

3. Check the results:
- Analytics data: `output/analytics.json`
- Visualizations: `output/visualizations/`

## Output Structure

### analytics.json
```json
{
    "company_distribution": {
        "total_initiatives": <number>,
        "companies": [<list of companies>],
        "initiatives_per_company": {<company>: <count>},
        "company_breakdown": {
            "<company>": {
                "total_initiatives": <number>,
                "initiatives": [<list of initiatives>],
                "challenges": [<list of challenges>]
            }
        }
    },
    "challenges_analysis": {
        "word_frequency": {<word>: <count>},
        "total_unique_challenges": <number>,
        "challenge_examples": [<list of examples>]
    },
    "actions_analysis": {
        "total_actions": <number>,
        "action_types": {<type>: <count>},
        "impact_metrics": {
            "environmental": <number>,
            "social": <number>,
            "technological": <number>,
            "conservation": <number>
        }
    },
    "cta_analysis": {
        "total_ctas": <number>,
        "cta_types": {<type>: <count>},
        "cta_examples": [<list of examples>]
    }
}
```

### Visualizations
- `company_distribution.png`: Bar chart showing initiatives per company
- `action_types_distribution.png`: Pie chart showing distribution of action types

## Future Enhancements

1. **Additional Analytics**
   - Time-based analysis of initiatives
   - Success rate analysis
   - Resource allocation analysis

2. **Enhanced Visualizations**
   - Interactive dashboards
   - Geographic distribution maps
   - Impact trend analysis

3. **Integration Features**
   - API endpoints for analytics
   - Real-time data updates
   - Custom report generation

4. **Advanced Analysis**
   - Machine learning for pattern recognition
   - Predictive analytics for initiative success
   - Sentiment analysis of challenges and actions

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 