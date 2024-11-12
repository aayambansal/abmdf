import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import json

class FeedbackSystem:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            'user_types': ['HR', 'Candidate', 'Manager', 'DEI_Officer'],
            'feedback_categories': [
                'System_Usability',
                'Decision_Fairness',
                'Transparency',
                'Technical_Issues'
            ],
            'satisfaction_scale': (1, 5),
            'retention_period_days': 365
        }
        self.feedback_data = []
        self.analysis_cache = {}
        
    def collect_feedback(self, user_type: str, feedback: Dict[str, Any]) -> bool:
        """Collect and validate user feedback."""
        if user_type not in self.config['user_types']:
            raise ValueError(f"Invalid user type: {user_type}")
            
        required_fields = ['satisfaction', 'category', 'comments']
        missing_fields = [f for f in required_fields if f not in feedback]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
            
        if not self._validate_satisfaction_score(feedback['satisfaction']):
            raise ValueError(
                f"Invalid satisfaction score. Must be between "
                f"{self.config['satisfaction_scale'][0]} and "
                f"{self.config['satisfaction_scale'][1]}"
            )
            
        feedback_entry = {
            'user_type': user_type,
            'timestamp': datetime.now(),
            **feedback
        }
        
        self.feedback_data.append(feedback_entry)
        self._clear_analysis_cache()
        
        return True
    
    def _validate_satisfaction_score(self, score: float) -> bool:
        """Validate satisfaction score is within configured range."""
        min_score, max_score = self.config['satisfaction_scale']
        return isinstance(score, (int, float)) and min_score <= score <= max_score
    
    def analyze_feedback(self, timeframe_days: int = None) -> Dict[str, Any]:
        """Analyze collected feedback to identify patterns and issues."""
        if not self.feedback_data:
            return {
                'status': 'No feedback data available',
                'timestamp': datetime.now()
            }
            
        # Convert feedback data to DataFrame for analysis
        df = pd.DataFrame(self.feedback_data)
        
        # Apply timeframe filter if specified
        if timeframe_days:
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=timeframe_days)
            df = df[df['timestamp'] >= cutoff_date]
            
        if len(df) == 0:
            return {
                'status': 'No feedback data available for specified timeframe',
                'timestamp': datetime.now()
            }
            
        analysis = {
            'overall_metrics': {
                'total_feedback': len(df),
                'average_satisfaction': df['satisfaction'].mean(),
                'satisfaction_std': df['satisfaction'].std(),
                'feedback_trend': self._calculate_feedback_trend(df)
            },
            'user_type_analysis': {
                'feedback_by_user_type': df['user_type'].value_counts().to_dict(),
                'satisfaction_by_user_type': df.groupby('user_type')['satisfaction'].mean().to_dict()
            },
            'category_analysis': {
                'feedback_by_category': df['category'].value_counts().to_dict(),
                'satisfaction_by_category': df.groupby('category')['satisfaction'].mean().to_dict()
            },
            'timestamp': datetime.now()
        }
        
        return analysis
    
    def _calculate_feedback_trend(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate trend in feedback satisfaction over time."""
        df = df.sort_values('timestamp')
        df['satisfaction_rolling_avg'] = df['satisfaction'].rolling(
            window=min(10, len(df)),
            min_periods=1
        ).mean()
        
        trend = {
            'direction': 'stable',
            'strength': 0.0
        }
        
        if len(df) >= 2:
            start_avg = df['satisfaction_rolling_avg'].iloc[0]
            end_avg = df['satisfaction_rolling_avg'].iloc[-1]
            change = end_avg - start_avg
            
            if abs(change) > 0.1:
                trend['direction'] = 'improving' if change > 0 else 'declining'
                trend['strength'] = abs(change)
                
        return trend
    
    def _clear_analysis_cache(self):
        """Clear cached analysis results."""
        self.analysis_cache = {}
