"""
A generic package for requesting/serving number sequences across a network context

No security!
"""

import logging

# Logging must be configured as early as possible, so that no loggers are acquired before
# the config is set.
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s"
)
