from app.calibration.validation_models import MatchStatus
from app.calibration.validation_workspace import ValidationWorkspace
import json

def test_validation_workspace():
    print("Testing Validation Workspace...")
    workspace = ValidationWorkspace("test_workspace.json")
    
    print("1. Creating Validation Case...")
    case1 = workspace.create_case(
        case_id="CASE_001",
        native_name="John Doe",
        canonical_json_path="test_data.json",
        birth_details={"dob": "2000-01-01", "time": "12:00"},
        reviewer="Admin"
    )
    print(f"Case Created: {case1.case_id}")
    
    print("2. Recording Comparisons...")
    workspace.record_comparison("CASE_001", "planet_strength", expected={"sun": 80}, actual={"sun": 80}, status=MatchStatus.MATCH)
    workspace.record_comparison("CASE_001", "house_strength", expected={"1": 70}, actual={"1": 50}, status=MatchStatus.MISMATCH)
    workspace.record_comparison("CASE_001", "master_probability", expected=80, actual=75, status=MatchStatus.PARTIAL)
    print("Comparisons Recorded.")
    
    print("3. Checking Accuracy Dashboard...")
    metrics = workspace.calculate_accuracy()
    print(f"Metrics: {metrics.model_dump_json(indent=2)}")
    assert metrics.total_matches == 1
    assert metrics.total_mismatches == 1
    assert metrics.total_partial == 1
    assert metrics.planet_strength_accuracy == 100.0
    assert metrics.house_strength_accuracy == 0.0
    
    print("4. Recording Calibration Recommendation...")
    workspace.record_recommendation(
        param="house_strength_multiplier",
        old_val=1.0,
        new_val=1.2,
        reason="Boost house 1 strength",
        supporting=["CASE_001"]
    )
    print("Recommendation Recorded.")
    
    print("5. Recording Regression Analysis...")
    workspace.record_regression_analysis(
        param="house_strength_multiplier",
        improved=["CASE_001"],
        unchanged=["CASE_002"],
        regressed=[]
    )
    print("Regression Recorded.")
    
    print("6. Approving Calibration...")
    workspace.approve_recommendation("house_strength_multiplier", version="v1.0.1")
    print("Calibration History:")
    print(workspace.data.history[0].model_dump_json(indent=2))
    
    print("\nSUCCESS: All Workspace Tests Passed!")
    
if __name__ == "__main__":
    test_validation_workspace()
