import demo
import autoflex

def test_get_field_infos():
    model = demo.BasicClass()

    fields = autoflex.get_field_infos(model)

    print(f"Fields: {fields}")
    assert len(fields) == 3, f"Expected 3 fields, found {len(fields)}"
