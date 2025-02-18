import numpy as np
from bejoor.symbolic_regression import Term
from bejoor.symbolic_regression import SymbolicRegressor  # Import your SymbolicRegressor class


def generate_sample_data():
    """
    Generate synthetic data for regression.
    y = sin(x1) + cos(x2) + log(x3) for x3 > 0
    """
    np.random.seed(42)
    X = np.random.uniform(1, 10, size=(100, 3))  # 100 samples, 3 features
    y = np.sin(X[:, 0]) + np.cos(X[:, 1]) + np.log(X[:, 2])
    return X, y


def test_symbolic_regression():
    """
    Test the SymbolicRegressor by fitting it to synthetic data.
    """
    # Generate synthetic data
    X, y = generate_sample_data()

    # Initialize the SymbolicRegressor
    regressor = SymbolicRegressor(max_terms=5, max_const=3)

    print("Fitting symbolic regressor to data...")
    regressor.fit(X, y)

    print("Model string:", regressor.model_string)

    # Make predictions
    predictions = regressor.predict(X)

    # Evaluate performance using Mean Squared Error
    mse = np.mean((predictions - y) ** 2)
    print(f"Mean Squared Error: {mse}")

    # Check if MSE is below an acceptable threshold
    assert mse < 0.1, f"MSE is too high: {mse}"


if __name__ == "__main__":
    test_symbolic_regression()
