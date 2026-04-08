import time


class RateLimitInfo:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}
    
    def is_allowed(self, client_id: str) -> tuple[bool, int]:
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < self.window_seconds
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False, 0
        
        self.requests[client_id].append(current_time)
        remaining = self.max_requests - len(self.requests[client_id])
        
        return True, remaining
