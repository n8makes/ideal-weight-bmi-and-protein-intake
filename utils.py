import numpy as np

def calculate_bmi(weight, height, unit_system='metric'):
    """Calculate BMI based on weight and height."""
    try:
        if unit_system == 'metric':
            bmi = weight / (height/100)**2
        else:  # imperial
            bmi = (weight * 703) / (height**2)
        return round(bmi, 1)
    except:
        return None

def get_bmi_category(bmi):
    """Return BMI category and color based on BMI value."""
    if bmi is None:
        return "N/A", "#6C757D"
    elif bmi < 18.5:
        return "Underweight", "#0DCAF0"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "#198754"
    elif 25 <= bmi < 30:
        return "Overweight", "#FFC107"
    else:
        return "Obese", "#DC3545"

def calculate_healthy_weight_range(height, unit_system='metric'):
    """Calculate healthy weight range for given height."""
    if unit_system == 'metric':
        min_weight = 18.5 * (height/100)**2
        max_weight = 24.9 * (height/100)**2
        return round(min_weight, 1), round(max_weight, 1)
    else:
        min_weight = (18.5 * (height**2)) / 703
        max_weight = (24.9 * (height**2)) / 703
        return round(min_weight, 1), round(max_weight, 1)
