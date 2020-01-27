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

class Shares: 
    def __init__(
        self, 
        number: int, 
        share_type: str = "ordinary", 
        nominal_value: float = 0.0001,
        prescribed_rights: str = "the usual"
    ) -> None:
        self.number = number
        self.share_type = share_type
        self.nominal_value = nominal_value
        self.prescribed_rights = prescribed_rights

    def __repr__(self):
        return get_repr(self)

def test_version_1():
    new_company = Company(name="Rocinante Limited")
    new_shareholder = Shareholder(name="James Holden")
    new_shareholder.shares_held.append(Shares(number=2500))
    new_company.shareholders.append(new_shareholder)
    
    # Check that James Holden is now a shareholder of Rocinante Limited
    assert new_company.name == "Rocinante Limited"
    assert "James Holden" in [sh.name for sh in new_company.shareholders]
    
    # Check that James Holden has 2500 ordinary shares of £0.0001 each
    assert new_company.shareholders[0].shares_held[0].number == 2500
    assert new_company.shareholders[0].shares_held[0].share_type == "ordinary"
    assert new_company.shareholders[0].shares_held[0].nominal_value == 0.0001    

    return new_company

if __name__ == "__main__":
    results = test_version_1()
    print(results)
    
