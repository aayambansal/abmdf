# API Reference

## ABDMF Core Class

### Initialization
```python
from abdmf import ABDMF

system = ABDMF(config_path: str = None)
```

Parameters:
- `config_path`: Optional path to YAML configuration file

### Methods

#### scan_historical_data
```python
def scan_historical_data(data: pd.DataFrame) -> Dict[str, Any]
```
Scans historical hiring data for bias patterns.

Parameters:
- `data`: DataFrame containing historical hiring data
  - Required columns: 'selected' and protected attributes
  - Additional columns used for decision analysis

Returns:
- Dictionary containing:
  - `bias_scan`: Detailed bias metrics
  - `model_metrics`: Model performance metrics
  - `timestamp`: Analysis timestamp

#### evaluate_candidate
```python
def evaluate_candidate(candidate_data: pd.DataFrame) -> Dict[str, Any]
```
Evaluates a candidate while checking for potential bias.

Parameters:
- `candidate_data`: DataFrame containing candidate information

Returns:
- Dictionary containing:
  - `decision_analysis`: Decision details and confidence
  - `protected_attributes`: Detected protected attributes
  - `timestamp`: Evaluation timestamp

## BiasDetector Class

### Methods

#### detect_bias
```python
def detect_bias(data: pd.DataFrame) -> Dict[str, Dict[str, float]]
```
Detects bias across protected attributes.

Parameters:
- `data`: DataFrame containing hiring decisions

Returns:
- Dictionary of bias metrics per attribute

#### analyze_intersectional_bias
```python
def analyze_intersectional_bias(
    data: pd.DataFrame,
    attributes: List[str]
) -> Dict[str, float]
```
Analyzes intersectional bias across multiple attributes.

## DecisionAnalyzer Class

### Methods

#### train
```python
def train(
    features: pd.DataFrame,
    decisions: pd.Series,
    validation_split: float = 0.2
) -> Dict[str, Any]
```
Trains the decision analyzer model.

#### analyze_decision
```python
def analyze_decision(
    candidate_features: pd.DataFrame
) -> Dict[str, Any]
```
Analyzes a hiring decision with explanation.

## FeedbackSystem Class

### Methods

#### collect_feedback
```python
def collect_feedback(
    user_type: str,
    feedback: Dict[str, Any]
) -> bool
```
Collects user feedback for system improvement.

#### analyze_feedback
```python
def analyze_feedback(
    timeframe_days: int = None
) -> Dict[str, Any]
```
Analyzes collected feedback for patterns.
