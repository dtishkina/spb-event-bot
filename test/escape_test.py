import unittest
from utils import html_escape


class TestEscape(unittest.TestCase):
    def test_escape_html(self):
        self.assertEqual(html_escape.escape_html('<div>Hello & "world"!</div>'),
                         '&lt;div&gt;Hello &amp; &quot;world&quot;!&lt;/div&gt;')
        self.assertEqual(html_escape.escape_html(""), "")
        self.assertEqual(html_escape.escape_html("No special characters"), "No special characters")
        self.assertEqual(html_escape.escape_html("5 > 3 and 3 < 5"), "5 &gt; 3 and 3 &lt; 5")
        # add assertion here


if __name__ == '__main__':
    unittest.main()
