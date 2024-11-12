# Usage Guide

## Quick Start

```python
from abdmf import ABDMF

# Initialize the system
system = ABDMF()

# Load your historical hiring data
historical_data = pd.read_csv('hiring_data.csv')

# Scan for bias patterns
scan_results = system.scan_historical_data(historical_data)

# Evaluate a new candidate
candidate_data = pd.DataFrame({
    'gender': ['F'],
    'race': ['Asian'],
    'age': [28],
    'years_experience': [5],
    'education_level': ['Master'],
    'interview_score': [85],
    'technical_score': [90]
})

evaluation = system.evaluate_candidate(candidate_data)
```

## Core Components

### 1. Bias Detection

The bias detector analyzes your historical hiring data for patterns of discrimination:

```python
# Get detailed bias metrics
bias_report = system.bias_detector.generate_bias_report(historical_data)

# Analyze intersectional bias
intersectional_analysis = system.bias_detector.analyze_intersectional_bias(
    historical_data,
    attributes=['gender', 'race']
)
```

### 2. Decision Analysis

The decision analyzer provides transparency into hiring decisions:

```python
# Get detailed decision analysis
decision = system.decision_analyzer.analyze_decision(candidate_data)

# Check feature importance
print(decision['significant_features'])

# Check confidence level
print(decision['confidence'])
```

### 3. Feedback System

Collect and analyze feedback from stakeholders:

```python
# Collect feedback
system.feedback_system.collect_feedback('HR', {
    'satisfaction': 4.5,
    'category': 'System_Usability',
    'comments': 'Easy to use and understand',
    'issues': None
})

# Analyze feedback
feedback_analysis = system.feedback_system.analyze_feedback()
```

## Best Practices

1. Data Preparation
   - Clean your data before analysis
   - Ensure consistent formatting
   - Handle missing values appropriately

2. Protected Attributes
   - Define protected attributes in config
   - Monitor all relevant demographics
   - Regular review of attribute definitions

3. Bias Thresholds
   - Set appropriate thresholds
   - Monitor and adjust as needed
   - Document threshold changes

4. Feedback Collection
   - Regular feedback collection
   - Diverse stakeholder input
   - Structured feedback categories

## Example Workflows

### Basic Workflow
```python
# Initialize
system = ABDMF()

# Analyze historical data
scan_results = system.scan_historical_data(historical_data)

# Monitor ongoing decisions
for candidate in candidates:
    result = system.evaluate_candidate(candidate)
    print(result['decision_analysis'])
```

### Advanced Workflow
```python
# Custom configuration
config = {
    'bias_detector': {
        'threshold': 0.15,
        'minimum_sample_size': 200
    },
    'decision_analyzer': {
        'confidence_threshold': 0.85
    }
}

system = ABDMF(config_path='custom_config.yaml')

# Comprehensive analysis
scan_results = system.scan_historical_data(historical_data)
visualize_bias_metrics(scan_results['bias_scan'])

# Detailed monitoring
for candidate in candidates:
    result = system.evaluate_candidate(candidate)
    if not result['decision_analysis']['high_confidence']:
        flag_for_review(candidate)
```

## Troubleshooting

### Common Issues

1. Data Format Issues
```python
# Correct data format
data = data.astype({
    'age': 'float64',
    'years_experience': 'float64',
    'education_level': 'category'
})
```

2. Missing Values
```python
# Handle missing values
data = data.fillna({
    'years_experience': 0,
    'interview_score': data['interview_score'].mean()
})
```

3. Performance Issues
```python
# Optimize for large datasets
system.bias_detector.config['minimum_sample_size'] = 500
```

## Advanced Topics

1. Custom Metrics
2. Integration Strategies
3. Compliance Reporting
4. Model Tuning

See the [API Reference](api.md) for detailed documentation.
