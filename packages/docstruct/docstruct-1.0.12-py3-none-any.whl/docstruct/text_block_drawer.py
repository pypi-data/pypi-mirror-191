from PIL import Image, ImageDraw
from .text_block import TextBlock, Character, Line, Page, Paragraph, Word


COLORS_MAP = {
    Character: "purple",
    Word: "blue",
    Line: "green",
    Paragraph: "yellow",
    Page: "red",
}
WIDTHS_MAP = {Character: 1, Word: 2, Line: 3, Paragraph: 4, Page: 5}


class TextBlockDrawer:
    """
    This class is used to draw bounding boxes of text blocks on an image.
    Example:

    from docstruct import TextBlockDrawer
    image_path = 'foo.png'
    page = Page() ...
    drawer = TextBlockDrawer(image_path)
    drawer.draw(page)
    drawer.show()
    """

    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.image_drawer = ImageDraw.Draw(self.image)

    def draw_block_index(self, block: TextBlock, draw_right: bool, draw_top: bool):
        """
        Draws the index of the block on the right top corner of the block.
        """
        bb = block.bounding_box
        top_left = bb.get_top_left()
        left, top = top_left.x * self.width, top_left.y * self.height
        bottom_right = bb.get_bottom_right()
        right, bottom = bottom_right.x * self.width, bottom_right.y * self.height
        top, bottom = self.height - top, self.height - bottom
        hor = right if draw_right else left
        ver = top if draw_top else bottom
        self.image_drawer.text(
            [hor, ver],
            str(block.get_absolute_order()),
            fill="black",
        )

    def draw_only(self, block: TextBlock, color: str = "black", width: int = 1):
        """
        Draws the bounding box of the text block on the image, not including it's children.
        """
        bb = block.bounding_box
        top_left = bb.get_top_left()
        left, top = top_left.x * self.width, top_left.y * self.height
        bottom_right = bb.get_bottom_right()
        right, bottom = bottom_right.x * self.width, bottom_right.y * self.height
        top, bottom = self.height - top, self.height - bottom

        self.image_drawer.rectangle(
            [left, top, right, bottom], outline=color, width=width
        )

    def draw(self, block: TextBlock, *to_draw: list[str]):
        """
        Draws the bounding boxes of the text block on the image, including it's children.
        """
        blocks = list(block.post_order_traversal(block))
        if not to_draw:
            to_draw = list((key.__name__.lower() for key in COLORS_MAP))
        for block in blocks:
            name = type(block).__name__.lower()
            if name not in to_draw:
                continue
            self.draw_only(
                block, color=COLORS_MAP[type(block)], width=WIDTHS_MAP[type(block)]
            )

        for block in blocks:
            name = type(block).__name__.lower()
            if name not in to_draw:
                continue
            if name == "paragraph":
                self.draw_block_index(block, draw_right=True, draw_top=True)
            elif name == "line":
                self.draw_block_index(block, draw_right=False, draw_top=False)

    def save(self, path: str):
        """
        Saves the image to the given path.
        """
        self.image.save(path)

    def show(self):
        """
        Shows the image.
        """
        self.image.show()
