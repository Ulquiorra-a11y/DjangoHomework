import logging
import time

http_logger = logging.getLogger('http_logger')


class HttpLogging:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        response = self.get_response(request)
        duration = time.monotonic() - start_time

        http_logger.info(
            '%s %s -> %s (%.3fs)',
            request.method,
            request.get_full_path(),
            response.status_code,
            duration,
        )
        return response