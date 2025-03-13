
import joblib
import pandas as pd

class MLPredictor:
    def __init__(self, model_path='qos_model.pkl'):
        self.model_path = model_path
        self.model, self.le = joblib.load(self.model_path)

    def predict(self, event_type, value):
        """Predict if an event will cause QoS issues."""
        event_type_encoded = self.le.transform([event_type])[0]
        prediction = self.model.predict([[event_type_encoded, value]])
        return "Issue Expected" if prediction[0] else "No Issue"

if __name__ == "__main__":
    predictor = MLPredictor()
    test_event = "network_delay"  # Replace with actual event type
    test_value = 120  # Replace with actual metric
    print(predictor.predict(test_event, test_value))


