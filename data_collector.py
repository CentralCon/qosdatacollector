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
            'network_latency': self.ping_latency('8.8.8.8'),
            'running_processes': len(psutil.pids()),
        }

    def ping_latency(self, host):
        """Measure network latency using ping."""
        try:
            result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)
            for line in result.stdout.split("\n"):
                if "time=" in line:
                    return float(line.split("time=")[1].split(" ")[0])
        except Exception:
            return None

    def store_data(self):
        """Store collected data into separate logs."""
        base_path = 'storage/logs'
        os.makedirs(base_path, exist_ok=True)

        for key, value in self.metrics.items():
            file_path = os.path.join(base_path, f"{key}.json")
            with open(file_path, 'a') as file:
                data = {'timestamp': time.time(), 'value': value}
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


