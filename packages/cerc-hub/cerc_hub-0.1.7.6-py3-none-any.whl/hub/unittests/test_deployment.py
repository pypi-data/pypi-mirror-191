from unittest import TestCase
from hub.version import __version__

class DeploymentTest(TestCase):
  def test_version(self):
    print(__version__)
    self.assertTrue(True)
