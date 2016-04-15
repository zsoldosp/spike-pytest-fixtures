import pytest
import _pytest
from functools import wraps


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
				# TODO: can implement shouldn't have tags relying on ! or ~ prefix
				missing_req = required_tags - self.tags
				if missing_req:
					_pytest.runner.skip('not applicable due to tags')
			return func(request, *a, **kw)
		return inner


@pytest.fixture
@tagged(tags=['enduser', 'billing'])
def end_user_billing_only(request):
	return dict(billing='billing', delivery=None)


@pytest.fixture
@tagged(tags=['enduser', 'billing', 'delivery'])
def end_user_billing_and_delivery(request):
	return dict(billing='billing', delivery='delivery')


@pytest.fixture
@tagged(tags=['partner', 'billing', 'delivery'])
def partner_billing_and_delivery(request):
	return dict(partner='some partner', billing='billing', delivery='delivery')


@pytest.fixture(params=[end_user_billing_only, end_user_billing_and_delivery, partner_billing_and_delivery])
def checkout_address(request):
	return request.param(request)


def pytest_addoption(parser):
	for option_name, values in tagged.options.items():
		arg_name = '--%s' % option_name.replace('_', '-')
		parser.addoption(
			arg_name, action="store", dest=option_name, metavar='label', nargs='+',
			choices=values,
			default=None, help="filter %s fixtures (tags)" % option_name)
