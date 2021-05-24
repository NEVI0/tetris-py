import random as rd

COLORS: tuple = (
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122)
)

class Block:

    def __init__(self: object, x: int, y: int) -> None:

        self.blocks: list = [
            [
                [1, 5, 9, 13], [4, 5, 6, 7]
            ],
            [
                [1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]
            ],
            [
                [1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]
            ],
            [
                [1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]
            ],
            [
                [1, 2, 5, 6]
            ]
        ]

        self.x: int = x
        self.y: int = y
        self.type = rd.randint(0, len(self.blocks) - 1)
        self.color = rd.randint(1, len(COLORS) - 1)
        self.rotation = 0

    def image(self: object) -> list:
        return self.blocks[self.type][self.rotation]

    def rotate(self: object) -> None:
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])