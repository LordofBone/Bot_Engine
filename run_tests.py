import os
import sys

import unittest
from unittest.mock import patch, Mock

chatbot_dir = os.path.join(os.path.dirname(__file__), 'Bot_Engine')

sys.path.append(chatbot_dir)

from tests.test_avatar_renderer import TestModelRendererProcess

unittest.main()
