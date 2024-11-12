import yaml
import pandas as pd
from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.warning(f"Failed to load config from {config_path}: {e}")
        return {}

def validate_data(data: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """Validate input data format and required columns."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")
        
    if required_columns:
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
    return True

def calculate_metrics(predictions: np.ndarray, actual: np.ndarray) -> Dict[str, float]:
    """Calculate various performance metrics."""
    return {
        'accuracy': accuracy_score(actual, predictions),
        'precision': precision_score(actual, predictions),
        'recall': recall_score(actual, predictions),
        'f1': f1_score(actual, predictions)
    }

def format_timestamp(timestamp: pd.Timestamp) -> str:
    """Format timestamp for consistent output."""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize input data to prevent injection attacks."""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(x) for x in data]
    elif isinstance(data, str):
        return data.replace('<', '&lt;').replace('>', '&gt;')
    else:
        return data
