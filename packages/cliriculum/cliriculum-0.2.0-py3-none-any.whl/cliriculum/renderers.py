from mistletoe.html_renderer import HTMLRenderer
from cliriculum.markdown import (
    LogoEntry,
    TextEntry,
    URLEntry,
    ContactBlock,
    SocialBlock,
    DescriptionBlock,
    ImageEntry,
    LocationEntry,
    PeriodEntry,
)
from textwrap import dedent


class Renderer(HTMLRenderer):
    def __init__(self):
        super().__init__(
            DescriptionBlock,
            ContactBlock,
            SocialBlock,
            TextEntry,
            URLEntry,
            ImageEntry,
            LocationEntry,
            PeriodEntry,
        )

    @staticmethod
    def _image_html(token):
        if token.width is None:
            width = ""
        else:
            width = 'width="{}"'.format(token.width)
        if token.height is None:
            height = ""
        else:
            height = 'height="{}"'.format(token.height)
        identifier = ""
        if hasattr(token, "id"):
            if token.id is not None:
                identifier = 'id="{}"'.format(token.id)

        html = '<img src="{src}" {width} {height} {identifier}/>'
        return html.format(
            src=token.src, width=width, height=height, identifier=identifier
        )

    @staticmethod
    def _i_image_html(token):
        template = '<i class="{classes}"></i>'
        return template.format(classes=token.classes)

    def render_logo_entry(self, token):
        text = token.title
        parent_o = '<div class="box">'
        parent_c = "</div>"

        if token.classes is not None:
            html = "\n".join(
                [parent_o, self._i_image_html(token), f"<span>{text}</span>", parent_c]
            )
        else:
            if token.src is None:
                html = "\n".join([parent_o, f"<span>{text}</span>", parent_c])
            else:
                html = "\n".join(
                    [
                        parent_o,
                        self._image_html(token),
                        f"<span>{text}</span>",
                        parent_c,
                    ]
                )
        return dedent(html)

    def render_period_entry(self, token):
        return self.render_logo_entry(token)

    def render_location_entry(self, token):
        return self.render_logo_entry(token)

    def render_image_entry(self, token):
        if token.src is not None:
            return self._image_html(token)
        else:
            return ""

    def render_text_entry(self, token):
        pre = "<p>"
        post = "</p>"
        if token.emphasis == "bold":
            html = """
            <strong>{text}</strong>
            """.format(
                text=token.text
            )
        elif token.emphasis == "italic":
            html = """
            <i>{text}</i>
            """.format(
                text=token.text
            )
        else:
            html = """
            <p>{text}</p>
            """.format(
                text=token.text
            )
        return pre + dedent(html) + post

    def render_url_entry(self, token):
        parent_o = '<div class="box">'
        parent_c = "</div>"
        url = token.url
        if token.text is None and token.url is not None:
            text = token.url
        elif token.text is None and token.url is None:
            return ""
        text = token.text
        if token.classes is not None:
            html = "\n".join(
                [
                    parent_o,
                    self._i_image_html(token),
                    f'<a href="{url}">{text}</a>',
                    parent_c,
                ]
            )
        else:
            if token.src is None:
                html = "\n".join([parent_o, f'<a href="{url}">{text}</a>', parent_c])

            else:
                html = "\n".join(
                    [
                        parent_o,
                        self._image_html(token),
                        f'<a href="{url}">{text}</a>',
                        parent_c,
                    ]
                )
        return dedent(html)

    def render_contact_block(self, token):
        template = """
        <div class="contact" id="contact">
        <div class="content">
        {inner}
        </div>
        </div>
        """

        return dedent(template.format(inner=self.render_inner(token)))

    def render_social_block(self, token):
        template = '<div class="social">\n{inner}\n</div>'
        inner = self.render_inner(token)
        return template.format(inner=inner)

    def render_description_block(self, token):
        template = (
            '<div class="description">\n<div class="content">\n{inner}\n</div>\n</div>'
        )
        inner = self.render_inner(token)
        return template.format(inner=inner)


class MainRenderer(Renderer):
    def render_document(self, token):
        """
        Renders document to html representation in `<main>...</main>` tags
        Parameters
        ----------
        token : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        template = """
        <main id = "main" class="main">
        <div class="content">
        {main}
        </div>
        </main>
        """
        return dedent(template.format(main=self.render_inner(token)))


class SideBarRenderer(Renderer):
    def render_document(self, token):
        """
        Renders document to html representation in `<aside>...</aside>` tags

        Parameters
        ----------
        token : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        template = '<aside id="aside" class="aside">\n{sidebar}\n</aside>'

        return template.format(sidebar=self.render_inner(token))
