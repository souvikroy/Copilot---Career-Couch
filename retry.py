import time, os
from functools import wraps

def retry_gpt(delay=10, retries=10):
        def retry_decorator(f):
            @wraps(f)
            def f_retry(*args, **kwargs):
                opt_dict = {'retries': retries, 'delay': delay}
                while opt_dict['retries'] > 1:
                    try:
                        return f(*args, **kwargs)
                    except Exception:
                        msg = f"Exception: Retrying in {opt_dict['delay']} seconds {opt_dict['retries']} times..., pid:{os.getpid()}"
                        print(msg)
                        time.sleep(opt_dict['delay'])
                        opt_dict['retries'] -= 1
                        opt_dict['delay'] = opt_dict['delay'] + 5
                return f(*args, **kwargs)

            return f_retry

        return retry_decorator