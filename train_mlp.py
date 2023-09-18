import json
from sklearn.preprocessing import StandardScaler

# Replace 'your_data.json' with the actual filename
with open('game_data.json', 'r') as json_file:
    data = json.load(json_file)


# Initialize empty lists to store features (game states) and target values (actions)
x_train = []
y_train = []

for item in data:
    game_state, action = item
    if action is not None:  # Filter out items where action is null
        x_train.append(game_state)
        y_train.append(action)

# Create a StandardScaler instance
scaler = StandardScaler()

# Fit the scaler to your training data and transform it
x_train = scaler.fit_transform(x_train)
print("done")