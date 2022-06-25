import random

MIN_ROW_COUNT = 5
MAX_ROW_COUNT = 30

MIN_COLUMN_COUNT = 5
MAX_COLUMN_COUNT = 30

MIN_MINE_COUNT = 1
MAX_MINE_COUNT = 800


class MinesweeperCell:
    # Возможные состояния игровой клетки:
    #   closed - закрыта
    #   opened - открыта
    #   flagged - помечена флажком
    #   questioned - помечена вопросительным знаком

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.state = 'closed'
        self.mined = False
        self.counter = 0

    markSequence = ['closed', 'flagged', 'questioned']

    def nextMark(self):
        if self.state in self.markSequence:
            stateIndex = self.markSequence.index(self.state)
            self.state = self.markSequence[(stateIndex + 1) % len(self.markSequence)]

    def open(self):
        if self.state != 'flagged':
            self.state = 'opened'


class MinesweeperModel:
    def __init__(self):
        self.startGame()

    def startGame(self, rowCount=15, columnCount=15, mineCount=15):
        if rowCount in range(MIN_ROW_COUNT, MAX_ROW_COUNT + 1):
            self.rowCount = rowCount

        if columnCount in range(MIN_COLUMN_COUNT, MAX_COLUMN_COUNT + 1):
            self.columnCount = columnCount

        if mineCount < self.rowCount * self.columnCount:
            if mineCount in range(MIN_MINE_COUNT, MAX_MINE_COUNT + 1):
                self.mineCount = mineCount
        else:
            self.mineCount = self.rowCount * self.columnCount - 1

        self.firstStep = True
        self.gameOver = False
        self.cellsTable = []
        for row in range(self.rowCount):
            cellsRow = []
            for column in range(self.columnCount):
                cellsRow.append(MinesweeperCell(row, column))
            self.cellsTable.append(cellsRow)

    def getCell(self, row, column):
        if row < 0 or column < 0 or self.rowCount <= row or self.columnCount <= column:
            return None

        return self.cellsTable[row][column]

    def isWin(self):
        for row in range(self.rowCount):
            for column in range(self.columnCount):
                cell = self.cellsTable[row][column]
                if not cell.mined and (cell.state != 'opened' and cell.state != 'flagged'):
                    return False

        return True

    def isGameOver(self):
        return self.gameOver

    def openCell(self, row, column):
        cell = self.getCell(row, column)
        if not cell:
            return

        cell.open()

        if cell.mined:
            self.gameOver = True
            return

        if self.firstStep:
            self.firstStep = False
            self.generateMines()

        cell.counter = self.countMinesAroundCell(row, column)
        if cell.counter == 0:
            neighbours = self.getCellNeighbours(row, column)
            for n in neighbours:
                if n.state == 'closed':
                    self.openCell(n.row, n.column)

    def nextCellMark(self, row, column):
        cell = self.getCell(row, column)
        if cell:
            cell.nextMark()

    def generateMines(self):
        for i in range(self.mineCount):
            while True:
                row = random.randint(0, self.rowCount - 1)
                column = random.randint(0, self.columnCount - 1)
                cell = self.getCell(row, column)
                if not cell.state == 'opened' and not cell.mined:
                    cell.mined = True
                    break

    def countMinesAroundCell(self, row, column):
        neighbours = self.getCellNeighbours(row, column)
        return sum(1 for n in neighbours if n.mined)

    def getCellNeighbours(self, row, column):
        neighbours = []
        for r in range(row - 1, row + 2):
            neighbours.append(self.getCell(r, column - 1))
            if r != row:
                neighbours.append(self.getCell(r, column))
            neighbours.append(self.getCell(r, column + 1))

        return filter(lambda n: n is not None, neighbours)