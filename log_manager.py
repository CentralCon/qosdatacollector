
import os
import shutil
import datetime
import time 

class LogManager:
    def __init__(self, logs_path='storage/logs', archive_path='storage/archives'):
        self.logs_path = logs_path
        self.archive_path = archive_path

        # Ensure directories exist
        os.makedirs(self.logs_path, exist_ok=True)
        os.makedirs(self.archive_path, exist_ok=True)

    def rotate_logs(self):
        """Move old logs to an archive directory and start new ones."""
        if not os.path.exists(self.logs_path): 
            print("No logs found to rotate.")
            return  # Prevent error if no logs exist yet

        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        archive_dir = os.path.join(self.archive_path, date_str)
        os.makedirs(archive_dir, exist_ok=True)

        for file_name in os.listdir(self.logs_path):
            file_path = os.path.join(self.logs_path, file_name)
            if os.path.isfile(file_path):
                shutil.move(file_path, os.path.join(archive_dir, file_name))
       
        print(f"Logs archived to {archive_dir}")

    def run_daily_rotation(self):
        """Run log rotation every 24 hours."""
        while True:
            self.rotate_logs()
            print(f"Log rotation completed at {datetime.datetime.now()}")
            time.sleep(86400)  # 24 hours

if __name__ == "__main__":
    manager = LogManager()
    manager.run_daily_rotation()

