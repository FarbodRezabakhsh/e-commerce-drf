
import os
env_target = os.getenv("DJANGO_ENV", "dev")
if env_target == "prod":
    from .prod import *  # noqa
else:
    from .dev import *   # noqa
