import pandas as pd
import numpy as np
from abdmf import ABDMF
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def setup_logging():
    """Configure logging for the example."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('abdmf_example.log'),
            logging.StreamHandler()
        ]
    )

def generate_realistic_data(n_samples: int = 5000):
    """Generate more realistic hiring data with built-in biases."""
    np.random.seed(42)
    
    # Generate base features
    data = pd.DataFrame({
        'gender': np.random.choice(['M', 'F'], n_samples),
        'race': np.random.choice(['White', 'Black', 'Asian', 'Hispanic'], n_samples),
        'age': np.random.normal(35, 10, n_samples).clip(22, 65),
        'years_experience': np.random.normal(10, 5, n_samples).clip(0, 30),
        'education_level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
        'interview_score': np.random.normal(75, 15, n_samples).clip(0, 100),
        'technical_score': np.random.normal(70, 20, n_samples).clip(0, 100)
    })
    
    # Add synthetic biases
    base_prob = 0.3  # Base selection probability
    
    # Create selection probabilities with built-in biases
    selection_prob = base_prob + \
                    (data['gender'] == 'M') * 0.1 + \
                    (data['age'] < 40) * 0.15 + \
                    (data['education_level'].isin(['Master', 'PhD'])) * 0.2 + \
                    (data['years_experience'] > 5) * 0.1
    
    # Normalize probabilities
    selection_prob = selection_prob.clip(0, 1)
    
    # Generate final selection
    data['selected'] = np.random.binomial(1, selection_prob)
    
    return data

def visualize_bias_metrics(bias_scan, save_path: str = None):
    """Visualize bias detection results."""
    metrics = bias_scan['detailed_metrics']
    
    # Prepare data for plotting
    attributes = list(metrics.keys())
    disparate_impact = [m['disparate_impact'] for m in metrics.values()]
    statistical_parity = [m['statistical_parity'] for m in metrics.values()]
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot disparate impact
    sns.barplot(x=attributes, y=disparate_impact, ax=ax1)
    ax1.set_title('Disparate Impact by Protected Attribute')
    ax1.axhline(y=0.8, color='r', linestyle='--', label='Threshold')
    ax1.set_ylim(0, 1)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    
    # Plot statistical parity
    sns.barplot(x=attributes, y=statistical_parity, ax=ax2)
    ax2.set_title('Statistical Parity Difference by Protected Attribute')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def analyze_feedback_trends(feedback_data):
    """Analyze trends in feedback over time."""
    df = pd.DataFrame(feedback_data)
    
    # Create time-based visualizations
    plt.figure(figsize=(12, 6))
    
    # Plot average satisfaction over time
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_satisfaction = df.groupby('date')['satisfaction'].mean()
    
    sns.lineplot(data=daily_satisfaction)
    plt.title('Average Satisfaction Over Time')
    plt.xlabel('Date')
    plt.ylabel('Satisfaction Score')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def main():
    # Setup logging
    setup_logging()
    logging.info("Starting advanced ABDMF example")
    
    # Initialize system
    system = ABDMF()
    
    # Generate and analyze data
    logging.info("Generating synthetic data")
    data = generate_realistic_data()
    
    # Scan for bias
    logging.info("Scanning for bias patterns")
    scan_results = system.scan_historical_data(data)
    
    # Visualize results
    logging.info("Generating visualizations")
    visualize_bias_metrics(scan_results['bias_scan'], 'bias_metrics.png')
    
    # Simulate multiple candidate evaluations
    logging.info("Simulating candidate evaluations")
    n_candidates = 100
    for i in range(n_candidates):
        candidate_data = pd.DataFrame({
            'gender': [np.random.choice(['M', 'F'])],
            'race': [np.random.choice(['White', 'Black', 'Asian', 'Hispanic'])],
            'age': [np.random.normal(35, 10)],
            'years_experience': [np.random.normal(10, 5)],
            'education_level': [np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'])],
            'interview_score': [np.random.normal(75, 15)],
            'technical_score': [np.random.normal(70, 20)]
        })
        
        evaluation = system.evaluate_candidate(candidate_data)
        
        # Simulate feedback collection
        if i % 10 == 0:  # Collect feedback every 10 evaluations
            system.feedback_system.collect_feedback('HR', {
                'satisfaction': np.random.normal(4, 0.5).clip(1, 5),
                'category': np.random.choice(['System_Usability', 'Decision_Fairness']),
                'comments': 'Simulated feedback',
                'issues': None
            })
    
    # Analyze feedback trends
    logging.info("Analyzing feedback trends")
    report = system.generate_report()
    analyze_feedback_trends(system.feedback_system.feedback_data)
    
    logging.info("Example completed successfully")

if __name__ == "__main__":
    main()
