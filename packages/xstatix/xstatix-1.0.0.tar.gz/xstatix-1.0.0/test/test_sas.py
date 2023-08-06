import logging
from pathlib import Path

from rich.logging import RichHandler
from statix.exposure import Exposure


logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
data_path = Path(".", "data")
data_path = data_path.resolve()

# Set the XMM exposure to be analized
event_list_path = data_path / "pnevt.fits"
attitude_path = data_path / "att.fits"
xmmexp = Exposure(event_list_path, attitude_path)

# Run SAS emldetect algorithm
# This also creates all products needed 
# for running STATiX, except the data cube
srclist = xmmexp.detect_sources(method="emldetect", likemin=6)

# Create data cube
cube = xmmexp.cube
print(cube)

# Run STATiX algorithm
# srclist = xmmexp.detect_sources()
