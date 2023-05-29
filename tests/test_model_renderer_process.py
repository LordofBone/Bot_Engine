import time
import unittest
from unittest.mock import patch, Mock
from graphics.skull_renderer import ModelRendererProcess
from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT


class TestModelRendererProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skull_renderer_process = ModelRendererProcess()
        cls.skull_renderer_process.start()  # Start the process

    @classmethod
    def tearDownClass(cls):
        cls.skull_renderer_process.terminate()  # Make sure to terminate the process when tests are done

    def test1_opengl_is_working(self):
        @patch('OpenGL.GL.glClearColor')
        @patch('OpenGL.GL.glClear')
        def test_clear(self, mock_glClear, mock_glClearColor):
            try:
                glClearColor(0.0, 0.0, 0.0, 1.0)
                glClear(GL_COLOR_BUFFER_BIT)
            except Exception as e:
                self.fail(f"OpenGL call raised exception: {e}")
            else:
                mock_glClearColor.assert_called_once_with(0.0, 0.0, 0.0, 1.0)
                mock_glClear.assert_called_once_with(GL_COLOR_BUFFER_BIT)

    def test2_jaw_movement(self):
        self.skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.jaw_movement_enabled, "Jaw movement should be enabled")
        self.skull_renderer_process.toggle_jaw_movement()  # Control the jaw movement again
        time.sleep(3)
        self.assertFalse(self.skull_renderer_process.jaw_movement_enabled, "Jaw movement should be disabled")
        time.sleep(3)

    def test3_head_nod(self):
        self.skull_renderer_process.toggle_head_nod()  # Control the head nod
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.head_nod_enabled, "Head nod should be enabled")
        self.skull_renderer_process.toggle_head_nod()  # Control the head nod again
        time.sleep(1)
        self.assertFalse(self.skull_renderer_process.head_nod_enabled, "Head nod should be disabled")
        time.sleep(3)

    def test4_head_shake(self):
        self.skull_renderer_process.toggle_head_shake()  # Control the head shake
        time.sleep(5)
        self.assertTrue(self.skull_renderer_process.head_shake_enabled, "Head shake should be enabled")
        self.skull_renderer_process.toggle_head_shake()  # Control the head shake again
        time.sleep(1)
        self.assertFalse(self.skull_renderer_process.head_shake_enabled, "Head shake should be disabled")
        time.sleep(3)

    def test5_combined_movements(self):
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
        time.sleep(3)

        # Test head nodding and shaking with jaw movement together
        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_nod()
        self.skull_renderer_process.toggle_head_shake()
        self.assertTrue(self.skull_renderer_process.jaw_movement_enabled)
        self.assertTrue(self.skull_renderer_process.head_nod_enabled)
        self.assertTrue(self.skull_renderer_process.head_shake_enabled)
        time.sleep(6)

        self.skull_renderer_process.toggle_jaw_movement()
        self.skull_renderer_process.toggle_head_nod()
        self.skull_renderer_process.toggle_head_shake()
        self.assertFalse(self.skull_renderer_process.jaw_movement_enabled)
        self.assertFalse(self.skull_renderer_process.head_nod_enabled)
        self.assertFalse(self.skull_renderer_process.head_shake_enabled)
        time.sleep(3)


if __name__ == '__main__':
    unittest.main()
