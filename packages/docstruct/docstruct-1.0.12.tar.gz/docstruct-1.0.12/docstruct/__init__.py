from .hocr_parser import HocrParser
from .textract_parser import TextractParser
from .text_block import TextBlock, Document, Page, Paragraph, Line, Word, Character
from .bounding_box import BoundingBox
from .text_block_drawer import TextBlockDrawer
from .searchable_pdf import save_searchable_pdf
from .text_block_splitter import TextBlockSplitter
from .point import Point
from .segment import Segment

__version__ = "1.0.12"
