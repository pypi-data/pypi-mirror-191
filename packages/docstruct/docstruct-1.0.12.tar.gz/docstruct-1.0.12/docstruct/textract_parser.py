from .text_block import Line, Page, Paragraph, Word
from .bounding_box import BoundingBox
from .constants import LINE, PAGE, WORD
from .paragraph_detection.paragraph_extractor import ParagraphExtractor
from .paragraph_detection.paragraph_sorter import sort_paragraphs


class TextractParser:
    def __init__(self, textract_response: dict):
        self.textract_response = textract_response
        self.validate_args()
        self.words: list[dict] = []
        self.lines: list[dict] = []
        self.page: dict = None
        self.map_id_to_block: dict[str, dict] = {}

    def validate_args(self):
        """
        Validate the arguments
        """
        if not type(self.textract_response) == dict:
            raise ValueError("textract_response must be a dict")

    def get_children_id(self, block_dict: dict) -> list[str]:
        """
        Get the children ids of a block dict
        """
        relationships = block_dict.get("Relationships", [])
        for relationship in relationships:
            if relationship["Type"] == "CHILD":
                return relationship["Ids"]
        return []

    def get_bounding_box(self, block_dict: dict) -> BoundingBox:
        """
        Get a bounding box object from a block dict
        """
        bb_dict = block_dict["Geometry"]["BoundingBox"]

        # normalized image coordinates
        left = bb_dict["Left"]
        top = bb_dict["Top"]
        right = left + bb_dict["Width"]
        bottom = top + bb_dict["Height"]

        # normalized pdf coordinates
        top, bottom = 1 - top, 1 - bottom
        return BoundingBox(left, top, right, bottom)

    def get_line(self, block_dict: dict) -> Line:
        """
        Get a line object from a block dict
        """
        bb = self.get_bounding_box(block_dict)
        line = Line(bounding_box=bb)
        children_id = self.get_children_id(block_dict)
        for child_id in children_id:
            child_block_dict = self.map_id_to_block[child_id]
            child_block_object = child_block_dict["BlockObject"]
            line.add_child(child_block_object)
        return line

    def get_word(self, block_dict: dict) -> Word:
        """
        Get a word object from a block dict
        """
        bb = self.get_bounding_box(block_dict)
        text = block_dict["Text"]
        block = Word(bounding_box=bb, text=text)
        return block

    def split_blocks_by_type(self):
        """
        Split the blocks by type
        """
        blocks_dict = self.textract_response["Blocks"]
        for block_dict in blocks_dict:
            block_type = block_dict["BlockType"]
            if block_type == PAGE:
                self.page = block_dict
            elif block_type == LINE:
                self.lines.append(block_dict)
            elif block_type == WORD:
                self.words.append(block_dict)

    def set_map_id_to_block(self):
        """
        Get a map from block id to block dict
        """
        blocks_dict = self.textract_response["Blocks"]
        for block_dict in blocks_dict:
            self.map_id_to_block[block_dict["Id"]] = block_dict

    def parse_words(self):
        """
        Parse the words
        """
        for word_dict in self.words:
            word = self.get_word(word_dict)
            word_dict["BlockObject"] = word

    def parse_lines(self):
        """
        Parse the lines
        """
        for line_dict in self.lines:
            line = self.get_line(line_dict)
            line_dict["BlockObject"] = line

    def extract_paragraphs(self) -> list[Paragraph]:
        """
        Parse the paragraphs
        """
        lines = [line_dict["BlockObject"] for line_dict in self.lines]
        paragraphs_extractor = ParagraphExtractor(lines)
        paragraphs = paragraphs_extractor.extract_paragraphs()
        # paragraphs = sort_paragraphs(paragraphs)
        return paragraphs

    def extract_page(self, paragraphs: list[Paragraph]) -> Page:
        """
        Parse the page
        """
        page = Page()
        for paragraph in paragraphs:
            page.add_child(paragraph)
        return page

    def parse_response(self) -> Page:
        """
        Parse the textract response and return the page object
        """
        self.split_blocks_by_type()
        self.set_map_id_to_block()
        self.parse_words()
        self.parse_lines()
        paragraphs = self.extract_paragraphs()
        page = self.extract_page(paragraphs)
        page.set_length()
        page.set_bounding_box()
        return page
