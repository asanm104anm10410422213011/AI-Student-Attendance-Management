from sklearn.linear_model import LinearRegression
import numpy as np

def predict_attendance(attendance_values):

    if len(attendance_values) < 2:
        return None

    X = np.array(range(1, len(attendance_values) + 1)).reshape(-1, 1)
    y = np.array(attendance_values)

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[len(attendance_values) + 1]])

    prediction = model.predict(next_day)[0]

    return round(prediction, 2)
