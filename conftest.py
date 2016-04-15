import pytest
import _pytest
from functools import wraps

### infra 1

# TODO: this approach doesn't work with --collect-only
class tagged(object):

	options = {}

	def __init__(self, **tags):
		assert len(tags) == 1, 'usage: tagged(<tag name>=["tag1", "tag2"])'
		(self.tag_name, provides), = tags.items()
		self.tags = set(provides)
		tagged.options.setdefault(self.tag_name, set([]))
		tagged.options[self.tag_name] |= self.tags
		missing = self.tags - tagged.options[self.tag_name]
		assert len(missing) == 0, missing

	def __call__(self, func):
		@wraps(func)
		def inner(request, *a, **kw):
			raw_tags = request.config.getoption(self.tag_name)
			if raw_tags:
				required_tags = set(raw_tags)
				# TODO: can implement shouldn't have tags relying on '~' prefix (don't use '!' as that interferes with bash)
				missing_req = required_tags - self.tags
				if missing_req:
					_pytest.runner.skip('not applicable due to tags')
			return func(request, *a, **kw)
		return inner

def idfn(fixture_value):
	return fixture_value.__name__

### cart

@pytest.fixture
@tagged(cart_item=['maintenance', '1yearmaint', '100'])
def maint_100_1_year_item(request):
	return dict(article='100', maint_years=1)

@pytest.fixture
@tagged(cart_item=['maintenance', '1yearmaint', '500'])
def maint_500_1_year_item(request):
	return dict(article='500', maint_years=1)

@pytest.fixture(params=[maint_100_1_year_item, maint_500_1_year_item])
def maint_item(request):
	return request.param(request)

@pytest.fixture
@tagged(cart_item=['newlicense', '1yearmaint', '100'])
def new_lic_100_1_year_item(request):
	return dict(article='100', maint_years=1)

@pytest.fixture
@tagged(cart_item=['newlicense', '1yearmaint', '500'])
def new_lic_500_1_year_item(request):
	return dict(article='500', maint_years=1)

@pytest.fixture(params=[new_lic_100_1_year_item, new_lic_500_1_year_item], ids=idfn)
def new_lic_item(request):
	return request.param(request)

@pytest.fixture(params=(new_lic_item._pytestfixturefunction.params + maint_item._pytestfixturefunction.params), ids=idfn)
def cart_item(request):
	return request.param(request)

### checkout_address

@pytest.fixture
@tagged(checkout_address=['enduser', 'billing'])
def end_user_billing_only(request):
	return dict(billing='billing', delivery=None)


@pytest.fixture
@tagged(checkout_address=['enduser', 'billing', 'delivery'])
def end_user_billing_and_delivery(request):
	return dict(billing='billing', delivery='delivery')


@pytest.fixture
@tagged(checkout_address=['partner', 'billing', 'delivery'])
def partner_billing_and_delivery(request):
	return dict(partner='some partner', billing='billing', delivery='delivery')


@pytest.fixture(params=[end_user_billing_only, end_user_billing_and_delivery, partner_billing_and_delivery], ids=idfn)
def checkout_address(request):
	return request.param(request)


### payment option

@pytest.fixture
@tagged(payment_option=['creditcard'])
def payment_creditcard(request):
	return 'creditcard'

@pytest.fixture
@tagged(payment_option=['banktransfer'])
def payment_banktransfer(request):
	return 'banktransfer'

@pytest.fixture(params=[payment_creditcard, payment_banktransfer], ids=idfn)
def payment(request):
	return request.param(request)

### order

@pytest.fixture
def order(cart_item, checkout_address, payment):
	return dict(cart=cart_item, addresses=checkout_address, payment=payment)

### infra 2

def pytest_addoption(parser):
	for option_name, values in tagged.options.items():
		arg_name = '--%s' % option_name.replace('_', '-')
		parser.addoption(
			arg_name, action="store", dest=option_name, metavar='label', nargs='+',
			choices=values,
			default=None, help="filter %s fixtures (tags)" % option_name)
