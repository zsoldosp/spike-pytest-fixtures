import pytest

@pytest.fixture(scope='module')
def new_lic_100_1_year_item():
	return dict(article='100', maint_years=1)
new_lic_100_1_year_item.tags = ['newlicense', '100', 1]

@pytest.fixture(scope='module')
def new_lic_500_1_year_item():
	return dict(article='500', maint_years=1)
new_lic_500_1_year_item.tags = ['newlicense', '500', 1]

def new_lic():
	yield new_lic_100_1_year_item()
	yield new_lic_500_1_year_item()

def test_addresses(checkout_address):
	assert False, checkout_address

