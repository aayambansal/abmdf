import pytest
import pandas as pd
import numpy as np
from abdmf.decision_analyzer import DecisionAnalyzer

@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    np.random.seed(42)
    n_samples = 1000
    
    features = pd.DataFrame({
        'experience': np.random.randint(0, 30, n_samples),
        'education_score': np.random.uniform(0, 100, n_samples),
        'interview_score': np.random.uniform(0, 100, n_samples)
    })
    
    decisions = pd.Series(np.random.choice([0, 1], n_samples))
    
    return features, decisions

@pytest.fixture
def analyzer():
    """Create DecisionAnalyzer instance for testing."""
    return DecisionAnalyzer()

def test_model_training(analyzer, sample_data):
    """Test model training process."""
    features, decisions = sample_data
    metrics = analyzer.train(features, decisions)
    
    assert isinstance(metrics, dict)
    assert 'train' in metrics
    assert 'validation' in metrics
    assert 'feature_importance' in metrics
    
    # Check feature importance
    assert len(metrics['feature_importance']) == len(features.columns)
    assert all(0 <= v <= 1 for v in metrics['feature_importance'].values())

def test_decision_analysis(analyzer, sample_data):
    """Test decision analysis functionality."""
    features, decisions = sample_data
    analyzer.train(features, decisions)
    
    # Test single candidate analysis
    candidate = pd.DataFrame({
        'experience': [5],
        'education_score': [80],
        'interview_score': [75]
    })
    
    result = analyzer.analyze_decision(candidate)
    assert isinstance(result, dict)
    assert 'prediction' in result
    assert 'confidence' in result
    assert 'significant_features' in result
    assert isinstance(result['prediction'], bool)
    assert 0 <= result['confidence'] <= 1

def test_model_persistence(analyzer, sample_data, tmp_path):
    """Test model saving and loading."""
    features, decisions = sample_data
    analyzer.train(features, decisions)
    
    # Save model
    save_path = tmp_path / "model.joblib"
    analyzer.save_model(str(save_path))
    assert save_path.exists()
    
    # Load model
    loaded_analyzer = DecisionAnalyzer.load_model(str(save_path))
    assert loaded_analyzer.feature_names == analyzer.feature_names
    
    # Test predictions match
    candidate = pd.DataFrame({
        'experience': [5],
        'education_score': [80],
        'interview_score': [75]
    })
    
    original_pred = analyzer.analyze_decision(candidate)
    loaded_pred = loaded_analyzer.analyze_decision(candidate)
    assert original_pred['prediction'] == loaded_pred['prediction']

def test_invalid_data(analyzer):
    """Test handling of invalid data."""
    with pytest.raises(ValueError):
        analyzer.analyze_decision(pd.DataFrame({'invalid_feature': [1]}))

def test_confidence_threshold(analyzer, sample_data):
    """Test confidence threshold functionality."""
    features, decisions = sample_data
    analyzer.train(features, decisions)
    
    # Test with high confidence threshold
    analyzer.config['confidence_threshold'] = 0.9
    result = analyzer.analyze_decision(features.iloc[[0]])
    assert 'high_confidence' in result
    
    # Test with low confidence threshold
    analyzer.config['confidence_threshold'] = 0.1
    result = analyzer.analyze_decision(features.iloc[[0]])
    assert result['high_confidence']
