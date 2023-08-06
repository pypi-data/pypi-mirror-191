import np_logging

np_logging.setup(config=np_logging.fetch_zk_config("/projects/np_datajoint/defaults/logging"))

from np_datajoint.classes import *
from np_datajoint.config import *
from np_datajoint.utils import *
from np_datajoint.comparisons import *