from mistletoe.block_token import (
    BlockCode,
    Heading,
    Quote,
    CodeFence,
    ThematicBreak,
    List,
    Table,
    Footnote,
    HTMLBlock,
    Paragraph,
    span_token,
)
from mistletoe.block_tokenizer import tokenize


# override mistletoe.block_token.Document defaults.
__all__ = [
    "BlockCode",
    "Heading",
    "Quote",
    "CodeFence",
    "ThematicBreak",
    "List",
    "Table",
    "Footnote",
    "HTMLBlock",
    "Paragraph",
]
_token_types = [globals()[cls_name] for cls_name in __all__]


class Document:
    """
    Copied from [mistletoe.block_token.Document](https://github.com/miyuchina/mistletoe/blob/276a7ec0f3ac541d93cec1fdb2fef582e48d9956/mistletoe/block_token.py#L136-L151)
    Instance attribute children is modified. I decided to copy instead of inherit the class to fix a scope issue.

    A copy of the original mistletoe license is available down below:

    The MIT License

    Copyright 2017 Mi Yu

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """

    token_types = _token_types

    def __init__(self, lines):
        if isinstance(lines, str):
            lines = lines.splitlines(keepends=True)
        lines = [line if line.endswith("\n") else "{}\n".format(line) for line in lines]
        self.footnotes = {}
        global _root_node
        _root_node = self
        span_token._root_node = self
        self.children = tokenize(lines, self.token_types)
        span_token._root_node = None
        _root_node = None
