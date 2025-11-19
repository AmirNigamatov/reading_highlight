import json
import os
import unittest

from src.highlights import DATA_FILE, Highlight, add_highlight, load_highlights


class TestHighlights(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_input_validation_text_too_long(self):
        long_text = "a" * 1001
        with self.assertRaises(ValueError) as cm:
            Highlight(long_text, "source", [])
        error = json.loads(str(cm.exception))
        self.assertEqual(error["title"], "Text too long")
        self.assertEqual(error["status"], 400)

    def test_rfc7807_error_format(self):
        with self.assertRaises(ValueError) as cm:
            Highlight("text", "", [])
        error = json.loads(str(cm.exception))
        self.assertEqual(error["type"], "validation_error")
        self.assertEqual(error["title"], "Empty source")
        self.assertEqual(error["status"], 400)
        self.assertIn("instance", error)
        self.assertIn("errors", error)

    def test_safe_serialization_float_precision(self):
        test_data = [{"text": "test", "source": "source", "tags": []}]
        with open(DATA_FILE, "w") as f:
            json.dump(test_data, f)
        highlights = load_highlights()
        self.assertEqual(len(highlights), 1)
        self.assertEqual(highlights[0].text, "test")

    def test_add_highlight_positive(self):
        add_highlight("Sample text", "Sample source", ["tag1", "tag2"])
        highlights = load_highlights()
        self.assertEqual(len(highlights), 1)
        self.assertEqual(highlights[0].text, "Sample text")
        self.assertEqual(highlights[0].source, "Sample source")
        self.assertEqual(highlights[0].tags, ["tag1", "tag2"])


if __name__ == "__main__":
    unittest.main()
