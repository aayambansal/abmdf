import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

class DecisionAnalyzer:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {
            'model_params': {
                'n_estimators': 100,
                'max_depth': None,
                'min_samples_split': 2,
                'random_state': 42
            },
            'feature_importance_threshold': 0.05,
            'confidence_threshold': 0.8
        }
        self.model = RandomForestClassifier(**self.config['model_params'])
        self.feature_names = None
        self.performance_metrics = {}
        
    def preprocess_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features for model training/prediction."""
        processed = features.copy()
        
        # Handle categorical variables
        categorical_columns = processed.select_dtypes(
            include=['object', 'category']
        ).columns
        
        for col in categorical_columns:
            processed[col] = pd.Categorical(processed[col]).codes
            
        # Handle missing values
        processed = processed.fillna(processed.mean())
        
        return processed
    
    def train(self, features: pd.DataFrame, decisions: pd.Series,
              validation_split: float = 0.2) -> Dict[str, Any]:
        """Train the decision analyzer model."""
        self.feature_names = features.columns.tolist()
        processed_features = self.preprocess_features(features)
        
        # Split data for validation
        X_train, X_val, y_train, y_val = train_test_split(
            processed_features, decisions,
            test_size=validation_split,
            random_state=self.config['model_params']['random_state']
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Calculate performance metrics
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        
        self.performance_metrics = {
            'train': classification_report(y_train, train_pred, output_dict=True),
            'validation': classification_report(y_val, val_pred, output_dict=True),
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
        
        return self.performance_metrics
    
    def analyze_decision(self, candidate_features: pd.DataFrame) -> Dict[str, Any]:
        """Analyze a hiring decision and provide detailed explanation."""
        if not isinstance(candidate_features, pd.DataFrame):
            raise ValueError("candidate_features must be a pandas DataFrame")
            
        if self.feature_names is None:
            raise RuntimeError("Model needs to be trained before analyzing decisions")
            
        # Ensure features match training data
        missing_features = set(self.feature_names) - set(candidate_features.columns)
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
            
        processed_features = self.preprocess_features(
            candidate_features[self.feature_names]
        )
        
        # Get prediction and probability
        prediction = self.model.predict(processed_features)[0]
        probability = self.model.predict_proba(processed_features)[0]
        
        # Get feature importance for this decision
        feature_importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        
        # Filter significant features
        significant_features = {
            k: v for k, v in feature_importance.items()
            if v >= self.config['feature_importance_threshold']
        }
        
        return {
            'prediction': bool(prediction),
            'confidence': float(max(probability)),
            'significant_features': significant_features,
            'all_features': feature_importance,
            'high_confidence': max(probability) >= self.config['confidence_threshold']
        }
    
    def save_model(self, path: str):
        """Save the trained model and configuration."""
        if self.feature_names is None:
            raise RuntimeError("Model needs to be trained before saving")
            
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'performance_metrics': self.performance_metrics,
            'config': self.config
        }
        
        joblib.dump(model_data, path)
    
    @classmethod
    def load_model(cls, path: str) -> 'DecisionAnalyzer':
        """Load a trained model and configuration."""
        model_data = joblib.load(path)
        
        analyzer = cls(config=model_data['config'])
        analyzer.model = model_data['model']
        analyzer.feature_names = model_data['feature_names']
        analyzer.performance_metrics = model_data['performance_metrics']
        
        return analyzer
