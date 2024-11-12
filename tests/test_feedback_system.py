import pytest
import pandas as pd
from datetime import datetime, timedelta
from abdmf.feedback_system import FeedbackSystem

@pytest.fixture
def feedback_system():
    """Create FeedbackSystem instance for testing."""
    return FeedbackSystem()

@pytest.fixture
def sample_feedback():
    """Generate sample feedback data."""
    return {
        'satisfaction': 4,
        'category': 'System_Usability',
        'comments': 'System works well',
        'issues': None
    }

def test_feedback_collection(feedback_system, sample_feedback):
    """Test feedback collection functionality."""
    result = feedback_system.collect_feedback('HR', sample_feedback)
    assert result is True
    assert len(feedback_system.feedback_data) == 1
    
    # Verify stored feedback
    stored = feedback_system.feedback_data[0]
    assert stored['user_type'] == 'HR'
    assert stored['satisfaction'] == 4
    assert stored['category'] == 'System_Usability'
    assert isinstance(stored['timestamp'], datetime)

def test_invalid_feedback(feedback_system):
    """Test handling of invalid feedback."""
    # Test invalid user type
    with pytest.raises(ValueError):
        feedback_system.collect_feedback('InvalidUser', {})
    
    # Test missing required fields
    with pytest.raises(ValueError):
        feedback_system.collect_feedback('HR', {'satisfaction': 4})
    
    # Test invalid satisfaction score
    with pytest.raises(ValueError):
        feedback_system.collect_feedback('HR', {
            'satisfaction': 6,
            'category': 'System_Usability',
            'comments': 'Test'
        })

def test_feedback_analysis(feedback_system, sample_feedback):
    """Test feedback analysis functionality."""
    # Add multiple feedback entries
    feedback_system.collect_feedback('HR', sample_feedback)
    feedback_system.collect_feedback('Candidate', {
        'satisfaction': 3,
        'category': 'Decision_Fairness',
        'comments': 'Fair process',
        'issues': None
    })
    
    analysis = feedback_system.analyze_feedback()
    assert isinstance(analysis, dict)
    assert 'overall_metrics' in analysis
    assert 'user_type_analysis' in analysis
    assert 'category_analysis' in analysis
    
    # Check metrics
    metrics = analysis['overall_metrics']
    assert metrics['total_feedback'] == 2
    assert 3 <= metrics['average_satisfaction'] <= 4
    assert isinstance(metrics['satisfaction_std'], float)

def test_timeframe_analysis(feedback_system, sample_feedback):
    """Test analysis with timeframe filtering."""
    # Add feedback with different timestamps
    old_feedback = sample_feedback.copy()
    feedback_system.collect_feedback('HR', old_feedback)
    
    # Manually adjust timestamp for testing
    feedback_system.feedback_data[0]['timestamp'] = datetime.now() - timedelta(days=40)
    
    # Add recent feedback
    feedback_system.collect_feedback('HR', sample_feedback)
    
    # Analyze last 30 days
    recent_analysis = feedback_system.analyze_feedback(timeframe_days=30)
    assert recent_analysis['overall_metrics']['total_feedback'] == 1
    
    # Analyze all time
    all_analysis = feedback_system.analyze_feedback()
    assert all_analysis['overall_metrics']['total_feedback'] == 2

def test_empty_feedback(feedback_system):
    """Test analysis with no feedback data."""
    analysis = feedback_system.analyze_feedback()
    assert analysis['status'] == 'No feedback data available'

def test_feedback_trends(feedback_system, sample_feedback):
    """Test feedback trend analysis."""
    # Add feedback over time
    for satisfaction in [4, 3, 5, 4]:
        feedback = sample_feedback.copy()
        feedback['satisfaction'] = satisfaction
        feedback_system.collect_feedback('HR', feedback)
    
    analysis = feedback_system.analyze_feedback()
    assert 'feedback_trend' in analysis['overall_metrics']
    trend = analysis['overall_metrics']['feedback_trend']
    assert isinstance(trend, dict)
    assert 'trend_direction' in trend
    assert 'trend_strength' in trend
