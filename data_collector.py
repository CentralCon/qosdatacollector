import psutil
import time
import json
import os
import subprocess

class DataCollector:
    def __init__(self, collection_interval=5):
        self.collection_interval = collection_interval
        self.metrics = {}

    def collect_data(self):
        """Collect system QoS metrics."""
        self.metrics = {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_latency': self.ping_latency('8.8.8.8'),  # Google DNS as test
            'running_processes': len(psutil.pids()),  # Number of active processes
        }

    def ping_latency(self, host):
        """Measure network latency using ping."""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', host], capture_output=True, text=True
            )
            for line in result.stdout.split("\n"):
                if "time=" in line:
                    return float(line.split("time=")[1].split(" ")[0])  # Extract latency in ms
        except Exception:
            return None  # If ping fails, return None

    def store_data(self, storage_path='storage/data.json'):
        """Store collected data."""
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
       
        with open(storage_path, 'a') as file:
            data = {
                'timestamp': time.time(),
                'metrics': self.metrics
            }
            json.dump(data, file)
            file.write('\n')

    def run(self):
        """Run the data collector continuously."""
        while True:
            self.collect_data()
            self.store_data()
            print(f"Data collected: {self.metrics}")
            time.sleep(self.collection_interval)

if __name__ == "__main__":
    collector = DataCollector(collection_interval=5)
    collector.run()


