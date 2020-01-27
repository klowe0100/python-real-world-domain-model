"""
This is part of the code accompanying this article: 
https://www.eventsorcery.com/posts/building-a-real-world-domain-model-python/

Version 2 clarifies what a share class should be and creates a 
relationship between it and the shares themselves. 
"""

from uuid import uuid4

def get_repr(obj):
    attributes = ("%s=%r" % (k, v) for k, v in obj.__dict__.items())
    return "<%s(%s)." % (obj.__class__.__name__, ', '.join(attributes))

class Company:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = uuid4()
        self.shareholders = []

    def __repr__(self):
        return get_repr(self)

class Shareholder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.shares_held = []

    def __repr__(self):
        return get_repr(self)

class ShareClass:
    def __init__(
        self,
        name: str = "ordinary",
        nominal_value: float = 0.0001,
        entitled_to_dividends: bool = True,
        entitled_to_capital: bool = True,
        votes_per_share: int = 1,
        redeemable: bool = False
    ) -> None:
        self.name = name
        self.nominal_value = nominal_value 
        self.entitled_to_dividends = entitled_to_dividends
        self.entitled_to_capital = entitled_to_capital
        self.votes_per_share = votes_per_share
        self.redeemable = redeemable

    def __repr__(self):
        return get_repr(self)

class Shares: 
    def __init__(
        self, 
        number: int, 
        share_class: ShareClass = ShareClass(name="ordinary")
    ) -> None:
        self.number = number
        self.share_class = share_class

    def __repr__(self):
        return get_repr(self)

def test_version_2():
    new_company = Company(name="Rocinante Limited")
    new_shareholder = Shareholder(name="James Holden")
    new_shares = Shares(number=2500)
    new_company.shareholders.append(new_shareholder)
    new_company.shareholders[0].shares_held.append(new_shares)

    # Check that James Holden is now a shareholder of Rocinante Limited
    assert new_company.name == "Rocinante Limited"
    assert "James Holden" in [sh.name for sh in new_company.shareholders]

    # Check that James Holden has 2500 ordinary shares of £0.0001 each
    assert new_company.shareholders[0].shares_held[0].number == 2500
    assert new_company.shareholders[0].shares_held[0].share_class.name == "ordinary"
    assert new_company.shareholders[0].shares_held[0].share_class.nominal_value == 0.0001

    return new_company

if __name__ == "__main__":
    results = test_version_2()
    print(results)
    
    

     