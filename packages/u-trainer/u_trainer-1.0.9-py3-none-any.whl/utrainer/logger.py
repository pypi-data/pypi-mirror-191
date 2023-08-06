# -*- coding: utf8 -*-
#

import logging
import sys

trainer_log = logging.getLogger('UTrainer')


formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

trainer_log.setLevel(logging.INFO)
trainer_log.addHandler(stream_handler)
