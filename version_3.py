"""
This is part of the code accompanying this article: 
https://www.eventsorcery.com/posts/building-a-real-world-domain-model-python/

Version 3 introduces commands and events triggered by them. 
"""
from uuid import uuid4
from typing import Any
from datetime import datetime

def get_simple_repr(obj):
    attributes = ("%s=%r" % (k, v) for k, v in obj.__dict__.items())
    return "<%s(%s)." % (obj.__class__.__name__, ', '.join(attributes))

class Company:
    def __init__(self, name: str) -> None:
        self.name = name
        self.id = uuid4()
        self.shareholders = []
        self.share_classes = []
        self.events = []

    def __repr__(self):
        return f"Company(name='{self.name}', len(share_classes)={len(self.share_classes)}, len(events)={len(self.events)})"

    def create_share_class(
            self,
            name: str,
            nominal_value: float,
            entitled_to_dividends: bool = True,
            entitled_to_capital: bool = True,
            votes_per_share: int = 1,
            redeemable: bool = False
        ) -> None: 
            event = self.ShareClassWasCreated(
                name=name,
                nominal_value=nominal_value,
                entitled_to_dividends=entitled_to_dividends,
                entitled_to_capital=entitled_to_capital,
                votes_per_share=votes_per_share,
                redeemable=redeemable
            )
            event.apply(self)
            self.events.append(event)

    class ShareClassWasCreated:
        def __init__(self, **kwargs: Any) -> None:
            self.__dict__['created_on'] = f"{datetime.now():%Y-%m-%d at %H:%M:%S%z}"
            self.__dict__.update(kwargs)
        
        def apply(event, company):
            new_shareclass = ShareClass(name=event.name, nominal_value=event.nominal_value)
            company.share_classes.append(new_shareclass)

        def __repr__(self):
            return "ShareClassWasCreated(" + ', '.join(
                    "{0}={1!r}".format(*item) for item in self.__dict__.items()
                ) + ')'

class Shareholder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.shares_held = []

    def __repr__(self):
        return get_simple_repr(self)

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
        return get_simple_repr(self)

class Shares: 
    def __init__(
        self, 
        number: int, 
        share_class: ShareClass
    ) -> None:
        self.number = number
        self.share_class = share_class or ShareClass(name="ordinary")

    def __repr__(self):
        return get_simple_repr(self)

def test_version_3():
    new_company = Company(name="Rocinante Limited")
    new_shareholder = Shareholder(name="James Holden")
    new_company.create_share_class(name="ordinary", nominal_value=0.0001)
    new_shares = Shares(number=2500, share_class=new_company.share_classes[0])

    new_company.shareholders.append(new_shareholder)
    new_company.shareholders[0].shares_held.append(new_shares)

    # Check that the company has a newly created ordinary share class
    assert new_company.share_classes[0].name == "ordinary"
    assert new_company.share_classes[0].nominal_value == 0.0001

    # Check that James Holden is a shareholder of Rocinante Limited
    assert new_company.name == "Rocinante Limited"
    assert "James Holden" in [sh.name for sh in new_company.shareholders]

    # Check that James Holden has 2500 ordinary shares of £0.0001 each
    assert new_company.shareholders[0].shares_held[0].number == 2500
    assert new_company.shareholders[0].shares_held[0].share_class.name == "ordinary"
    assert new_company.shareholders[0].shares_held[0].share_class.nominal_value == 0.0001

    # Check that we have something useful in our new event log
    assert len(new_company.events) == 1
    assert isinstance(new_company.events[0], Company.ShareClassWasCreated)
    assert hasattr(new_company.events[0], "created_on")

    return new_company

if __name__ == "__main__":
    newco = test_version_3()
    print(newco)
    
    

     