import pytest
import pandas as pd
import numpy as np
from abdmf.bias_detector import BiasDetector

@pytest.fixture
def sample_data():
    """Generate sample data for testing."""
    np.random.seed(42)
    n_samples = 1000
    
    return pd.DataFrame({
        'gender': np.random.choice(['M', 'F'], n_samples),
        'race': np.random.choice(['A', 'B', 'C'], n_samples),
        'age': np.random.randint(22, 65, n_samples),
        'experience': np.random.randint(0, 30, n_samples),
        'education_score': np.random.uniform(0, 100, n_samples),
        'selected': np.random.choice([0, 1], n_samples)
    })

@pytest.fixture
def bias_detector():
    """Create BiasDetector instance for testing."""
    return BiasDetector()

def test_disparate_impact_calculation(bias_detector, sample_data):
    """Test disparate impact calculation."""
    impact = bias_detector.calculate_disparate_impact(sample_data, 'gender')
    assert 0 <= impact <= 1
    assert isinstance(impact, float)

def test_statistical_parity(bias_detector, sample_data):
    """Test statistical parity calculation."""
    parity = bias_detector.calculate_statistical_parity(sample_data, 'gender')
    assert 0 <= parity <= 1
    assert isinstance(parity, float)

def test_bias_detection(bias_detector, sample_data):
    """Test overall bias detection."""
    results = bias_detector.detect_bias(sample_data)
    assert isinstance(results, dict)
    assert 'gender' in results
    assert 'race' in results
    
    for attribute, metrics in results.items():
        assert 'disparate_impact' in metrics
        assert 'statistical_parity' in metrics
        assert 'sample_size' in metrics
        assert isinstance(metrics['disparate_impact'], float)

def test_intersectional_bias(bias_detector, sample_data):
    """Test intersectional bias analysis."""
    results = bias_detector.analyze_intersectional_bias(
        sample_data, ['gender', 'race']
    )
    assert isinstance(results, dict)
    assert 'disparate_impact' in results

def test_bias_report(bias_detector, sample_data):
    """Test bias report generation."""
    report = bias_detector.generate_bias_report(sample_data)
    assert isinstance(report, dict)
    assert 'summary' in report
    assert 'detailed_metrics' in report
    assert 'recommendations' in report
    assert isinstance(report['recommendations'], list)

def test_invalid_data(bias_detector):
    """Test handling of invalid data."""
    invalid_data = pd.DataFrame({'invalid_column': [1, 2, 3]})
    with pytest.raises(ValueError):
        bias_detector.detect_bias(invalid_data)

def test_empty_data(bias_detector):
    """Test handling of empty data."""
    empty_data = pd.DataFrame()
    with pytest.raises(ValueError):
        bias_detector.detect_bias(empty_data)
