from piccolo.table import Table
from piccolo.columns import Varchar, Integer


class Website(Table):
    url = Varchar()