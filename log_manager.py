import os
import shutil
import datetime

class LogManager:
    def __init__(self, logs_path='storage/logs', archive_path='storage/archives'):
        self.logs_path = logs_path
        self.archive_path = archive_path

    def rotate_logs(self):
        """Move old logs to an archive directory and start new ones."""
        os.makedirs(self.archive_path, exist_ok=True)
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        archive_dir = os.path.join(self.archive_path, date_str)
        os.makedirs(archive_dir, exist_ok=True)

        for file_name in os.listdir(self.logs_path):
            file_path = os.path.join(self.logs_path, file_name)
            if os.path.isfile(file_path):
                shutil.move(file_path, os.path.join(archive_dir, file_name))

    def run_daily_rotation(self):
        """Run log rotation every 24 hours."""
        while True:
            self.rotate_logs()
            print(f"Logs rotated and archived at {datetime.datetime.now()}")
            time.sleep(86400)  # 24 hours

if __name__ == "__main__":
    manager = LogManager()
    manager.run_daily_rotation()


