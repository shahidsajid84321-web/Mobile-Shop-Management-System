import pytest
from pydantic import ValidationError
from app.modules.categories.category_schema import CategoryCreate, CategoryUpdate

def test_category_create_valid():
    item = CategoryCreate(name="Phones", description="Mobile phones")
    assert item.name == "Phones"

@pytest.mark.parametrize("name", ["", "A", "x" * 101])
def test_category_name_constraints(name):
    with pytest.raises(ValidationError): CategoryCreate(name=name)

def test_category_update_allows_partial_fields():
    assert CategoryUpdate(description="Updated").description == "Updated"
