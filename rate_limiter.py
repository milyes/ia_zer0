# rate_limiter.py - IA_ZER0.09 - Native Network Rate Limiter
import time

class NativeRateLimiter:
    def __init__(self, requests_limit=5, window_seconds=10):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.ip_history = {}

    def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        if client_ip not in self.ip_history:
            self.ip_history[client_ip] = []
        self.ip_history[client_ip] = [t for t in self.ip_history[client_ip] if current_time - t < self.window_seconds]
        if len(self.ip_history[client_ip]) < self.requests_limit:
            self.ip_history[client_ip].append(current_time)
            return True
        return False