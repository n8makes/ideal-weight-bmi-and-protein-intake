import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils import calculate_bmi, get_bmi_category, calculate_healthy_weight_range

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🏥",
    layout="wide"
)

# Load custom CSS
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-header'>BMI Calculator & Health Range Visualizer</h1>", unsafe_allow_html=True)

# Create two columns for unit selection and inputs
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    unit_system = st.radio(
        "Select Unit System",
        ('Metric', 'Imperial'),
        index=0
    )

    # Input fields based on unit system
    if unit_system == 'Metric':
        weight = st.number_input('Weight (kg)', min_value=0.0, max_value=500.0, value=70.0)
        height = st.number_input('Height (cm)', min_value=0.0, max_value=300.0, value=170.0)
    else:
        weight = st.number_input('Weight (lbs)', min_value=0.0, max_value=1000.0, value=154.0)
        height = st.number_input('Height (inches)', min_value=0.0, max_value=120.0, value=67.0)
    st.markdown("</div>", unsafe_allow_html=True)

# Calculate BMI
bmi = calculate_bmi(weight, height, unit_system.lower())
category, category_color = get_bmi_category(bmi)

# Calculate healthy weight range
if height > 0:
    min_weight, max_weight = calculate_healthy_weight_range(height, unit_system.lower())
    weight_unit = 'kg' if unit_system == 'Metric' else 'lbs'
    healthy_range = f"{min_weight} - {max_weight} {weight_unit}"
else:
    healthy_range = "N/A"

# Display results
with col2:
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    if bmi:
        st.markdown(f"<h2>Your BMI: {bmi}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>Category: <span style='color:{category_color}'>{category}</span></h3>", 
                   unsafe_allow_html=True)
        st.markdown(f"<p>Healthy weight range for your height: {healthy_range}</p>", 
                   unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Create BMI range visualization
st.markdown("<h3>BMI Range Visualization</h3>", unsafe_allow_html=True)

# Create BMI range chart
fig = go.Figure()

# BMI ranges
ranges = [
    (0, 18.5, 'Underweight', '#0DCAF0'),
    (18.5, 25, 'Normal', '#198754'),
    (25, 30, 'Overweight', '#FFC107'),
    (30, 40, 'Obese', '#DC3545')
]

# Add ranges to chart
for start, end, label, color in ranges:
    fig.add_trace(go.Scatter(
        x=[start, end],
        y=[1, 1],
        mode='lines',
        line=dict(color=color, width=20),
        name=label,
        hoverinfo='name+text',
        text=[f'BMI {start}-{end}'],
    ))

# Add marker for user's BMI
if bmi:
    fig.add_trace(go.Scatter(
        x=[bmi],
        y=[1],
        mode='markers',
        marker=dict(size=15, color='black', symbol='triangle-down'),
        name='Your BMI',
        hoverinfo='name+x'
    ))

# Update layout
fig.update_layout(
    showlegend=True,
    xaxis=dict(
        title='BMI',
        range=[15, 40],
        gridcolor='lightgray'
    ),
    yaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        range=[0.95, 1.05]
    ),
    height=200,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)

# Add information section
st.markdown("""
### BMI Categories:
- **Underweight**: BMI less than 18.5
- **Normal weight**: BMI between 18.5 and 24.9
- **Overweight**: BMI between 25 and 29.9
- **Obese**: BMI of 30 or greater

### Note:
BMI is a screening tool but not a diagnostic tool. Factors such as age, ethnicity, muscle mass, and sex can influence the relationship between body fat and BMI. Please consult with a healthcare provider for a complete health assessment.
""")
