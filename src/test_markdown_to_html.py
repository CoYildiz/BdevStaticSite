import unittest

from markdown_to_html import markdown_to_html_node, extract_title


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a heading</h3></div>")

    def test_heading_with_inline_markdown(self):
        md = "# This is a **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a <b>bold</b> heading</h1></div>")

    def test_quote_block(self):
        md = """
> This is a quote
> spanning multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
- and _more_ items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. with items
3. and **more** items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with items</li><li>and <b>more</b> items</li></ol></div>",
        )

    def test_multiple_block_types(self):
        md = """
# Heading

This is a paragraph

> A quote

- list item one
- list item two

1. ordered one
2. ordered two

```
code here
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph</p>"
            "<blockquote>A quote</blockquote>"
            "<ul><li>list item one</li><li>list item two</li></ul>"
            "<ol><li>ordered one</li><li>ordered two</li></ol>"
            "<pre><code>code here\n</code></pre>"
            "</div>",
        )

    def test_links_and_images(self):
        md = "This is a [link](https://www.boot.dev) and an ![image](https://www.boot.dev/img.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a <a href="https://www.boot.dev">link</a> and an <img src="https://www.boot.dev/img.png" alt="image"></img></p></div>',
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_not_first_line(self):
        md = "Some intro text\n\n# The Real Title\n\nMore content"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_extract_title_ignores_h2(self):
        md = "## Not this one\n\n# This one"
        self.assertEqual(extract_title(md), "This one")

    def test_extract_title_no_heading_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a paragraph, no heading here")

    def test_extract_title_hash_without_space_raises(self):
        with self.assertRaises(ValueError):
            extract_title("#NoSpaceHeading")

    def test_extract_title_multiple_h1_returns_first(self):
        md = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()
