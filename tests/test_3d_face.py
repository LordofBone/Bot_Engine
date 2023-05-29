import time
import unittest

from graphics.skull_renderer import ModelRendererProcess


class TestModelRendererProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skull_renderer_process = ModelRendererProcess()
        cls.skull_renderer_process.start()  # Start the process

    @classmethod
    def tearDownClass(cls):
        cls.skull_renderer_process.terminate()  # Make sure to terminate the process when tests are done
        time.sleep(3)

    def test_jaw_movement(self):
        self.skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.jaw_movement_enabled, "Jaw movement should be enabled")
        self.skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement again
        time.sleep(3)
        self.assertFalse(self.skull_renderer_process.jaw_movement_enabled, "Jaw movement should be disabled")

    def test_head_nod(self):
        self.skull_renderer_process.toggle_head_nod()  # Control the head nod
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.head_nod_enabled, "Head nod should be enabled")
        self.skull_renderer_process.toggle_head_nod()  # Control the head nod again
        time.sleep(1)
        self.assertFalse(self.skull_renderer_process.head_nod_enabled, "Head nod should be disabled")

    def test_head_shake(self):
        self.skull_renderer_process.toggle_head_shake()  # Control the head shake
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.head_shake_enabled, "Head shake should be enabled")
        self.skull_renderer_process.toggle_head_shake()  # Control the head shake again
        time.sleep(1)
        self.assertFalse(self.skull_renderer_process.head_shake_enabled, "Head shake should be disabled")

    def test_combined_movements(self):
        # Test jaw movement and head nodding together
        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_nod()
        self.assertTrue(self.skull_renderer_process.jaw_movement_enabled)
        self.assertTrue(self.skull_renderer_process.head_nod_enabled)
        time.sleep(3)

        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_nod()
        self.assertFalse(self.skull_renderer_process.jaw_movement_enabled)
        self.assertFalse(self.skull_renderer_process.head_nod_enabled)

        # Test jaw movement and head shaking together
        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_shake()
        self.assertTrue(self.skull_renderer_process.jaw_movement_enabled)
        self.assertTrue(self.skull_renderer_process.head_shake_enabled)
        time.sleep(3)

        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_shake()
        self.assertFalse(self.skull_renderer_process.jaw_movement_enabled)
        self.assertFalse(self.skull_renderer_process.head_shake_enabled)

        # Test head nodding and shaking together
        self.skull_renderer_process.toggle_head_nod()
        self.skull_renderer_process.toggle_head_shake()
        self.assertTrue(self.skull_renderer_process.head_nod_enabled)
        self.assertTrue(self.skull_renderer_process.head_shake_enabled)
        time.sleep(3)

        self.skull_renderer_process.toggle_head_nod()
        self.skull_renderer_process.toggle_head_shake()
        self.assertFalse(self.skull_renderer_process.head_nod_enabled)
        self.assertFalse(self.skull_renderer_process.head_shake_enabled)


if __name__ == '__main__':
    unittest.main()
