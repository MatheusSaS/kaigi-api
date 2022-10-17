from src.service.instance import server

from src.controllers.User import *
from src.controllers.Airline import *

from src.routes.User import *
from src.routes.Airline import *

from src.routes.stripe import *
from src.routes.Utils import *

server.run()