import psutil
import time
import json
import os

class DataCollector:
    def __init__(self, collection_interval=5):
        self.collection_interval = collection_interval  # time in seconds
        self.metrics = {}

    def collect_data(self):
        """Collect basic system QoS metrics."""
        self.metrics = {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_info': psutil.net_if_addrs(),
        }

    def store_data(self, storage_path='CentralCon/storage/data.json'):
        """Store collected data in the specified container."""
        # Create storage directory if it doesn't exist
        if not os.path.exists(os.path.dirname(storage_path)):
            os.makedirs(os.path.dirname(storage_path))
       
        with open(storage_path, 'a') as file:
            data = {
                'timestamp': time.time(),
                'metrics': self.metrics
            }
            json.dump(data, file)
            file.write('\n')  # new line after each entry for easy reading

    def run(self):
        """Run the data collector indefinitely."""
        while True:
            self.collect_data()
            self.store_data()
            print(f"Data collected: {self.metrics}")
            time.sleep(self.collection_interval)

if __name__ == "__main__":
    collector = DataCollector(collection_interval=5)  # collects every 5 seconds
    collector.run()

