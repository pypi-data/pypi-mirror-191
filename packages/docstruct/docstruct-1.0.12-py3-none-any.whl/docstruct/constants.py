"""Constants for the docstruct package.

The delimiter between pages / paragraphs / lines / words  
is represented by the `PAGE_DELIMITER` / `PARAGRAPH_DELIMITER` /  `LINE_DELIMITER`  / `WORD_DELIMITER` constant.
"""

PAGE_DELIMITER = "\f"
PARAGRAPH_DELIMITER = "\v"
LINE_DELIMITER = "\n"
WORD_DELIMITER = " "
PAGE = "PAGE"
LINE = "LINE"
WORD = "WORD"
BBOX_PATTERN = "\s*bbox\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)"

# The factor of which we'll multiply the paragraph bounding box when looking for intersections with other paragraphs.
PARAGRAPH_VERTICAL_SCALE = 1.3
PARAGRAPH_HORIZONTAL_SCALE = 1
