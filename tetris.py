from block import Block

class Tetris:

    def __init__(self: object, height: int, width: int) -> None:

        self.height: int = height
        self.width: int = width

        self.level: int = 2
        self.score: int = 0
        self.zoom: int = 20
        self.x: int = 100
        self.y: int = 60

        self.state: str = 'start'
        self.field: list = []
        self.block = None

        for i in range(self.height):
            new_line: list = []

            for j in range(self.width):
                new_line.append(0)

            self.field.append(new_line)

    def new_figure(self: object) -> None:
        self.block: Block = Block(3, 0)

    def intersects(self: object) -> bool:
        intersection = False

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    if (i + self.block.y > self.height - 1) or (j + self.block.x > self.width - 1) or (j + self.block.x < 0) or (self.field[i + self.block.y][j + self.block.x] > 0):
                        intersection = True

        return intersection

    def freeze(self: object) -> None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color

        self.break_lines()
        self.new_figure()

        if self.intersects():
            self.state ='gameover'

    def break_lines(self: object) -> None:
        lines: int = 0

        for i in range(1, self.height):
            zeros: int = 0

            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1

            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]

        self.score += lines ** 2

    def go_space(self: object) -> None:
        while not self.intersects():
            self.block.y += 1

        self.block.y -= 1
        self.freeze()

    def go_down(self: object) -> None:
        self.block.y += 1

        if self.intersects():
            self.block.y -= 1
            self.freeze()

    def go_side(self: object, dx) -> None:
        old_x = self.block.x
        self.block.x += dx

        if self.intersects():
            self.block.x = old_x

    def rotate(self: object) -> None:
        old_rotation = self.block.rotation
        self.block.rotate()

        if self.intersects():
            self.block.rotation = old_rotation