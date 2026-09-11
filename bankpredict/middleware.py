import time
import logging

logger = logging.getLogger(__name__)

class RequestPerformanceMiddleware:
    """
    Middleware that measures HTTP request execution time and logs requests taking longer than threshold.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        response['X-Process-Time'] = f"{duration:.3f}s"
        
        if duration > 1.0:
            logger.warning(f"Slow request: {request.method} {request.path} took {duration:.3f}s")
            
        return response
