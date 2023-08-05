from collections import namedtuple

from .lark_parser import Lark_StandAlone, Transformer

class TJawnTransformer(Transformer):
    Pair = namedtuple('Pair', ['k', 'v'])

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

    def number(self, n):
        (n,) = n
        return float(n)

    def string(self, s):
        (s,) = s
        s = str(s[1:-1]).replace('\\"', '"')
        return s

    def cname(self, s):
        (s,) = s
        return str(s)

    def text(self, s):
        (s,) = s
        s = str(s[3:-3]).replace('\\"', '"')
        return s

    def list(self, s):
        if len(s) == 1 and s[0] is None:
            return list()
        return list(s)

    def set(self, s):
        if len(s) == 1 and s[0] is None:
            return set()
        return set(s)

    def dict(self, s):
        if len(s) == 1 and s[0] is None:
            return dict()
        return {p.k: p.v for p in s}

    def file(self, s):
        return self.dict(s)

    def key(self, s):
        (s, ) = s
        k = str(s) if s.type == 'CNAME' else str(s[1:-1]).replace('\\"', '"')
        return k

    def pair(self, s):
        return self.Pair(s[0], s[1])

parser = Lark_StandAlone(transformer=TJawnTransformer())

def loads(text: str):
    return parser.parse(text)
