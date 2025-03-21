# Virgin Initiatives Analysis Platform

This project analyzes Virgin's sustainability and social responsibility initiatives to create insights and enable collaboration between different Virgin companies and initiatives.

## Project Structure

- `analyze_initiatives.py`: Main script for analyzing the initiatives data
- `requirements.txt`: Python dependencies
- `output/insights.json`: Generated insights from the analysis
- `Virgin_StartHack_Sample_Initiatives.csv`: Input data file

## Features

1. **Data Analysis**
   - Loads and cleans initiative data from CSV
   - Performs text analysis using TF-IDF vectorization
   - Calculates similarity between initiatives
   - Categorizes initiatives into themes

2. **Insights Generation**
   - Total number of initiatives
   - List of Virgin companies involved
   - Top keywords across all initiatives
   - Similarity analysis between initiatives
   - Categorized initiatives by theme

3. **Categories**
   - Environmental initiatives
   - Social initiatives
   - Technology initiatives
   - Conservation initiatives

## Implementation Details

### Data Processing
- The script uses pandas to load and process the CSV data
- Text data is combined from multiple columns for comprehensive analysis
- Missing values are handled appropriately

### Text Analysis
- TF-IDF vectorization is used to convert text into numerical features
- Cosine similarity is calculated to find related initiatives
- Keywords are extracted and ranked by importance

### Categorization
- Initiatives are categorized based on predefined keywords
- Each initiative can belong to multiple categories
- Categories are designed to reflect Virgin's main focus areas

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the analysis:
```bash
python analyze_initiatives.py
```

3. Check the results in `output/insights.json`

## Future Enhancements

1. **Web Interface**
   - Create a web application to visualize insights
   - Add interactive features for exploring initiatives
   - Implement user authentication and profiles

2. **Matchmaking System**
   - Develop an algorithm to match similar initiatives
   - Add collaboration suggestions
   - Create a recommendation system

3. **Impact Tracking**
   - Add metrics tracking for initiatives
   - Implement progress monitoring
   - Create impact visualization tools

4. **Community Features**
   - Add user engagement features
   - Implement feedback mechanisms
   - Create collaboration spaces

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 