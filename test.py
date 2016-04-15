import pytest

@pytest.fixture
def new_lic_100_1_year_item():
	return dict(article='100', maint_years=1)

@pytest.fixture
def new_lic_500_1_year_item():
	return dict(article='500', maint_years=1)

def new_lic():
	yield new_lic_100_1_year_item()
	yield new_lic_500_1_year_item()

@pytest.fixture
def billing_only_address():
	return dict(billing='billing', delivery=None)

@pytest.fixture
def billing_and_delivery_address():
	return dict(billing='billing', delivery='delivery')

@pytest.fixture(params=[billing_only_address, billing_and_delivery_address])
def checkout_address(request):
	return request.param
#	yield billing_only_address()
#	yield billing_and_delivery_address()

@pytest.fixture
def pay_with_creditcard():
	yield dict(order_method='creditcard')

@pytest.fixture
def pay_with_banktransfer():
	yield dict(order_method='banktransfer')

def order_methods():
	yield pay_with_creditcard()
	yield pay_with_banktransfer()

@pytest.mark.parametrize("new_lic", new_lic())
@pytest.mark.parametrize("addresses", checkout_address())
@pytest.mark.parametrize("order_methods", order_methods())
def orders(new_lic, addresses, order_methods):
	yield dict(
		cart=new_lic,
		addresses=addresses,
		payment=order_methods
	)

@pytest.mark.parametrize("new_lic", new_lic())
@pytest.mark.parametrize("addresses", checkout_address())
@pytest.mark.parametrize("order_methods", order_methods())
def _test_parts(new_lic, addresses, order_methods):
	assert True, new_lic

@pytest.mark.parametrize("order", orders())
def _test_orders(order):
	assert False, order

def test_addresses(checkout_address):
	assert False, checkout_address

