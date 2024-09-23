from app.parsers import TreeParser


def test_parse_clean():
    parser = TreeParser()
    parser.add("ANIMAL,CAT,")
    values = parser.expand()
    assert len(values) == 1
    value = values.pop()
    parent, child = value[0], value[1]
    assert parent == "ANIMAL"
    assert child == "CAT"

def test_parse_no_previous():
    parser = TreeParser()
    parser.add("ANIMAL,CAT")
    values = parser.expand()
    assert len(values) == 1
    value = values.pop()
    parent, child = value[0], value[1]
    assert parent == "ANIMAL"
    assert child == "CAT"

def test_parse_previous_excluded():
    parser = TreeParser()
    parser.add("LOCATION,CITY,CAPITAL")
    parser.add("PERSON,MAN")
    values = parser.expand()
    assert len(values) == 3
    assert values == {("LOCATION","CITY"), ("CITY","CAPITAL"),("PERSON","MAN")}
    # different order
    parser = TreeParser()
    parser.add("PERSON,MAN")
    parser.add("LOCATION,CITY,CAPITAL")
    values = parser.expand()
    assert len(values) == 3
    assert values == {("LOCATION","CITY"), ("CITY","CAPITAL"),("PERSON","MAN")}

def test_parse_previous():
    parser = TreeParser()
    parser.add("LOCATION,CITY,CAPITAL")
    parser.add(",RESTAURANT")
    values = parser.expand()
    assert len(values) == 3
    assert values == {("LOCATION","CITY"), ("CITY","CAPITAL"),("LOCATION","RESTAURANT")}
    parser = TreeParser()
    parser.add("LOCATION,CITY")
    parser.add(",RESTAURANT,COCINA")
    values = parser.expand()
    assert len(values) == 3
    assert values == {("LOCATION","CITY"), ("RESTAURANT","COCINA"),("LOCATION","RESTAURANT")}
    