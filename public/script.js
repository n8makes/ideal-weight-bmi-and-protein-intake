// BMI calculation functions
function calculateBMI(weight, height, unitSystem) {
    if (unitSystem === 'metric') {
        return (weight / ((height / 100) ** 2)).toFixed(1);
    } else {
        return ((703 * weight) / (height ** 2)).toFixed(1);
    }
}

function getBMICategory(bmi) {
    if (bmi < 18.5) return ['Underweight', '#0DCAF0'];
    if (bmi < 25) return ['Normal', '#198754'];
    if (bmi < 30) return ['Overweight', '#FFC107'];
    return ['Obese', '#DC3545'];
}

function calculateHealthyWeightRange(height, unitSystem, gender) {
    let minBMI = 18.5;
    let maxBMI = gender === 'male' ? 25.0 : 24.5;
    
    if (unitSystem === 'metric') {
        height = height / 100; // Convert cm to meters
        const minWeight = (minBMI * height * height).toFixed(1);
        const maxWeight = (maxBMI * height * height).toFixed(1);
        return [minWeight, maxWeight];
    } else {
        const minWeight = ((minBMI * (height ** 2)) / 703).toFixed(1);
        const maxWeight = ((maxBMI * (height ** 2)) / 703).toFixed(1);
        return [minWeight, maxWeight];
    }
}

function calculateProteinRequirement(idealWeight) {
    return Math.round(idealWeight);
}

// Chart initialization
let bmiChart = null;

function initializeChart() {
    const ctx = document.getElementById('bmiChart').getContext('2d');
    const ranges = [
        { min: 0, max: 18.5, label: 'Underweight', color: '#0DCAF0' },
        { min: 18.5, max: 25, label: 'Normal', color: '#198754' },
        { min: 25, max: 30, label: 'Overweight', color: '#FFC107' },
        { min: 30, max: 40, label: 'Obese', color: '#DC3545' }
    ];

    bmiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ranges.map(r => r.label),
            datasets: [{
                data: ranges.map(r => r.max - r.min),
                backgroundColor: ranges.map(r => r.color),
                barPercentage: 1,
                categoryPercentage: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 0,
                            yMax: 2,
                            borderColor: 'black',
                            borderWidth: 2,
                            display: false
                        }
                    }
                },
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const range = ranges[context.dataIndex];
                            return `BMI ${range.min}-${range.max}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    display: false,
                    max: 2
                }
            }
        }
    });
}

function updateBMIMarker(bmi) {
    if (bmiChart) {
        bmiChart.options.plugins.annotation.annotations.line1.xMin = bmi;
        bmiChart.options.plugins.annotation.annotations.line1.xMax = bmi;
        bmiChart.options.plugins.annotation.annotations.line1.display = true;
        bmiChart.update();
    }
}

// Event handlers and UI updates
function updateUI() {
    const unitSystem = document.querySelector('input[name="unit-system"]:checked').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    
    // Show/hide appropriate input fields
    document.getElementById('metric-inputs').style.display = unitSystem === 'metric' ? 'block' : 'none';
    document.getElementById('imperial-inputs').style.display = unitSystem === 'imperial' ? 'block' : 'none';
    
    // Calculate BMI
    let weight, height;
    if (unitSystem === 'metric') {
        weight = parseFloat(document.getElementById('weight-metric').value);
        height = parseFloat(document.getElementById('height-metric').value);
    } else {
        weight = parseFloat(document.getElementById('weight-imperial').value);
        const feet = parseFloat(document.getElementById('height-feet').value);
        const inches = parseFloat(document.getElementById('height-inches').value);
        height = feet * 12 + inches;
    }
    
    if (weight && height) {
        // Calculate BMI
        const bmi = calculateBMI(weight, height, unitSystem);
        const [category, color] = getBMICategory(bmi);
        
        // Calculate healthy weight range
        const [minWeight, maxWeight] = calculateHealthyWeightRange(height, unitSystem, gender);
        const unit = unitSystem === 'metric' ? 'kg' : 'lbs';
        
        // Calculate protein requirement
        const idealWeight = (parseFloat(minWeight) + parseFloat(maxWeight)) / 2;
        const idealWeightLbs = unitSystem === 'metric' ? idealWeight * 2.20462 : idealWeight;
        const proteinRequirement = calculateProteinRequirement(idealWeightLbs);
        
        // Update UI
        document.getElementById('bmi-value').textContent = bmi;
        document.getElementById('bmi-category').textContent = category;
        document.getElementById('bmi-category').style.color = color;
        document.getElementById('weight-range').textContent = `${minWeight} - ${maxWeight} ${unit}`;
        document.getElementById('protein-intake').textContent = proteinRequirement;
        
        // Update chart
        updateBMIMarker(bmi);
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeChart();
    
    // Add event listeners
    document.querySelectorAll('input[type="radio"], input[type="number"]').forEach(input => {
        input.addEventListener('change', updateUI);
    });
    
    // Initial UI update
    updateUI();
});
