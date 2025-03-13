
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class MLTrainer:
    def __init__(self, logs_folder='logs', model_path='qos_model.pkl'):
        self.logs_folder = logs_folder
        self.model_path = model_path

    def load_data(self):
        """Load logs into a structured DataFrame."""
        log_files = [f for f in os.listdir(self.logs_folder) if f.endswith('.log')]
        data = []
       
        for file in log_files:
            with open(os.path.join(self.logs_folder, file), 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # Assuming log format: timestamp, event_type, value
                        timestamp, event_type, value = parts
                        data.append([timestamp, event_type, float(value)])

        return pd.DataFrame(data, columns=['timestamp', 'event_type', 'value'])

    def train_model(self):
        """Train an ML model on QoS logs and save it."""
        df = self.load_data()
        if df.empty:
            print("No log data available for training.")
            return

        le = LabelEncoder()
        df['event_type'] = le.fit_transform(df['event_type'])

        X = df[['event_type', 'value']]
        y = (df['value'] > df['value'].mean()).astype(int)  # Binary classification (above/below avg)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump((model, le), self.model_path)
        print(f"Model trained and saved to {self.model_path}")

if __name__ == "__main__":
    trainer = MLTrainer()
    trainer.train_model()

