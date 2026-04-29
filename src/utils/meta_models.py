import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from itertools import product


def fit_MLR_model(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Standardize the features for better training stability
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)


    # Define a simple linear regression model
    class LinearRegressionModel(nn.Module):
        def __init__(self, input_dim, output_dim):
            super(LinearRegressionModel, self).__init__()
            self.linear = nn.Linear(input_dim, output_dim)  # Linear layer

        def forward(self, x):
            return self.linear(x)


    # Model setup
    input_dim = X.shape[1]  # 4 features
    output_dim = Y.shape[1]  # 3 target variables
    model = LinearRegressionModel(input_dim, output_dim)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer for stability

    # Training loop
    epochs = 500
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 5 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))




    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])

def fit_NN_model(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Standardize the features for better training stability
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define a simple neural network model
    class NeuralNet(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(NeuralNet, self).__init__()
            self.hidden1 = nn.Linear(input_dim, hidden_dim)  # Hidden layer 1
            self.hidden2 = nn.Linear(hidden_dim, hidden_dim)  # Hidden layer 2
            self.output = nn.Linear(hidden_dim, output_dim)  # Output layer
            self.relu = nn.ReLU()  # Activation function

        def forward(self, x):
            x = self.relu(self.hidden1(x))  # Apply ReLU after first layer
            x = self.relu(self.hidden2(x))  # Apply ReLU after second layer
            x = self.output(x)  # Final output
            return x

    # Model setup
    input_dim = X.shape[1]  # 4 features
    hidden_dim = 32  # Number of neurons in hidden layers
    output_dim = Y.shape[1]  # 3 target variables
    model = NeuralNet(input_dim, hidden_dim, output_dim)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer

    # Training loop
    epochs = 500
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 5 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))

    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())






    # Define the bounds
    bounds = {
        "q_dt": (4, 120),
        "energy_density": (30e9, 120e9),
        "layer_thickness": (30e-6, 120e-6),
        "T_bottom": (273.15 + 25, 273.15 + 400),
    }

    # Generate 15 levels for each variable
    levels = {key: np.linspace(start, end, 15) for key, (start, end) in bounds.items()}

    # Create a full factorial DOE
    doe_extend = list(product(*levels.values()))

    # Create a DataFrame
    df_extend = pd.DataFrame(doe_extend, columns=['q_dt', 'energy_density', 'layer_thickness', 'T_bottom'])

    X_extend = df_extend[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features

    X_scaled_extend = scaler_X.fit_transform(X_extend)

    X_tensor_extend = torch.tensor(X_scaled_extend, dtype=torch.float32)

    Y_all_pred_extend = model(X_tensor_extend)

    Y_all_pred_extend_original = scaler_Y.inverse_transform(Y_all_pred_extend.detach().numpy())

    # Create a DataFrame for Y_all_pred_extend_original with specified column titles
    df_Y_all_pred_extend = pd.DataFrame(Y_all_pred_extend_original, columns=['x_b', 'x_as', 'x_am'])

    # Merge df_extend with df_Y_all_pred_extend
    df_merged = pd.concat([df_extend, df_Y_all_pred_extend], axis=1)

    # Save the DataFrame to a CSV file
    df_merged.to_csv("results_extended.csv", index=False)

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_NN_model02(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Standardize the features for better training stability
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define a more complex neural network model
    class NeuralNet(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super(NeuralNet, self).__init__()
            self.hidden1 = nn.Linear(input_dim, hidden_dim)  # Hidden layer 1
            self.bn1 = nn.BatchNorm1d(hidden_dim)  # Batch normalization 1
            self.hidden2 = nn.Linear(hidden_dim, hidden_dim * 2)  # Hidden layer 2 (more neurons)
            self.bn2 = nn.BatchNorm1d(hidden_dim * 2)  # Batch normalization 2
            self.hidden3 = nn.Linear(hidden_dim * 2, hidden_dim)  # Hidden layer 3
            self.bn3 = nn.BatchNorm1d(hidden_dim)  # Batch normalization 3
            self.output = nn.Linear(hidden_dim, output_dim)  # Output layer
            self.relu = nn.ReLU()  # Activation function
            self.dropout = nn.Dropout(0.3)  # Dropout to prevent overfitting

        def forward(self, x):
            x = self.relu(self.bn1(self.hidden1(x)))  # Hidden layer 1
            x = self.dropout(x)  # Apply dropout
            x = self.relu(self.bn2(self.hidden2(x)))  # Hidden layer 2
            x = self.dropout(x)  # Apply dropout
            x = self.relu(self.bn3(self.hidden3(x)))  # Hidden layer 3
            x = self.output(x)  # Final output layer
            return x

    # Model setup
    input_dim = X.shape[1]  # 4 features
    hidden_dim = 64  # Increased number of neurons in hidden layers
    output_dim = Y.shape[1]  # 3 target variables
    model = NeuralNet(input_dim, hidden_dim, output_dim)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer

    # Training loop
    epochs = 500
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 5 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])

def fit_NN_sigmoid(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Standardize the features for better training stability
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define the sigmoid-based model
    class SigmoidFittingModel(nn.Module):
        def __init__(self):
            super(SigmoidFittingModel, self).__init__()

            # Define learnable parameters for each target variable
            self.a_b = nn.Parameter(torch.randn(1))
            self.b_b = nn.Parameter(torch.randn(1))
            self.c_b = nn.Parameter(torch.randn(1))
            self.d_b = nn.Parameter(torch.randn(1))
            self.e_b = nn.Parameter(torch.randn(1))

            self.a_as = nn.Parameter(torch.randn(1))
            self.b_as = nn.Parameter(torch.randn(1))
            self.c_as = nn.Parameter(torch.randn(1))
            self.d_as = nn.Parameter(torch.randn(1))
            self.e_as = nn.Parameter(torch.randn(1))

            self.a_am = nn.Parameter(torch.randn(1))
            self.b_am = nn.Parameter(torch.randn(1))
            self.c_am = nn.Parameter(torch.randn(1))
            self.d_am = nn.Parameter(torch.randn(1))
            self.e_am = nn.Parameter(torch.randn(1))

        def forward(self, x):
            q_dt, energy_density, layer_thickness, T_bottom = x[:, 0], x[:, 1], x[:, 2], x[:, 3]

            # Sigmoid-based equations for each target variable
            x_b = self.e_b * torch.sigmoid((self.d_b * q_dt) * (self.a_b * energy_density + self.b_b * T_bottom + self.c_b * layer_thickness))
            x_as = self.e_as * torch.sigmoid((self.d_as * q_dt) * (self.a_as * energy_density + self.b_as * T_bottom + self.c_as * layer_thickness))
            x_am = self.e_am * torch.sigmoid((self.d_am * q_dt) * (self.a_am * energy_density + self.b_am * T_bottom + self.c_am * layer_thickness))

            return torch.stack([x_b, x_as, x_am], dim=1)

    # Model setup
    # input_dim = X.shape[1]  # 4 features
    # hidden_dim = 64  # Increased number of neurons in hidden layers
    # output_dim = Y.shape[1]  # 3 target variables
    model = model = SigmoidFittingModel()

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer

    loss_values = []

    # Training loop
    epochs = 4000
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_values.append(loss.item())

        if epoch % 5 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Plot the loss values
    plt.figure(figsize=(10, 5))
    plt.plot(loss_values, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss per Epoch')
    plt.legend()
    plt.show()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_NN_sigmoid02(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Normalize inputs and outputs (Min-Max Scaling)
    scaler_X = MinMaxScaler()
    scaler_Y = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define the sigmoid-based model
    class SigmoidFittingModel(nn.Module):
        def __init__(self):
            super(SigmoidFittingModel, self).__init__()

            # Learnable parameters for x_b
            self.a_b = nn.Parameter(torch.randn(1))
            self.b_b = nn.Parameter(torch.randn(1))
            self.c_b = nn.Parameter(torch.randn(1))
            self.d_b = nn.Parameter(torch.randn(1))
            self.e_b = nn.Parameter(torch.randn(1))
            self.f_b = nn.Parameter(torch.randn(1))  # New parameter

            # Learnable parameters for x_as
            self.a_as = nn.Parameter(torch.randn(1))
            self.b_as = nn.Parameter(torch.randn(1))
            self.c_as = nn.Parameter(torch.randn(1))
            self.d_as = nn.Parameter(torch.randn(1))
            self.e_as = nn.Parameter(torch.randn(1))
            self.f_as = nn.Parameter(torch.randn(1))  # New parameter

            # Learnable parameters for x_am
            self.a_am = nn.Parameter(torch.randn(1))
            self.b_am = nn.Parameter(torch.randn(1))
            self.c_am = nn.Parameter(torch.randn(1))
            self.d_am = nn.Parameter(torch.randn(1))
            self.e_am = nn.Parameter(torch.randn(1))
            self.f_am = nn.Parameter(torch.randn(1))  # New parameter

        def forward(self, x):
            q_dt, energy_density, layer_thickness, T_bottom = x[:, 0], x[:, 1], x[:, 2], x[:, 3]

            # Updated sigmoid equations with additional f parameter
            x_b = self.e_b * torch.sigmoid(
                (self.d_b * q_dt) * (self.a_b * energy_density + self.b_b * T_bottom + self.c_b * layer_thickness) + self.f_b)
            x_as = self.e_as * torch.sigmoid(
                (self.d_as * q_dt) * (self.a_as * energy_density + self.b_as * T_bottom + self.c_as * layer_thickness) + self.f_as)
            x_am = self.e_am * torch.sigmoid(
                (self.d_am * q_dt) * (self.a_am * energy_density + self.b_am * T_bottom + self.c_am * layer_thickness) + self.f_am)

            return torch.stack([x_b, x_as, x_am], dim=1)

    model = SigmoidFittingModel()

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer

    loss_values = []

    # Training loop
    epochs = 4000
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_values.append(loss.item())

        if epoch % 5 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Plot the loss values
    plt.figure(figsize=(10, 5))
    plt.plot(loss_values, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss per Epoch')
    plt.legend()
    plt.show()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_NN_sigmoid03(df_input, row_val, col_val, coly_value):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables (Only using energy_density)
    X = df[['energy_density']].values  # Only energy_density as input
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Normalize inputs and outputs (Min-Max Scaling)
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)

    scaler_Y = MinMaxScaler(feature_range=(Y.max(), Y.min()))
    Y_scaled = scaler_Y.fit_transform(Y)


    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define the sigmoid-based model
    class SigmoidFittingModel(nn.Module):
        def __init__(self):
            super(SigmoidFittingModel, self).__init__()

            # # Learnable parameters for x_b
            # self.a_b = nn.Parameter(torch.randn(1))
            # self.b_b = nn.Parameter(torch.randn(1))
            # self.c_b = nn.Parameter(torch.randn(1))
            # self.d_b = nn.Parameter(torch.randn(1))
            #
            # # Learnable parameters for x_as
            # self.a_as = nn.Parameter(torch.randn(1))
            # self.b_as = nn.Parameter(torch.randn(1))
            # self.c_as = nn.Parameter(torch.randn(1))
            # self.d_as = nn.Parameter(torch.randn(1))
            #
            # # Learnable parameters for x_am
            # self.a_am = nn.Parameter(torch.randn(1))
            # self.b_am = nn.Parameter(torch.randn(1))
            # self.c_am = nn.Parameter(torch.randn(1))
            # self.d_am = nn.Parameter(torch.randn(1))

            # Learnable parameters for x_b
            self.a_b = nn.Parameter(torch.randn(1))
            self.b_b = nn.Parameter(torch.randn(1))
            self.c_b = nn.Parameter(torch.randn(1))
            self.d_b = nn.Parameter(torch.randn(1))

            # Learnable parameters for x_as
            self.a_as = nn.Parameter(torch.randn(1))
            self.b_as = nn.Parameter(torch.randn(1))
            self.c_as = nn.Parameter(torch.randn(1))
            self.d_as = nn.Parameter(torch.randn(1))

            # Learnable parameters for x_am
            self.a_am = nn.Parameter(torch.randn(1))
            self.b_am = nn.Parameter(torch.randn(1))
            self.c_am = nn.Parameter(torch.randn(1))
            self.d_am = nn.Parameter(torch.randn(1))


        def forward(self, x):
            energy_density = x[:, 0]  # Extract energy_density

            # Updated sigmoid equations
            x_b = self.a_b * torch.sigmoid(self.b_b * (energy_density + self.c_b)) + self.d_b
            x_as = self.a_as * torch.sigmoid(self.b_as * (energy_density + self.c_as)) + self.d_as
            x_am = self.a_am * torch.sigmoid(self.b_am * (energy_density + self.c_am)) + self.d_am

            return torch.stack([x_b, x_as, x_am], dim=1)

    model = SigmoidFittingModel()

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    criterion_insight = nn.MSELoss(reduction="none")
    optimizer = optim.Adam(model.parameters(), lr=0.1)  # Adam optimizer

    loss_values = []
    loss_insight_values = []

    # Training loop
    epochs = 1000
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)
        loss_insight = criterion_insight(predictions.detach(), Y_train.detach()).sum(dim=0)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_values.append(loss.item())
        loss_insight_values.append(loss_insight)

        # if epoch % (epochs+1) == 0:  # Print loss every 50 epochs
        #     print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Plot the loss values
    plt.figure(figsize=(10, 5))
    plt.plot(loss_values, label='Training Loss', c="black")
    for i, label in enumerate(['x_b', 'x_as', 'x_am']):
        plt.plot([loss[i] for loss in loss_insight_values], label=label, color=["#2171b5", "#238b45", "#d7301f"][i])
    # plt.plot(loss_insight_values, label=["x_b", "x_as", "x_am"], color=["#2171b5", "#238b45", "#d7301f"])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.yscale('log')
    plt.ylim(1e-3,1e1)
    plt.title('Training Loss per Epoch')
    plt.legend(loc="bottom left")
    plt.show()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        # print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    # print("\nSample Predictions (First 5 rows):")
    # print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    loss_insight_all = criterion_insight(Y_all_pred.detach(), Y_tensor.detach()).sum(dim=0)

    # Print the final learned parameters
    x_b_string = f"{model.a_b.item()}, {model.b_b.item()}, {model.c_b.item()}, {model.d_b.item()}"
    x_as_string = f"{model.a_as.item()}, {model.b_as.item()}, {model.c_as.item()}, {model.d_as.item()}"
    x_am_string = f"{model.a_am.item()}, {model.b_am.item()}, {model.c_am.item()}, {model.d_am.item()}"

    print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_NN_sigmoid04(df_input, row_val, col_val, coly_value):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables (Only using energy_density)
    X = df[['energy_density']].values  # Only energy_density as input
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Normalize inputs and outputs (Min-Max Scaling)
    scaler_X = MinMaxScaler()
    scaler_Y = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

    # Define the sigmoid-based model
    class SigmoidFittingModel(nn.Module):
        def __init__(self):
            super(SigmoidFittingModel, self).__init__()

            # Learnable parameters for x_b
            self.a_b = nn.Parameter(torch.randn(1))
            self.b_b = nn.Parameter(torch.randn(1))
            self.c_b = nn.Parameter(torch.randn(1))
            self.d_b = nn.Parameter(torch.randn(1))

            # Learnable parameters for x_as
            self.a_as = nn.Parameter(torch.randn(1))
            self.b_as = nn.Parameter(torch.randn(1))
            self.c_as = nn.Parameter(torch.randn(1))
            self.d_as = nn.Parameter(torch.randn(1))

            # Learnable parameters for x_am
            self.a_am = nn.Parameter(torch.randn(1))
            self.b_am = nn.Parameter(torch.randn(1))
            self.c_am = nn.Parameter(torch.randn(1))
            self.d_am = nn.Parameter(torch.randn(1))

        def forward(self, x):
            energy_density = x[:, 0]  # Extract energy_density

            # Updated sigmoid equations
            x_b = self.a_b * torch.sigmoid(self.b_b * (energy_density + self.c_b)) + self.d_b
            x_as = self.a_as * torch.sigmoid(self.b_as * (energy_density + self.c_as)) + self.d_as
            x_am = self.a_am * torch.sigmoid(self.b_am * (energy_density + self.c_am)) + self.d_am

            x_b = self.a_b * torch.sigmoid(self.b_b * (energy_density + self.c_b)) + self.d_b
            x_as = self.a_as * torch.sigmoid(self.b_as * (energy_density + self.c_as)) + self.d_as
            x_am = self.a_am * torch.sigmoid(self.b_am * (energy_density + self.c_am)) + self.d_am

            return torch.stack([x_b, x_as, x_am], dim=1)

    model = SigmoidFittingModel()

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    criterion_insight = nn.MSELoss(reduction="none")
    optimizer = optim.Adam(model.parameters(), lr=0.1)  # Adam optimizer

    loss_values = []
    loss_insight_values = []

    # Training loop
    epochs = 1000
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)
        loss_insight = criterion_insight(predictions.detach(), Y_train.detach()).sum(dim=0)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_values.append(loss.item())
        loss_insight_values.append(loss_insight)

        # if epoch % (epochs+1) == 0:  # Print loss every 50 epochs
        #     print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Plot the loss values
    plt.figure(figsize=(10, 5))
    plt.plot(loss_values, label='Training Loss', c="black")
    for i, label in enumerate(['x_b', 'x_as', 'x_am']):
        plt.plot([loss[i] for loss in loss_insight_values], label=label, color=["#2171b5", "#238b45", "#d7301f"][i])
    # plt.plot(loss_insight_values, label=["x_b", "x_as", "x_am"], color=["#2171b5", "#238b45", "#d7301f"])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.yscale('log')
    plt.ylim(1e-3,1e1)
    plt.title('Training Loss per Epoch')
    plt.legend(loc="bottom left")
    plt.show()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        # print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    # print("\nSample Predictions (First 5 rows):")
    # print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    loss_insight_all = criterion_insight(Y_all_pred.detach(), Y_tensor.detach()).sum(dim=0)

    # Print the final learned parameters
    x_b_string = f"{model.a_b.item()}, {model.b_b.item()}, {model.c_b.item()}, {model.d_b.item()}"
    x_as_string = f"{model.a_as.item()}, {model.b_as.item()}, {model.c_as.item()}, {model.d_as.item()}"
    x_am_string = f"{model.a_am.item()}, {model.b_am.item()}, {model.c_am.item()}, {model.d_am.item()}"

    print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_polynomial_reg_model(df_input):
    # Load your dataframe
    df = df_input.copy()

    # Define input (X) and output (Y) variables
    X = df[['q_dt', 'energy_density', 'layer_thickness', 'T_bottom']].values  # Features
    Y = df[['x_b', 'x_as', 'x_am']].values  # Targets

    # Define polynomial transformation (e.g., degree 2 for quadratic terms)
    degree = 3  # Change to 3 for cubic regression
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)  # Expands input features with polynomial terms

    # Standardize the features for better training stability
    scaler_X = StandardScaler()
    scaler_Y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_poly)
    Y_scaled = scaler_Y.fit_transform(Y)

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_scaled, dtype=torch.float32)

    # Split data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)


    # Define a linear model (will learn polynomial coefficients)
    class PolynomialRegressionModel(nn.Module):
        def __init__(self, input_dim, output_dim):
            super(PolynomialRegressionModel, self).__init__()
            self.linear = nn.Linear(input_dim, output_dim)  # Simple linear layer

        def forward(self, x):
            return self.linear(x)


    # Model setup
    input_dim = X_scaled.shape[1]  # Number of polynomial features
    output_dim = Y.shape[1]  # 3 target variables
    model = PolynomialRegressionModel(input_dim, output_dim)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam optimizer

    # Training loop
    epochs = 500
    for epoch in range(epochs):
        model.train()

        # Forward pass
        predictions = model(X_train)
        loss = criterion(predictions, Y_train)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 50 == 0:  # Print loss every 50 epochs
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}')

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        Y_pred = model(X_test)
        test_loss = criterion(Y_pred, Y_test)
        print(f'Test Loss: {test_loss.item():.4f}')

    # Convert predictions back to original scale
    Y_pred_original = scaler_Y.inverse_transform(Y_pred.numpy())

    # Display sample predictions
    print("\nSample Predictions (First 5 rows):")
    print(pd.DataFrame(Y_pred_original[:5], columns=['x_b_pred', 'x_as_pred', 'x_am_pred']))


    Y_all_pred = model(X_tensor)
    # Convert predictions back to original scale
    Y_all_pred_original = scaler_Y.inverse_transform(Y_all_pred.detach().numpy())

    return pd.DataFrame(Y_all_pred_original, columns=['x_b', 'x_as', 'x_am'])


def fit_scipy_sigmoid01(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    def sigmoid(x, a, b, c, d):
        return a / (1 + np.exp(-b * (x + c))) + d

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), 1, -np.mean(x_data), min(y_data)]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {params_x_b[3]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {params_x_as[3]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {params_x_am[3]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    def sigmoid(x, a, b, c, d):
        return 1 / (1 + np.exp(-b * (x + c))) + d

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), 1, -np.mean(x_data), min(y_data)]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {params_x_b[3]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {params_x_as[3]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {params_x_am[3]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_bounds(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    def sigmoid(x, a, b, c, d):
        return 1 / (1 + np.exp(-b * (x + c))) + d

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), -5, -0.5, 0]
        bounds_bcd = ([-1e6, -30, -2, -0.5], [1e6, 0, 0.5, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000, bounds=bounds_bcd)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {params_x_b[3]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {params_x_as[3]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {params_x_am[3]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_bounds02(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return 1 / (1 + np.exp(-b * (x + c))) + d

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), -5, 0]
        bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000, bounds=bounds_bcd)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_wa_bounds02(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return a / (1 + np.exp(-b * (x + c))) + d

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), -5, 0]
        bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000, bounds=bounds_bcd)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_wa_wod_bounds02(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return a / (1 + np.exp(-b * (x + c)))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [max(y_data), -5, 0]
        bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000, bounds=bounds_bcd)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_wa_wod_noBbounds02(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return a / (1 + np.exp(-b * (x + c)))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, -5, 0]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_wod_noBounds02(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return 1 / (1 + np.exp(-b * (x + c)))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, -5, 0]
        # bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_wod_noBounds02_bcSep(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400


    if df["layer_thickness"].iloc[0] == 3e-05:
        y_intercepts = {"4": -4, "6": -4, "8": -4, "10": -4, "12": -4, "20": -4, "30": -4, "60": -4, "90": -4, "120": -4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": -0.19, "6": -0.18, "8": -0.17, "10": -0.16, "12": -0.15, "20": -0.13, "30": -0.11, "60": -0.07, "90": -0.02,
                          "120": 0.04}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 6e-05:
        y_intercepts = {"4": -0.77, "6": -1.05, "8": -1.22, "10": -1.4, "12": -1.5, "20": -1.65, "30": -1.75, "60": -1.8, "90": -1.8, "120": -1.8}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.06, "6": 0.06, "8": 0.06, "10": 0.05, "12": 0.04, "20": 0.02, "30": 0.02, "60": 0.03, "90": 0.04, "120": 0.07}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 9e-05:
        y_intercepts = {"4": -0.06, "6": -0.31, "8": -0.47, "10": -0.60, "12": -0.72, "20": -1.03, "30": -1.22, "60": -1.4, "90": -1.3, "120": -1.4}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.3, "6": 0.45, "8": 0.45, "10": 0.2, "12": 0.2, "20": 0.12, "30": 0.10, "60": 0.10, "90": 0.1, "120": 0}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude
    if df["layer_thickness"].iloc[0] == 12e-05:
        y_intercepts = {"4": 0, "6": -0.03, "8": -0.16, "10": -0.22, "12": -0.32, "20": -0.54, "30": -0.74, "60": -1.08, "90": -1.2, "120": -1.3}
        y_intercept = y_intercepts[f"{df['q_dt'].iloc[0]:.0f}"]

        one_intercepts = {"4": 0.5, "6": 0.45, "8": 0.3, "10": 0.25, "12": 0.25, "20": 0.25, "30": 0.25, "60": 0.20, "90": 0.25, "120": 0.25}
        magnitude = one_intercepts[f"{df['q_dt'].iloc[0]:.0f}"] - y_intercept
        c = y_intercept + df["T_bottom_scaled"].iloc[0] * magnitude

    print(c)


    def sigmoid(x, a, b, d):
        return 1 / (1 + np.exp(-b * x + c))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, -5, 0]
        # bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {c}, {params_x_b[2]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {c}, {params_x_as[2]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {c}, {params_x_am[2]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_wc_wod_noBounds_bcSep(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400

    def sigmoid(x, a, b, c):
        return 1 / (1 + np.exp(-b * x + c))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, 1, 0.5]
        # bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {0}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {0}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {0}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_wc_wod_noBounds_bcSep_wbrackets(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    df["T_bottom_scaled"] = 1 - (673.15-df["T_bottom"] ) / 400

    def sigmoid(x, a, b, c):
        return 1 / (1 + np.exp(-b * (x + c)))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, 1, 0.5]
        # bounds_bcd = ([-1e6, -10, -0.5], [1e6, 0, 0.3])

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {0}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {0}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {0}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid01_woa_wod(df_input, row_val, col_val, coly_value):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)

    def sigmoid(x, a, b, c, d):
        return 1 / (1 + np.exp(-b * (x + c)))

    def fit_sigmoid(df, col_name):
        x_data = df["energy_density_scaled"].values
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        if col_name == "x_am":
            initial_params = [1, -1, -np.mean(x_data), 1]
        else:
            initial_params = [1, 1, -np.mean(x_data), 1]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df["energy_density_scaled"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3]),
        'x_as': sigmoid(df["energy_density_scaled"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3]),
        'x_am': sigmoid(df["energy_density_scaled"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {params_x_b[3]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {params_x_as[3]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {params_x_am[3]}"

    summary_string = f"{row_val},{col_val},{coly_value},{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions, summary_string


def fit_scipy_sigmoid02(df_input):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)
    df["q_dt_scaled"] = scaler_X.fit_transform(df[['q_dt']].values)
    df["T_bottom_scaled"] = scaler_X.fit_transform(df[['T_bottom']].values)
    df["layer_thickness_scaled"] = scaler_X.fit_transform(df[['layer_thickness']].values)


    def sigmoid(x_data, a1, a2, a3, a4, b1, b2, b3, b4, c1, c2, c3, c4, d1, d2, d3, d4):
        a_prefactor = (a1 * x_data[0] + a2 * x_data[1] + a3 * x_data[2] + a4 * x_data[3])
        b_c_mid = (b1 * x_data[0] + c1 + b2 * x_data[1] + c2 + b3 * x_data[2] + c3 + b4 * x_data[3] + c4)
        d_add = (d1 * x_data[0] + d2 * x_data[1] + d3 * x_data[2] + d4 * x_data[3])
        return a_prefactor / (1 + np.exp(b_c_mid)) + d_add

    def fit_sigmoid(df, col_name):
        x_data = df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T
        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        initial_params = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    params_x_b = fit_sigmoid(df, "x_b")
    params_x_as = fit_sigmoid(df, "x_as")
    params_x_am = fit_sigmoid(df, "x_am")

    # print("Fitted parameters for x_b:", params_x_b)
    # print("Fitted parameters for x_as:", params_x_as)
    # print("Fitted parameters for x_am:", params_x_am)

    # x_bs_pred = sigmoid(df_input["energy_density"], params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3])
    # x_ass_pred = sigmoid(df_input["energy_density"], params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3])
    # x_ams_pred = sigmoid(df_input["energy_density"], params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3])

    df_predictions = pd.DataFrame({
        'x_b': sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_b[0], params_x_b[1], params_x_b[2], params_x_b[3], params_x_b[4], params_x_b[5], params_x_b[6], params_x_b[7], params_x_b[8], params_x_b[9], params_x_b[10], params_x_b[11], params_x_b[12], params_x_b[13], params_x_b[14], params_x_b[15]),
        'x_as': sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_as[0], params_x_as[1], params_x_as[2], params_x_as[3], params_x_as[4], params_x_as[5], params_x_as[6], params_x_as[7], params_x_as[8], params_x_as[9], params_x_as[10], params_x_as[11], params_x_as[12], params_x_as[13], params_x_as[14], params_x_as[15]),
        'x_am': sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_am[0], params_x_am[1], params_x_am[2], params_x_am[3], params_x_am[4], params_x_am[5], params_x_am[6], params_x_am[7], params_x_am[8], params_x_am[9], params_x_am[10], params_x_am[11], params_x_am[12], params_x_am[13], params_x_am[14], params_x_am[15])
    })

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"{params_x_b[0]}, {params_x_b[1]}, {params_x_b[2]}, {params_x_b[3]}, {params_x_b[4]}, {params_x_b[5]}, {params_x_b[6]}, {params_x_b[7]}, {params_x_b[8]}, {params_x_b[9]}, {params_x_b[10]}, {params_x_b[11]}, {params_x_b[12]}, {params_x_b[13]}, {params_x_b[14]}, {params_x_b[15]}"
    x_as_string = f"{params_x_as[0]}, {params_x_as[1]}, {params_x_as[2]}, {params_x_as[3]}, {params_x_as[4]}, {params_x_as[5]}, {params_x_as[6]}, {params_x_as[7]}, {params_x_as[8]}, {params_x_as[9]}, {params_x_as[10]}, {params_x_as[11]}, {params_x_as[12]}, {params_x_as[13]}, {params_x_as[14]}, {params_x_as[15]}"
    x_am_string = f"{params_x_am[0]}, {params_x_am[1]}, {params_x_am[2]}, {params_x_am[3]}, {params_x_am[4]}, {params_x_am[5]}, {params_x_am[6]}, {params_x_am[7]}, {params_x_am[8]}, {params_x_am[9]}, {params_x_am[10]}, {params_x_am[11]}, {params_x_am[12]}, {params_x_am[13]}, {params_x_am[14]}, {params_x_am[15]}"

    summary_string = f"{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions


def fit_scipy_sigmoid03_woa_wod(df_input):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)
    df["q_dt_scaled"] = scaler_X.fit_transform(df[['q_dt']].values)
    df["T_bottom_scaled"] = scaler_X.fit_transform(df[['T_bottom']].values)
    df["layer_thickness_scaled"] = scaler_X.fit_transform(df[['layer_thickness']].values)


    def sigmoid(x_data, b1, b2, b3, b4, c1, c2, c3, c4):
        b_mid = (b1 * x_data[0] + b2 * x_data[1] + b3 * x_data[2]) + b4  # 5 to 20 default 10
        c_mid = (c1 * x_data[0] + c2 * x_data[1] + c3 * x_data[2]) + c4 # -2 to 2 default -0.5
        return 0.9 * 1 / (1 + np.exp(-b_mid  * (x_data[3] + c_mid)))

    def fit_sigmoid(df, col_name):
        x_data = df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T
        for i, row in enumerate(x_data):
            print(f"Unique values in row {i}: {np.unique(row)}")

        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        if col_name == "x_as":
            initial_params = [1.2, 1.2, 1.2, 5, -0.1, -0.1, -0.1, -0.25]
        else:
            initial_params = [-1.2, -1.2, -1.2, -5, -0.1, -0.1, -0.1, -0.25]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    # params_x_b = fit_sigmoid(df, "x_b")
    print("Fitting x_as")
    params_x_as = fit_sigmoid(df, "x_as")
    print("Fitting x_am")
    params_x_am = fit_sigmoid(df, "x_am")

    x_ass_pred = sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_as[0],
                         params_x_as[1], params_x_as[2], params_x_as[3], params_x_as[4], params_x_as[5], params_x_as[6], params_x_as[7])
    x_ams_pred = sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_am[0],
                         params_x_am[1], params_x_am[2], params_x_am[3], params_x_am[4], params_x_am[5], params_x_am[6], params_x_am[7])
    x_bs_pred = 1 - x_ass_pred - x_ams_pred

    df_predictions = pd.DataFrame({
        'x_b': x_bs_pred,
        'x_as': x_ass_pred,
        'x_am': x_ams_pred,
    })

    df["x_b_pred"] = x_bs_pred
    df["x_as_pred"] = x_ass_pred
    df["x_am_pred"] = x_ams_pred

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"0,0,0,0,0,0,0,0,0"
    x_as_string = f"{params_x_as[0]},{params_x_as[1]},{params_x_as[2]},{params_x_as[3]},{params_x_as[4]},{params_x_as[5]},{params_x_as[6]},{params_x_as[7]}"
    x_am_string = f"{params_x_am[0]},{params_x_am[1]},{params_x_am[2]},{params_x_am[3]},{params_x_am[4]},{params_x_am[5]},{params_x_am[6]},{params_x_am[7]}"

    summary_string = f"{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions


def fit_scipy_sigmoid03_woa_wod_ln(df_input):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)
    df["q_dt_scaled"] = scaler_X.fit_transform(df[['q_dt']].values)
    df["T_bottom_scaled"] = scaler_X.fit_transform(df[['T_bottom']].values)
    df["layer_thickness_scaled"] = scaler_X.fit_transform(df[['layer_thickness']].values)


    def sigmoid(x_data, b1, b2, b3, b4, b5, c1, c2, c3, c4):
        # b_mid = np.log(b1 * (x_data[2] + b2 * x_data[0] + 0.125)) + b4 * x_data[1] + b5  # 5 to 20 default 10
        # c_mid = (c1 * x_data[0] + c2 * x_data[1] + c3 * x_data[2]) + c4 # -2 to 2 default -0.5

        b_mid = 1.5*(np.log(0.1 * (x_data[2] - 0.4 * x_data[0] + 0.2))) - 3 * x_data[1] - 3 * x_data[0] + 0  # 5 to 20 default 10
        c_mid = (1.243697451 * x_data[0] + 1.298083595 * x_data[1] + -0.582727792 * x_data[2]) + -1.751  # -2 to 2 default -0.5

        return 1 / (1 + np.exp(-b_mid  * (x_data[3] + c_mid)))

    def sigmoid_as(x_data, b1, b2, b3, b4, b5, c1, c2, c3, c4):
        b_mid = -( np.log(b1 * (x_data[2] + b2 * x_data[0] + 0.125)) + b4 * x_data[1] + b5 ) # 5 to 20 default 10


        c_mid = (c1 * x_data[0] + c2 * x_data[1] + c3 * x_data[2]) + c4 # -2 to 2 default -0.5
        return 1 / (1 + np.exp(-b_mid  * (x_data[3] + c_mid)))

    def fit_sigmoid(df, col_name):
        x_data = df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T
        for i, row in enumerate(x_data):
            print(f"Unique values in row {i}: {np.unique(row)}")

        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        if col_name == "x_as":
            initial_params = [1, -0.125, +0.125, -1.25, -3, -0.1, -0.1, -0.1, -0.25]
        else:
            initial_params = [1, -0.125, +0.125, -1.25, -3, -0.1, -0.1, -0.1, -0.25]

        # Fit the curve
        try:
            # Fit the curve
            if col_name == "x_as":
                params, _ = curve_fit(sigmoid_as, x_data, y_data, p0=initial_params, maxfev=10000)
            else:
                params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    # params_x_b = fit_sigmoid(df, "x_b")
    print("Fitting x_as")
    params_x_as = fit_sigmoid(df, "x_as")
    print("Fitting x_am")
    params_x_am = fit_sigmoid(df, "x_am")

    x_ass_pred = sigmoid_as(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_as[0],
                         params_x_as[1], params_x_as[2], params_x_as[3], params_x_as[4], params_x_as[5], params_x_as[6], params_x_as[7], params_x_as[8])
    x_ams_pred = sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_am[0],
                         params_x_am[1], params_x_am[2], params_x_am[3], params_x_am[4], params_x_am[5], params_x_am[6], params_x_am[7], params_x_am[8])
    x_bs_pred = 1 - x_ass_pred - x_ams_pred

    df_predictions = pd.DataFrame({
        'x_b': x_bs_pred,
        'x_as': x_ass_pred,
        'x_am': x_ams_pred,
    })

    df["x_b_pred"] = x_bs_pred
    df["x_as_pred"] = x_ass_pred
    df["x_am_pred"] = x_ams_pred

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"0,0,0,0,0,0,0,0,0"
    x_as_string = f"{params_x_as[0]},{params_x_as[1]},{params_x_as[2]},{params_x_as[3]},{params_x_as[4]},{params_x_as[5]},{params_x_as[6]},{params_x_as[7]},{params_x_as[8]}"
    x_am_string = f"{params_x_am[0]},{params_x_am[1]},{params_x_am[2]},{params_x_am[3]},{params_x_am[4]},{params_x_am[5]},{params_x_am[6]},{params_x_am[7]},{params_x_am[8]}"

    summary_string = f"{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions


def fit_scipy_sigmoid03_woa_wod_Q(df_input):

    # Load your dataframe
    df = df_input.copy()
    scaler_X = MinMaxScaler()
    df["energy_density_scaled"] = scaler_X.fit_transform(df[['Q_magnitude']].values)
    # df["energy_density_scaled"] = scaler_X.fit_transform(df[['energy_density']].values)
    df["q_dt_scaled"] = scaler_X.fit_transform(df[['q_dt']].values)
    df["T_bottom_scaled"] = scaler_X.fit_transform(df[['T_bottom']].values)
    df["layer_thickness_scaled"] = scaler_X.fit_transform(df[['layer_thickness']].values)


    def sigmoid(x_data, b1, b2, b3, b4, c1, c2, c3, c4):
        b_mid = (b1 * x_data[0] + b2 * x_data[1] + b3 * x_data[2]) + b4  # 5 to 20 default 10
        c_mid = (c1 * x_data[0] + c2 * x_data[1] + c3 * x_data[2]) + c4 # -2 to 2 default -0.5
        return 0.9 * 1 / (1 + np.exp(-b_mid  * (x_data[3] /  + c_mid)))

    def fit_sigmoid(df, col_name):
        x_data = df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T
        for i, row in enumerate(x_data):
            print(f"Unique values in row {i}: {np.unique(row)}")

        y_data = df[col_name].values

        # Initial parameter guesses: (a, b, c, d)
        if col_name == "x_as":
            initial_params = [1.2, 1.2, 1.2, 5, -0.1, -0.1, -0.1, -0.25]
        else:
            initial_params = [-1.2, -1.2, -1.2, -5, -0.1, -0.1, -0.1, -0.25]

        # Fit the curve
        try:
            # Fit the curve
            params, _ = curve_fit(sigmoid, x_data, y_data, p0=initial_params, maxfev=10000)
        except RuntimeError:
            print(f"Warning: Curve fitting did not converge for {col_name}.")
            params = initial_params  # Return initial guesses as fallback

        return params

    # Example usage
    # Assuming df is your dataframe
    # params_x_b = fit_sigmoid(df, "x_b")
    print("Fitting x_as")
    params_x_as = fit_sigmoid(df, "x_as")
    print("Fitting x_am")
    params_x_am = fit_sigmoid(df, "x_am")

    x_ass_pred = sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_as[0],
                         params_x_as[1], params_x_as[2], params_x_as[3], params_x_as[4], params_x_as[5], params_x_as[6], params_x_as[7])
    x_ams_pred = sigmoid(df[["layer_thickness_scaled", "T_bottom_scaled", "q_dt_scaled", "energy_density_scaled"]].values.T, params_x_am[0],
                         params_x_am[1], params_x_am[2], params_x_am[3], params_x_am[4], params_x_am[5], params_x_am[6], params_x_am[7])
    x_bs_pred = 1 - x_ass_pred - x_ams_pred

    df_predictions = pd.DataFrame({
        'x_b': x_bs_pred,
        'x_as': x_ass_pred,
        'x_am': x_ams_pred,
    })

    df["x_b_pred"] = x_bs_pred
    df["x_as_pred"] = x_ass_pred
    df["x_am_pred"] = x_ams_pred

    mse_x_b = np.mean((df["x_b"] - df_predictions["x_b"]) ** 2)
    mse_x_as = np.mean((df["x_as"] - df_predictions["x_as"]) ** 2)
    mse_x_am = np.mean((df["x_am"] - df_predictions["x_am"]) ** 2)

    # Print the final learned parameters
    x_b_string = f"0,0,0,0,0,0,0,0,0"
    x_as_string = f"{params_x_as[0]},{params_x_as[1]},{params_x_as[2]},{params_x_as[3]},{params_x_as[4]},{params_x_as[5]},{params_x_as[6]},{params_x_as[7]}"
    x_am_string = f"{params_x_am[0]},{params_x_am[1]},{params_x_am[2]},{params_x_am[3]},{params_x_am[4]},{params_x_am[5]},{params_x_am[6]},{params_x_am[7]}"

    summary_string = f"{x_b_string},{x_as_string},{x_am_string},{mse_x_b},{mse_x_as},{mse_x_am}"

    # print(f"{row_val}, {col_val}, {coly_value}, {x_b_string}, {x_as_string}, {x_am_string}, {loss_insight_all[0]}, {loss_insight_all[1]}, {loss_insight_all[2]}")
    print(summary_string)

    return df_predictions


