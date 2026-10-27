"""
Enterprise Data Processing, Cleaning & Feature Engineering Pipeline
Palo Alto Networks Workforce Analytics & Organizational Network Analysis (ONA)
"""

import pandas as pd
import numpy as np
import io

def clean_and_engineer_features(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans raw HR attrition data, deduplicates, and creates rich engineered features
    for statistical modeling, industry benchmarking, and network analysis.
    """
    initial_rows = len(df)
    initial_cols = len(df.columns)
    
    # 1. Deduplication
    df = df.drop_duplicates()
    rows_deduped = initial_rows - len(df)
    
    # 2. Check & drop duplicate/constant columns
    cols_to_drop = []
    for col in df.columns:
        if df[col].nunique() <= 1:
            cols_to_drop.append(col)
    
    # Redundant / administrative constant columns standard in IBM/HR datasets
    known_constants = ["EmployeeCount", "StandardHours", "Over18"]
    for c in known_constants:
        if c in df.columns and c not in cols_to_drop:
            cols_to_drop.append(c)
            
    df = df.drop(columns=cols_to_drop, errors="ignore")
    
    # 3. Missing Value Imputation (Enterprise robustness)
    for col in df.columns:
        if df[col].isnull().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
                
    # 4. Standardize Target Variable (Robust to object, string[pyarrow], int, float, bool)
    attrition_raw = df["Attrition"].astype(str).str.strip().str.capitalize()
    df["Attrition_Numeric"] = attrition_raw.map({
        "Yes": 1, "1": 1, "True": 1, "1.0": 1,
        "No": 0, "0": 0, "False": 0, "0.0": 0
    }).fillna(0).astype(int)
    df["Attrition_Label"] = df["Attrition_Numeric"].map({1: "Yes", 0: "No"})

    # 5. Feature Engineering
    
    # A. Age Cohorts
    age_bins = [17, 25, 34, 44, 54, 75]
    age_labels = ["<25 (Gen-Z Entry)", "25-34 (Millennial Core)", "35-44 (Mid-Career)", "45-54 (Senior Leaders)", "55+ (Veterans)"]
    df["Age_Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, include_lowest=True)
    
    # B. Tenure Horizons
    tenure_bins = [-1, 2, 5, 10, 50]
    tenure_labels = ["0-2 yrs (Critical Onboarding)", "3-5 yrs (Mid-Tenure)", "6-10 yrs (Experienced)", "10+ yrs (Veterans)"]
    df["Tenure_Horizon"] = pd.cut(df["YearsAtCompany"], bins=tenure_bins, labels=tenure_labels)
    
    # C. Commute Distance Risk Tiers
    commute_bins = [-1, 5, 15, 60]
    commute_labels = ["Short Commute (0-5 mi)", "Moderate (6-15 mi)", "High-Friction (>15 mi)"]
    df["Commute_Tier"] = pd.cut(df["DistanceFromHome"], bins=commute_bins, labels=commute_labels)
    
    # D. Education Mapping
    edu_map = {1: "Below College", 2: "College / Associate", 3: "Bachelor's Degree", 4: "Master's Degree", 5: "Doctorate"}
    df["Education_Level_Label"] = df["Education"].map(edu_map)
    
    # E. Promotion Stagnation Flag
    # High risk when an employee has spent >3 years in role without a promotion
    df["Promotion_Stagnant"] = np.where(
        (df["YearsInCurrentRole"] >= 3) & (df["YearsSinceLastPromotion"] >= 3),
        "Stagnant (≥3 Yrs)",
        "Active Progression"
    )
    
    # F. Manager Relationship Continuity Ratio
    # Safe division: ratio of years with manager relative to tenure at company
    df["Manager_Continuity_Ratio"] = np.where(
        df["YearsAtCompany"] > 0,
        np.clip(df["YearsWithCurrManager"] / df["YearsAtCompany"], 0.0, 1.0),
        1.0
    )
    
    # G. Comprehensive Workload & Burnout Index (0.0 to 3.0 scale)
    # Weights: Overtime (1.2) + Travel Frequency (0.8) + Low WorkLifeBalance (0.6) + Long Commute (0.4)
    ot_score = (df["OverTime"].astype(str).str.strip().str.capitalize() == "Yes").astype(float) * 1.2
    travel_map = {"Travel_Frequently": 0.8, "Travel_Rarely": 0.3, "Non-Travel": 0.0}
    travel_score = df["BusinessTravel"].astype(str).str.strip().map(travel_map).fillna(0.3)
    wlb_score = np.where(df["WorkLifeBalance"] <= 2, 0.6, 0.0)
    commute_score = np.where(df["DistanceFromHome"] > 15, 0.4, 0.0)
    df["Burnout_Index"] = np.round(ot_score + travel_score + wlb_score + commute_score, 2)
    
    # H. Composite Attrition Flight Risk Classification
    # Score combining Burnout Index, Low Salary Level, Single Status, and Stagnation
    risk_score = (
        (df["Burnout_Index"] >= 1.5).astype(int) * 35 +
        (df["YearsAtCompany"] <= 2).astype(int) * 25 +
        (df["Promotion_Stagnant"] == "Stagnant (≥3 Yrs)").astype(int) * 20 +
        (df["MaritalStatus"] == "Single").astype(int) * 10 +
        (df["JobSatisfaction"] <= 2).astype(int) * 10
    )
    df["Risk_Score"] = np.clip(risk_score, 5, 95)
    df["Risk_Tier"] = pd.cut(
        df["Risk_Score"],
        bins=[-1, 35, 65, 100],
        labels=["Low Risk (Stable)", "Medium Risk (Monitor)", "High Flight Risk (Urgent Action)"]
    )
    
    # Summary telemetry metadata
    telemetry = {
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "duplicates_removed": rows_deduped,
        "dropped_constant_columns": cols_to_drop,
        "new_features_engineered": [
            "Attrition_Label", "Attrition_Numeric", "Age_Group", "Tenure_Horizon",
            "Commute_Tier", "Education_Level_Label", "Promotion_Stagnant",
            "Manager_Continuity_Ratio", "Burnout_Index", "Risk_Score", "Risk_Tier"
        ]
    }
    
    return df, telemetry
