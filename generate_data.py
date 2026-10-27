"""
Dataset Generator for Palo Alto Networks Workforce Attrition Analysis.
Generates a realistic 1,470-record enterprise cybersecurity workforce dataset
matching the exact 31 schema fields and reflecting empirical attrition patterns.
"""

import numpy as np
import pandas as pd
import os

def generate_attrition_dataset(n_samples=1470, seed=42):
    np.random.seed(seed)
    
    # 1. Demographics
    age = np.clip(np.random.normal(37, 8.5, n_samples).astype(int), 18, 60)
    gender = np.random.choice(["Male", "Female"], size=n_samples, p=[0.60, 0.40])
    marital_status = np.random.choice(["Single", "Married", "Divorced"], size=n_samples, p=[0.32, 0.46, 0.22])
    distance_from_home = np.clip(np.random.exponential(scale=8, size=n_samples).astype(int) + 1, 1, 29)
    
    education = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.11, 0.19, 0.39, 0.27, 0.04])
    education_field = np.random.choice(
        ["Technical Degree", "Life Sciences", "Medical", "Marketing", "Human Resources", "Other"],
        size=n_samples,
        p=[0.32, 0.28, 0.20, 0.11, 0.04, 0.05]
    )
    
    # 2. Departments & Roles (tailored to Palo Alto Networks Cybersecurity ecosystem)
    dept_choices = ["Research & Development", "Sales", "Human Resources"]
    department = np.random.choice(dept_choices, size=n_samples, p=[0.65, 0.30, 0.05])
    
    roles_rd = [
        "Security Research Engineer",
        "Laboratory Technician",
        "Research Scientist",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Research Director"
    ]
    roles_sales = ["Sales Executive", "Sales Representative", "Manager"]
    roles_hr = ["Human Resources", "Manager"]
    
    job_roles = []
    job_levels = []
    
    for dept in department:
        if dept == "Research & Development":
            role = np.random.choice(
                ["Research Scientist", "Security Research Engineer", "Laboratory Technician", 
                 "Manufacturing Director", "Research Director", "Manager"],
                p=[0.25, 0.30, 0.26, 0.10, 0.04, 0.05]
            )
            if role in ["Laboratory Technician", "Security Research Engineer"]:
                level = np.random.choice([1, 2, 3], p=[0.55, 0.35, 0.10])
            elif role == "Research Scientist":
                level = np.random.choice([1, 2, 3, 4], p=[0.30, 0.45, 0.20, 0.05])
            elif role == "Manufacturing Director":
                level = np.random.choice([2, 3, 4], p=[0.20, 0.50, 0.30])
            elif role == "Research Director":
                level = np.random.choice([3, 4, 5], p=[0.15, 0.50, 0.35])
            else: # Manager
                level = np.random.choice([4, 5], p=[0.60, 0.40])
        elif dept == "Sales":
            role = np.random.choice(["Sales Executive", "Sales Representative", "Manager"], p=[0.70, 0.22, 0.08])
            if role == "Sales Representative":
                level = 1
            elif role == "Sales Executive":
                level = np.random.choice([2, 3, 4], p=[0.60, 0.30, 0.10])
            else:
                level = np.random.choice([4, 5], p=[0.65, 0.35])
        else: # HR
            role = np.random.choice(["Human Resources", "Manager"], p=[0.80, 0.20])
            level = np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.30, 0.15, 0.10, 0.10])
            
        job_roles.append(role)
        job_levels.append(level)
        
    job_roles = np.array(job_roles)
    job_levels = np.array(job_levels)
    
    # 3. Workload & Mobility
    business_travel = np.random.choice(["Travel_Rarely", "Travel_Frequently", "Non-Travel"], size=n_samples, p=[0.71, 0.19, 0.10])
    overtime = np.random.choice(["Yes", "No"], size=n_samples, p=[0.28, 0.72])
    
    # 4. Tenure & Experience
    total_working_years = []
    years_at_company = []
    years_in_current_role = []
    years_since_promotion = []
    years_with_curr_manager = []
    num_companies_worked = []
    
    for i in range(n_samples):
        lvl = job_levels[i]
        ag = age[i]
        
        max_exp = max(1, ag - 18)
        min_exp = max(0, (lvl - 1) * 3)
        twy = int(np.clip(np.random.normal(min_exp + 5, 4), min_exp, max_exp))
        total_working_years.append(twy)
        
        yac = int(np.clip(np.random.uniform(0, twy), 0, twy))
        years_at_company.append(yac)
        
        yicr = int(np.clip(np.random.uniform(0, min(yac, 15)), 0, yac))
        years_in_current_role.append(yicr)
        
        yslp = int(np.clip(np.random.exponential(scale=2.5), 0, yac))
        years_since_promotion.append(yslp)
        
        ywcm = int(np.clip(np.random.uniform(0, min(yicr + 2, yac)), 0, yac))
        years_with_curr_manager.append(ywcm)
        
        ncw = int(np.clip(np.random.poisson(lam=2.5), 0, 9))
        num_companies_worked.append(ncw)
        
    total_working_years = np.array(total_working_years)
    years_at_company = np.array(years_at_company)
    years_in_current_role = np.array(years_in_current_role)
    years_since_promotion = np.array(years_since_promotion)
    years_with_curr_manager = np.array(years_with_curr_manager)
    num_companies_worked = np.array(num_companies_worked)
    
    # 5. Compensation & Financials
    # Base monthly income strongly correlated with JobLevel
    monthly_income = []
    for lvl in job_levels:
        if lvl == 1:
            inc = np.random.normal(2800, 500)
        elif lvl == 2:
            inc = np.random.normal(5500, 1000)
        elif lvl == 3:
            inc = np.random.normal(9500, 1500)
        elif lvl == 4:
            inc = np.random.normal(15000, 2000)
        else:
            inc = np.random.normal(19500, 1200)
        monthly_income.append(int(np.clip(inc, 1000, 20000)))
    monthly_income = np.array(monthly_income)
    
    daily_rate = np.random.randint(102, 1499, size=n_samples)
    hourly_rate = np.random.randint(30, 100, size=n_samples)
    monthly_rate = np.random.randint(2094, 26999, size=n_samples)
    
    percent_salary_hike = np.random.choice(range(11, 26), size=n_samples)
    performance_rating = np.where(percent_salary_hike >= 20, 4, 3)
    stock_option_level = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.43, 0.41, 0.11, 0.05])
    training_times_last_year = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=n_samples, p=[0.04, 0.08, 0.37, 0.34, 0.10, 0.05, 0.02])
    
    # 6. Satisfaction & Well-being Scores (1 to 4)
    environment_satisfaction = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.19, 0.20, 0.31, 0.30])
    job_involvement = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.06, 0.25, 0.59, 0.10])
    job_satisfaction = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.20, 0.19, 0.30, 0.31])
    relationship_satisfaction = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.19, 0.21, 0.31, 0.29])
    work_life_balance = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.06, 0.23, 0.61, 0.10])
    
    # 7. Model Attrition Probability (Realistic Log-Odds model matching real Palo Alto / IBM benchmark ~16.1%)
    # Risk factors: Overtime (strong+), Frequent Travel (+), Low Income / Level (+), Low Tenure (+),
    # Single (+), Long Distance (+), Low Environment/Job Satisfaction (+), Promotion Stagnation (+)
    z = (
        -1.45
        + (overtime == "Yes") * 1.35
        + (business_travel == "Travel_Frequently") * 0.85
        + (business_travel == "Travel_Rarely") * 0.20
        + (marital_status == "Single") * 0.80
        + (job_roles == "Sales Representative") * 1.10
        + (job_roles == "Laboratory Technician") * 0.50
        + (job_roles == "Security Research Engineer") * 0.25
        + (job_levels == 1) * 0.65
        - (job_levels >= 4) * 0.85
        - (monthly_income / 5000.0) * 0.45
        - (years_at_company < 2) * -0.75  # Early tenure higher risk
        + (distance_from_home > 15) * 0.55
        + (work_life_balance == 1) * 0.80
        + (job_satisfaction == 1) * 0.70
        + (environment_satisfaction == 1) * 0.65
        + (stock_option_level == 0) * 0.60
        - (stock_option_level > 0) * 0.35
        + (years_since_promotion > 4) * 0.40
        - (age > 40) * 0.40
    )
    
    prob = 1 / (1 + np.exp(-z))
    attrition_bool = np.random.binomial(1, prob)
    attrition = np.where(attrition_bool == 1, "Yes", "No")
    
    df = pd.DataFrame({
        "Age": age,
        "Attrition": attrition,
        "BusinessTravel": business_travel,
        "DailyRate": daily_rate,
        "Department": department,
        "DistanceFromHome": distance_from_home,
        "Education": education,
        "EducationField": education_field,
        "EnvironmentSatisfaction": environment_satisfaction,
        "Gender": gender,
        "HourlyRate": hourly_rate,
        "JobInvolvement": job_involvement,
        "JobLevel": job_levels,
        "JobRole": job_roles,
        "JobSatisfaction": job_satisfaction,
        "MaritalStatus": marital_status,
        "MonthlyIncome": monthly_income,
        "MonthlyRate": monthly_rate,
        "NumCompaniesWorked": num_companies_worked,
        "OverTime": overtime,
        "PercentSalaryHike": percent_salary_hike,
        "PerformanceRating": performance_rating,
        "RelationshipSatisfaction": relationship_satisfaction,
        "StockOptionLevel": stock_option_level,
        "TotalWorkingYears": total_working_years,
        "TrainingTimesLastYear": training_times_last_year,
        "WorkLifeBalance": work_life_balance,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_current_role,
        "YearsSinceLastPromotion": years_since_promotion,
        "YearsWithCurrManager": years_with_curr_manager
    })
    
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    df = generate_attrition_dataset()
    csv_path = os.path.join(out_dir, "palo_alto_attrition.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated successfully: {len(df)} records.")
    print(f"Attrition rate: {(df['Attrition'] == 'Yes').mean() * 100:.2f}%")
    print(f"Saved to: {csv_path}")
