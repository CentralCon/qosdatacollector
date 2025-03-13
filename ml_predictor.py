import joblib
import os

class MLPredictor:
    def __init__(self, model_path='qos_model.pkl'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found. Train it first.")
        self.model, self.le = joblib.load(model_path)

    def predict(self, event_type, value):
        """Predict if an event will cause QoS issues."""
        # Handle unseen labels gracefully by using a fallback value
        if event_type not in self.le.classes_:
            print(f"Warning: Unseen event type '{event_type}'. Using default encoding.")
            event_type_encoded = len(self.le.classes_)  # Fallback encoding
        else:
            event_type_encoded = self.le.transform([event_type])[0]

        prediction = self.model.predict([[event_type_encoded, value]])
        return "Issue Expected" if prediction[0] else "No Issue"

if __name__ == "__main__":
    predictor = MLPredictor()
    test_event = "network_delay"  # Example event
    test_value = 120  # Example metric
    print(predictor.predict(test_event, test_value))



