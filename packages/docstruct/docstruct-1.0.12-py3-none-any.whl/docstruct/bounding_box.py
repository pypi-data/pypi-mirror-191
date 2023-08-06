from typing import Optional
from .point import Point
from .segment import Segment


class BoundingBox:
    """
    A bounding box is a rectangle that has a left, top, right, and bottom.
    The coordinates of a box are meant to be normalized pdf coordinates i.e. the origin is at the bottom left of the page,
    the x-axis is horizontal and increases to the right, and the y-axis is vertical and increases upwards and the page coordinates
    is left = 0, top = 1, right = 1, bottom = 0.
    """

    def __init__(self, left: float, top: float, right: float, bottom: float):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.height = self.top - self.bottom
        self.width = self.right - self.left

    def validate_args(self):
        """Validate the arguments of the bounding box."""
        if self.right <= self.left:
            raise ValueError("right must be greater than left")
        if self.top <= self.bottom:
            raise ValueError("top must be greater than bottom")

    def get_left(self) -> float:
        """Get the left coordinate of the bounding box."""
        return self.left

    def get_top(self) -> float:
        """Get the top coordinate of the bounding box."""
        return self.top

    def get_right(self) -> float:
        """Get the right coordinate of the bounding box."""
        return self.right

    def get_bottom(self) -> float:
        """Get the bottom coordinate of the bounding box."""
        return self.bottom

    def get_width(self) -> float:
        """Get the width of the bounding box."""
        return self.right - self.left

    def get_area(self) -> float:
        """Get the area of the bounding box."""
        return self.get_width() * self.get_height()

    def get_height(self) -> float:
        """Get the height of the bounding box."""
        return self.top - self.bottom

    def get_center(self) -> Point:
        """Get the center of the bounding box."""
        center_x = (self.left + self.right) / 2
        center_y = (self.top + self.bottom) / 2
        return Point(center_x, center_y)

    def get_top_left(self) -> Point:
        """Get the top left point of the bounding box."""
        return Point(self.left, self.top)

    def get_top_right(self) -> Point:
        """Get the top right point of the bounding box."""
        return Point(self.right, self.top)

    def get_bottom_left(self) -> Point:
        """Get the bottom left point of the bounding box."""
        return Point(self.left, self.bottom)

    def get_bottom_right(self) -> Point:
        """Get the bottom right point of the bounding box."""
        return Point(self.right, self.bottom)

    def get_horizontal_segment(self):
        """Get the horizontal segment of the bounding box."""
        return Segment(self.left, self.right)

    def get_vertical_segment(self):
        """Get the vertical segment of the bounding box."""
        return Segment(self.bottom, self.top)

    def scale(self, scale_x: float, scale_y: float) -> "BoundingBox":
        """Scale the bounding box in the horizontal axis by scales_x
        and in the vertical axis by scale_y."""

        center = self.get_center()
        hor_shift = self.width * scale_x / 2
        ver_shift = self.height * scale_y / 2
        left = center.x - hor_shift
        top = center.y + ver_shift
        right = center.x + hor_shift
        bottom = center.y - ver_shift
        return BoundingBox(left, top, right, bottom)

    def intersect(self, other: "BoundingBox") -> bool:
        """Check if the bounding boxes intersect."""
        hor_intersection = self.left <= other.right and other.left <= self.right
        ver_intersection = self.bottom <= other.top and other.bottom <= self.top
        return hor_intersection and ver_intersection

    def __le__(self, other):
        """Check if the bounding box is weakly inside the other bounding box."""
        return (
            self.left >= other.left
            and self.right <= other.right
            and self.top <= other.top
            and self.bottom >= other.bottom
        )

    def __lt__(self, other):
        """Check if the bounding box is strongly inside the other bounding box."""
        return (
            self.left > other.left
            and self.right < other.right
            and self.top < other.top
            and self.bottom > other.bottom
        )

    def __str__(self):
        return f"BoundingBox(l={self.left:.3g}, t={self.top:.3g}, r={self.right:.3g}, b={self.bottom:.3g})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def compose_bounding_boxes(
        bounding_boxes: list["BoundingBox"],
    ) -> Optional["BoundingBox"]:
        """Compose a list of bounding boxes into a single bounding box.
        The resulting bounding box is the smallest bounding box that contains all the bounding boxes in the list."""
        if not bounding_boxes:
            return None
        left = min(bounding_boxes, key=lambda bb: bb.left).left
        top = max(bounding_boxes, key=lambda bb: bb.top).top
        right = max(bounding_boxes, key=lambda bb: bb.right).right
        bottom = min(bounding_boxes, key=lambda bb: bb.bottom).bottom
        return BoundingBox(left, top, right, bottom)

    @staticmethod
    def split_bounding_box(
        bounding_box: "BoundingBox", num_boxes: int
    ) -> list["BoundingBox"]:
        """Split a bounding box into a list of bounding boxes.
        The bounding boxes are split evenly along the width of the bounding box."""
        if num_boxes < 1:
            raise ValueError("num_boxes must be greater than 0")
        if num_boxes == 1:
            return [bounding_box]
        width = bounding_box.get_width()
        left = bounding_box.left
        top = bounding_box.top
        right = bounding_box.right
        bottom = bounding_box.bottom
        bounding_boxes = []
        for i in range(num_boxes):
            bounding_boxes.append(
                BoundingBox(
                    left + i * width / num_boxes,
                    top,
                    left + (i + 1) * width / num_boxes,
                    bottom,
                )
            )
        return bounding_boxes
