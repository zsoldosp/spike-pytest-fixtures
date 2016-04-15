import pytest
import _pytest


def pytest_addoption(parser):
        parser.addoption(
		"--tags", action="store", dest='tags',
		default=None, help="filter fixtures by tag")


def apply_fixture(request, fixture_fn):
	raw_tags = request.config.getoption('tags')
	if not raw_tags:
		return True
	required_tags = set(raw_tags.split(','))
	# TODO: can implement shouldn't have tags relying on ! or ~ prefix
	fn_tags = set(fixture_fn.tags)
	missing_req = required_tags - fn_tags
	if missing_req:
		return False
	return True

@pytest.fixture(scope='module')
def end_user_billing_only(request):
	if not apply_fixture(request, end_user_billing_only):
		_pytest.runner.skip('not applicable due to tags')
	return dict(billing='billing', delivery=None)
end_user_billing_only.tags = ['enduser', 'billing']


@pytest.fixture(scope='module')
def end_user_billing_and_delivery(request):
	return dict(billing='billing', delivery='delivery')
end_user_billing_and_delivery.tags = ['enduser', 'billing', 'delivery']


@pytest.fixture(params=[end_user_billing_only, end_user_billing_and_delivery])
def checkout_address(request):
	return request.param(request)
