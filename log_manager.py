import os
import shutil
import datetime
import time 

class LogManager:
    def __init__(self, logs_path='logs', archive_path='archives'):
        self.logs_path = logs_path
        self.archive_path = archive_path

        # Ensure directories exist
        os.makedirs(self.logs_path, exist_ok=True)
        os.makedirs(self.archive_path, exist_ok=True)

    def rotate_logs(self):
        """Move old logs to the archive folder and start new ones."""
        if not os.path.exists(self.logs_path): 
            print("No logs found to rotate.")
            return 

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        archive_folder = os.path.join(self.archive_path, f"logs_{date_str}")
        os.makedirs(archive_folder, exist_ok=True)

        for file_name in os.listdir(self.logs_path):
            file_path = os.path.join(self.logs_path, file_name)
            if os.path.isfile(file_path):
                shutil.move(file_path, os.path.join(archive_folder, file_name))
       
        print(f"Logs moved to {archive_folder}")

    def run_daily_rotation(self):
        """Run log rotation every 24 hours."""
        while True:
            self.rotate_logs()
            print(f"Log rotation completed at {datetime.datetime.now()}")
            time.sleep(86400)  # 24 hours

if __name__ == "__main__":
    manager = LogManager()
    manager.run_daily_rotation()





