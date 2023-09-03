import pandas as pd
import pulp

# Read the CSV file containing food data
food_data = pd.read_csv('food_data.csv')

# Define the nutrients and their requirements
nutrient_requirements = {
    'Protein (g)': 150,
    'Carbohydrates (g)': 300,
    'Fat (g)': 70,
    'Vitamin A (IU)': 4000,
    'Vitamin C (mg)': 90,
    'Calcium (mg)': 1300,
    'Iron (mg)': 18,
    'Zinc (mg)': 11,        # Add nutrient requirements for Zinc
    'Iodine (µg)': 150,     # Add nutrient requirements for Iodine
    'Copper (mg)': 2,       # Add nutrient requirements for Copper
    'Magnesium (mg)': 400,  # Add nutrient requirements for Magnesium
    'Manganese (mg)': 2.3,  # Add nutrient requirements for Manganese
    'Vitamin B1 (mg)': 1.1, # Add nutrient requirements for Vitamin B1
    'Vitamin B2 (mg)': 1.3, # Add nutrient requirements for Vitamin B2
    'Vitamin B3 (mg)': 16,   # Add nutrient requirements for Vitamin B3
    'Vitamin B5 (mg)': 5,    # Add nutrient requirements for Vitamin B5
    'Vitamin B6 (mg)': 1.3,  # Add nutrient requirements for Vitamin B6
    'Vitamin B7 (µg)': 30,   # Add nutrient requirements for Vitamin B7
    'Vitamin B9 (µg)': 400,  # Add nutrient requirements for Vitamin B9
    'Vitamin B12 (µg)': 2.4, # Add nutrient requirements for Vitamin B12
    'Vitamin D (IU)': 600,   # Add nutrient requirements for Vitamin D
    'Vitamin E (mg)': 15,    # Add nutrient requirements for Vitamin E
    #'Vitamin K (µg)': 120,    # Add nutrient requirements for Vitamin K
    'Calories (kcal)': None,  # We will minimize this
    
}

# Define maximum values for specific foods (in grams)
max_values = {
    'Apple': 200,    # Example: Maximum 200 grams of apples allowed
    'Banana': 150,   # Example: Maximum 150 grams of bananas allowed
}

# Create a linear programming problem
prob = pulp.LpProblem("DietOptimization", pulp.LpMinimize)

# Define decision variables (quantity of each food item to include)
food_vars = pulp.LpVariable.dicts("Food", food_data.index, lowBound=0, cat='Continuous')


# Define the objective function: minimize calorie consumption
prob += pulp.lpSum([food_data.at[i, 'Calories (kcal)'] * food_vars[i] for i in food_data.index]), "Total_Calories"

# Add nutrient constraint equations
for nutrient, requirement in nutrient_requirements.items():
    if requirement is not None:
        prob += pulp.lpSum([food_data.at[i, nutrient] * food_vars[i] for i in food_data.index]) >= requirement, nutrient

# # Add constraints to limit the quantity of specific foods
# for food, max_quantity in max_values.items():
#     if max_quantity is not None:
#         prob += pulp.lpSum([food_data.at[i, nutrient] * food_vars[i] for i in food_data.index]) <= max_quantity, food
    #index = food_data[food_data['Grocery'] == food].index[0]
    #prob += food_vars[index] <= max_quantity, f"Max_{food}"

# Solve the linear programming problem
prob.solve()

# Print the status of the optimization
print("Status:", pulp.LpStatus[prob.status])

# Print the optimized diet
print("\nOptimized Diet:")
for i in food_data.index:
    if food_vars[i].varValue > 0:
        print(f"{i}: {food_data.at[i, 'Grocery']}: {food_vars[i].varValue*100} grams")

# Print the total calorie consumption
print("\nTotal Calories:", pulp.value(prob.objective))
