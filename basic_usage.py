import pandas as pd
import numpy as np
from abdmf import ABDMF

def generate_sample_data(n_samples: int = 1000):
    """Generate sample hiring data for demonstration."""
    np.random.seed(42)
    
    data = pd.DataFrame({
        'gender': np.random.choice(['M', 'F'], n_samples),
        'race': np.random.choice(['A', 'B', 'C'], n_samples),
        'age': np.random.randint(22, 65, n_samples),
        'experience': np.random.randint(0, 30, n_samples),
        'education_score': np.random.uniform(0, 100, n_samples),
        'interview_score': np.random.uniform(0, 100, n_samples),
        'selected': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    })
    
    # Introduce some synthetic bias
    data.loc[(data['gender'] == 'F') & (data['experience'] > 10), 'selected'] *= 0.7
    data.loc[data['age'] > 50, 'selected'] *= 0.8
    
    return data

def main():
    # Initialize the system
    system = ABDMF()
    
    # Generate and analyze historical data
    historical_data = generate_sample_data(1000)
    print("\nScanning historical data...")
    scan_results = system.scan_historical_data(historical_data)
    print("Bias scan results:", scan_results['bias_scan'])
    
    # Evaluate a candidate
    candidate_data = pd.DataFrame({
        'gender': ['F'],
        'race': ['B'],
        'age': [28],
        'experience': [5],
        'education_score': [85],
        'interview_score': [90]
    })
    
    print("\nEvaluating candidate...")
    evaluation = system.evaluate_candidate(candidate_data)
    print("Evaluation results:", evaluation)
    
    # Collect feedback
    print("\nCollecting feedback...")
    system.feedback_system.collect_feedback('HR', {
        'satisfaction': 4.5,
        'category': 'System_Usability',
        'comments': 'System working well',
        'issues': None
    })
    
    # Generate report
    print("\nGenerating system report...")
    report = system.generate_report()
    print("System report:", report)

if __name__ == "__main__":
    main()
