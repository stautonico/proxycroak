import os
import datetime

from proxycroak.config import CONFIG

from sentry_sdk import capture_exception


# import logging
#
# handler = logging.FileHandler(os.path.join(config.LOG_DIRECTORY, "requests.log"))
#     handler.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
#     formatter = logging.Formatter('[%(levelname)s] - %(message)s')
#     handler.setFormatter(formatter)
#
#     app.logger.removeHandler(default_handler)
#     app.logger.addHandler(handler)
#     app.logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)


class Logger:
    def __init__(self, log_file):
        self.log_path = CONFIG.LOG_DIRECTORY

        # Don't try to create it, this might cause errors, just throw
        print(f"[INFO] Checking for logs directory {self.log_path}")
        if not os.path.exists(self.log_path):
            raise Exception("[FATAL] Log directory does not exist!")

        # Try to open the log file
        print(f"[INFO] Trying to open log file {os.path.join(self.log_path, log_file)}")
        try:
            self.file = open(os.path.join(self.log_path, log_file), "a")
        except Exception as e:
            print(f"[FATAL] Failed to open log file: {e}")
            capture_exception(e)
            exit(1)

    def _get_timestamp(self):
        now = datetime.datetime.now()
        # Check if we're in DST
        if now.dst():
            offset = datetime.timedelta(hours=-4)
        else:
            offset = datetime.timedelta(hours=-5)
        now = now + offset
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def _write(self, level, message, category=None):
        self.file.write(f"\n[{level}] {self._get_timestamp()} ({category or '?'}) - {message}")
        self.file.flush()

    def debug(self, msg, category=None):
        self._write("DEBUG", msg, category)

    def info(self, msg, category=None):
        """Informational content"""
        self._write("INFO", msg, category)

    def warn(self, msg, category=None):
        """Something went wrong, but its recoverable"""
        self._write("WARN", msg, category)

    def error(self, msg, category=None):
        """Something went wrong, and the request cannot continue"""
        self._write("ERROR", msg, category)

    def fatal(self, msg, category=None):
        """Something went wrong, and the entire app cannot continue"""
        self._write("FATAL", msg, category)

    def close(self):
        print("[INFO] Closing log file")
        self.file.close()

    def __del__(self):
        self.close()


logger = Logger("app.log")
