import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from security.limiter.rate_limit import RateLimiter as RealRateLimiter
from security.limiter.login_rate_limit import LoginRateLimiter as RealLoginRateLimiter

class DummyApp:
    async def __call__(self, scope, receive, send):
        pass

def test_rate_limiter_init():
    app = DummyApp()
    limiter = RealRateLimiter(app)
    assert hasattr(limiter, 'requests')




