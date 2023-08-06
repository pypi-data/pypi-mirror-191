from .api import Tran, Card, Member, Trade
from .context import Context


class Gateway:
    def __init__(self, timeout=None, production=True):
        self._context = Context(timeout=timeout, production=production)
        self.tran = Tran(context=self._context)
        self.card = Card(context=self._context)
        self.member = Member(context=self._context)
        self.trade = Trade(context=self._context)
