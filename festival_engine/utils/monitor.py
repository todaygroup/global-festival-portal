import time
import json
import os
from datetime import datetime
from typing import Any, Callable

class PerformanceMonitor:
    """
    Monitors system efficiency, tracking execution time and estimated token usage.
    Logs data to allow the GrowthOptimizer to identify bottlenecks.
    """
    def __init__(self, log_dir: str = "/home/aiagent/hyeongryeol_workspace/festival_engine/data/analytics"):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "performance_logs.json")
        os.makedirs(log_dir, exist_ok=True)

    def track(self, task_name: str, estimated_tokens: int = 0):
        """
        Decorator/Context Manager to track task performance.
        """
        class Timer:
            def __init__(self, monitor, name, tokens):
                self.monitor = monitor
                self.name = name
                self.tokens = tokens
                self.start_time = None

            def __enter__(self):
                self.start_time = time.time()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                duration = time.time() - self.start_time
                self.monitor._log_performance(self.name, duration, self.tokens, exc_type is None)

        return Timer(self, task_name, estimated_tokens)

    def _log_performance(self, task_name: str, duration: float, tokens: int, success: bool):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task_name,
            "duration_sec": round(duration, 4),
            "tokens": tokens,
            "success": success
        }
        
        # Append to log file
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        
        logs.append(log_entry)
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

# Global singleton for easy access across modules
monitor = PerformanceMonitor()
