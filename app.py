from flask import Flask, render_template, request
from sympy import symbols, Eq, solve
import re

app = Flask(__name__)

# Function to add '*' between numbers and variables (e.g., convert '2x' to '2*x')
def preprocess_equation(equation):
    return re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation)

# Function to solve two linear equations
def solve_linear_equations(eq1_str, eq2_str):
    # Preprocess the equations to insert '*' where necessary
    eq1_str = preprocess_equation(eq1_str)
    eq2_str = preprocess_equation(eq2_str)

    # Define the variables
    x, y = symbols('x y')
    
    # Split the equations at '=' to handle both sides of the equation
    eq1_left, eq1_right = eq1_str.split('=')
    eq2_left, eq2_right = eq2_str.split('=')
    
    # Create sympy equations by converting strings into expressions
    eq1 = Eq(eval(eq1_left), eval(eq1_right))
    eq2 = Eq(eval(eq2_left), eval(eq2_right))
    
    # Solve the system of equations
    solution = solve((eq1, eq2), (x, y))
    
    return solution

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_equations():
    eq1 = request.form['equation1']
    eq2 = request.form['equation2']
    
    try:
        # Solve the equations using the provided function
        solution = solve_linear_equations(eq1, eq2)
        x_value = solution[symbols('x')]
        y_value = solution[symbols('y')]
        result = f"The solution is: x = {x_value}, y = {y_value}"
    except Exception as e:
        result = "Error: Invalid equations provided."
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=environ.get('PORT', 5000))
