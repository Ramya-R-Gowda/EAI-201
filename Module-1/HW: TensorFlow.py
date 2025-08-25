import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

m = float(input("Enter slope (m): "))
c = float(input("Enter intercept (c): "))

X = np.linspace(5, 15, 80)
Y = m * X + c + np.random.randn(*X.shape) * 1.2

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=[1])
])

# Compile model with Adam optimizer
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
print("Training...")
model.fit(X, Y, epochs=80, verbose=0)
print("Training done!")

# Extract learned weights
w, b = model.layers[0].get_weights()
w = w[0][0]   # slope
b = b[0]      # intercept
print(f"Learned line: y = {w:.2f}x + {b:.2f}")

# Plot data and fitted line
plt.scatter(X, Y, label="Data")
plt.plot(X, model.predict(X.reshape(-1, 1)), color="red", label="Fit")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("TensorFlow Linear Regression")
plt.legend()
plt.show()
