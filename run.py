from src.service.instance import server

from src.controllers.User import *
from src.controllers.Admin import *
from src.controllers.Events import *

from src.routes.User import *
from src.routes.Admin import *
from src.routes.Evensts import *

server.run()