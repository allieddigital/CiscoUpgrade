DOCUMENTATION = r'''
---
module: swversion
short_description: Test plugin for comparing software versions using netports.swversion
description:
  - Provides tests for software version equality and parsing.
  - Uses the netports.swversion module for version parsing.
options: {}
author:
  - Justin Grote (@JustinGrote)
'''

EXAMPLES = r'''
- assert:
    that:
      - swversion_equal('1.2.3', '1.2.3')
      - swversion_parse('1.2.3', '1.2.3')
'''

RETURN = r'''
swversion_equal:
  description: Returns True if versions are equal.
  type: bool
swversion_parse:
  description: Returns True if parsed version matches expected.
  type: bool
'''

from ansible.errors import AnsibleFilterError
from ansible.utils.display import Display
from netports import SwVersion

# Use this to write debug messages
display = Display()

def test_swversion_equal(value, other):
	try:
		display.vvv(f"SWVERSION: Comparing versions {value} == {other}")
		return SwVersion(value) == SwVersion(other)
	except Exception as e:
		raise AnsibleFilterError(f'Error comparing versions {value} and {other}: {e}')

def test_swversion_greater(value, other):
	try:
		display.vvv(f"SWVERSION: Comparing versions {value} > {other}")
		return SwVersion(other) > SwVersion(value)
	except Exception as e:
		raise AnsibleFilterError(f'Error comparing versions {value} and {other}: {e}')

def test_swversion_lesser(value, other):
	try:
		display.vvv(f"SWVERSION: Comparing versions {value} < {other}")
		return SwVersion(other) < SwVersion(value)
	except Exception as e:
		raise AnsibleFilterError(f'Error comparing versions {value} and {other}: {e}')

#Export the functions
class TestModule(object):
	def tests(self):
		return {
			'swversion_equalto': test_swversion_equal,
			'swversion_greaterthan': test_swversion_greater,
			'swversion_lesserthan': test_swversion_lesser,
		}