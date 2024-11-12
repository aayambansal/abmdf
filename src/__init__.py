from .bias_detector import BiasDetector
from .decision_analyzer import DecisionAnalyzer
from .feedback_system import FeedbackSystem
from .utils import load_config, validate_data

class ABDMF:
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path) if config_path else {}
        self.bias_detector = BiasDetector(self.config.get('bias_detector', {}))
        self.decision_analyzer = DecisionAnalyzer(self.config.get('decision_analyzer', {}))
        self.feedback_system = FeedbackSystem(self.config.get('feedback_system', {}))
        
    def scan_historical_data(self, data):
        """Scan historical hiring data for bias patterns."""
        validate_data(data, required_columns=['selected'])
        
        bias_scan = self.bias_detector.generate_bias_report(data)
        
        features = data.drop(['selected'] + self.bias_detector.config['protected_attributes'], axis=1)
        model_metrics = self.decision_analyzer.train(features, data['selected'])
        
        return {
            'bias_scan': bias_scan,
            'model_metrics': model_metrics,
            'timestamp': pd.Timestamp.now()
        }
    
    def evaluate_candidate(self, candidate_data):
        """Evaluate a candidate while checking for potential bias."""
        validate_data(candidate_data)
        
        protected_attributes = {
            attr: candidate_data.get(attr)
            for attr in self.bias_detector.config['protected_attributes']
            if attr in candidate_data
        }
        
        features = candidate_data.drop(list(protected_attributes.keys()), axis=1)
        decision_analysis = self.decision_analyzer.analyze_decision(features)
        
        return {
            'decision_analysis': decision_analysis,
            'protected_attributes': protected_attributes,
            'timestamp': pd.Timestamp.now()
        }
        
    def generate_report(self):
        """Generate a comprehensive system performance report."""
        feedback_analysis = self.feedback_system.analyze_feedback()
        
        return {
            'system_metrics': {
                'total_evaluations': len(self.feedback_system.feedback_data),
                'bias_detection_accuracy': self.bias_detector.get_accuracy(),
                'decision_analysis_performance': self.decision_analyzer.performance_metrics,
                'system_uptime': 99.9  # Placeholder for actual uptime tracking
            },
            'feedback_analysis': feedback_analysis,
            'timestamp': pd.Timestamp.now()
        }

__version__ = "0.1.0"
