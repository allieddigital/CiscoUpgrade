import re
from functools import total_ordering
from ansible.errors import AnsibleFilterError
from ansible.utils.display import Display

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

@total_ordering
class SwVersion:
	def __init__(self, version):
		# Normalize and parse version string
		self.original = version
		# Match patterns like 17.6.1a, 16.12.4, 3.18S, 15.7.3M, etc.
		match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?([a-zA-Z]*)", version)
		if not match:
			raise ValueError(f"Invalid Cisco IOS XE version: {version}")
		self.major = int(match.group(1))
		self.release = int(match.group(2))
		self.rebuild = int(match.group(3)) if match.group(3) else 0
		self.special = match.group(4) or ""

	def __eq__(self, other):
		if not isinstance(other, SwVersion):
			other = SwVersion(other)
		return (self.major, self.release, self.rebuild, self.special) == \
			(other.major, other.release, other.rebuild, other.special)

	def __lt__(self, other):
		if not isinstance(other, SwVersion):
			other = SwVersion(other)
		return (self.major, self.release, self.rebuild, self.special) < \
			(other.major, other.release, other.rebuild, other.special)

	def __repr__(self):
		return f"SwVersion('{self.original}' Normalized: {self.major}.{self.release}.{self.rebuild}{self.special})"

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