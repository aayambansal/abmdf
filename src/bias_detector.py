import pandas as pd
import numpy as np
from typing import Dict, List, Any

class BiasDetector:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            'protected_attributes': [
                'gender', 'race', 'age', 'education_type',
                'career_change', 'disability_status', 'location'
            ],
            'threshold': 0.2,
            'minimum_sample_size': 100
        }
        self.baseline_metrics = {}
        
    def calculate_disparate_impact(self, data: pd.DataFrame, attribute: str) -> float:
        """Calculate disparate impact ratio for a protected attribute."""
        groups = data[attribute].unique()
        selection_rates = {}
        
        for group in groups:
            group_data = data[data[attribute] == group]
            if len(group_data) >= self.config['minimum_sample_size']:
                selection_rates[group] = (group_data['selected'] == 1).mean()
        
        if not selection_rates:
            return 0.0
            
        max_rate = max(selection_rates.values())
        min_rate = min(selection_rates.values())
        
        return min_rate / max_rate if max_rate > 0 else 0.0
    
    def calculate_statistical_parity(self, data: pd.DataFrame, attribute: str) -> float:
        """Calculate statistical parity difference."""
        groups = data[attribute].unique()
        selection_rates = {}
        
        for group in groups:
            group_data = data[data[attribute] == group]
            if len(group_data) >= self.config['minimum_sample_size']:
                selection_rates[group] = (group_data['selected'] == 1).mean()
                
        if not selection_rates:
            return 0.0
            
        return max(selection_rates.values()) - min(selection_rates.values())
    
    def detect_bias(self, data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Comprehensive bias detection across all protected attributes."""
        results = {}
        
        for attribute in self.config['protected_attributes']:
            if attribute not in data.columns:
                continue
                
            results[attribute] = {
                'disparate_impact': self.calculate_disparate_impact(data, attribute),
                'statistical_parity': self.calculate_statistical_parity(data, attribute),
                'sample_size': len(data[data[attribute].notna()]),
                'groups_analyzed': len(data[attribute].unique())
            }
            
        return results
    
    def analyze_intersectional_bias(self, data: pd.DataFrame, 
                                  attributes: List[str]) -> Dict[str, float]:
        """Analyze intersectional bias across multiple attributes."""
        if not all(attr in data.columns for attr in attributes):
            return {}
            
        # Create intersectional groups
        data['intersectional_group'] = data[attributes].apply(
            lambda x: '_'.join(x.astype(str)), axis=1
        )
        
        return self.detect_bias(data)['intersectional_group']
    
    def generate_bias_report(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive bias analysis report."""
        bias_metrics = self.detect_bias(data)
        
        report = {
            'summary': {
                'total_records': len(data),
                'attributes_analyzed': len(bias_metrics),
                'significant_bias_detected': any(
                    m['disparate_impact'] < (1 - self.config['threshold'])
                    for m in bias_metrics.values()
                )
            },
            'detailed_metrics': bias_metrics,
            'recommendations': self._generate_recommendations(bias_metrics),
            'timestamp': pd.Timestamp.now()
        }
        
        return report
    
    def _generate_recommendations(self, metrics: Dict[str, Dict[str, float]]) -> List[str]:
        """Generate recommendations based on bias analysis."""
        recommendations = []
        
        for attribute, values in metrics.items():
            if values['disparate_impact'] < (1 - self.config['threshold']):
                recommendations.append(
                    f"High bias detected in {attribute}. Consider reviewing "
                    f"selection criteria and implementing additional controls."
                )
            if values['statistical_parity'] > self.config['threshold']:
                recommendations.append(
                    f"Significant selection rate differences found in {attribute}. "
                    f"Review decision-making process for this attribute."
                )
                
        return recommendations
