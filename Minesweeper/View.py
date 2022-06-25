from tkinter import *
from tkinter.messagebox import *

MIN_ROW_COUNT = 5
MAX_ROW_COUNT = 30

MIN_COLUMN_COUNT = 5
MAX_COLUMN_COUNT = 30

MIN_MINE_COUNT = 1
MAX_MINE_COUNT = 800

class MinesweeperView(Frame):
    def __init__(self, model, controller, parent=None):
        Frame.__init__(self, parent)
        self.model = model
        self.controller = controller
        self.controller.setView(self)
        self.createBoard()

        panel = Frame(self)
        panel.pack(side=BOTTOM, fill=X)

        Button(panel, text='Новая игра', command=self.controller.startNewGame).pack(side=RIGHT)

        self.mineCount = StringVar(panel)
        self.mineCount.set(self.model.mineCount)
        Spinbox(
            panel,
            from_=MIN_MINE_COUNT,
            to=MAX_MINE_COUNT,
            textvariable=self.mineCount,
            width=5
        ).pack(side=RIGHT)
        Label(panel, text=' Количество мин: ').pack(side=RIGHT)

        self.rowCount = StringVar(panel)
        self.rowCount.set(self.model.rowCount)
        Spinbox(
            panel,
            from_=MIN_ROW_COUNT,
            to=MAX_ROW_COUNT,
            textvariable=self.rowCount,
            width=5
        ).pack(side=RIGHT)

        Label(panel, text=' x ').pack(side=RIGHT)

        self.columnCount = StringVar(panel)
        self.columnCount.set(self.model.columnCount)
        Spinbox(
            panel,
            from_=MIN_COLUMN_COUNT,
            to=MAX_COLUMN_COUNT,
            textvariable=self.columnCount,
            width=5
        ).pack(side=RIGHT)
        Label(panel, text='Размер поля: ').pack(side=RIGHT)

    def syncWithModel(self):
        for row in range(self.model.rowCount):
            for column in range(self.model.columnCount):
                cell = self.model.getCell(row, column)
                if cell:
                    btn = self.buttonsTable[row][column]

                    if self.model.isGameOver() and cell.mined:
                        btn.config(bg='black', text='')

                    if cell.state == 'closed':
                        btn.config(text='')
                    elif cell.state == 'opened':
                        btn.config(relief=SUNKEN, text='')
                        if cell.counter > 0:
                            btn.config(text=cell.counter)
                        elif cell.mined:
                            btn.config(bg='red')
                    elif cell.state == 'flagged':
                        btn.config(text='P')
                    elif cell.state == 'questioned':
                        btn.config(text='?')

    def blockCell(self, row, column, block=True):
        btn = self.buttonsTable[row][column]
        if not btn:
            return

        if block:
            btn.bind('<Button-1>', 'break')
        else:
            btn.unbind('<Button-1>')

    def getGameSettings(self):
        return self.rowCount.get(), self.columnCount.get(), self.mineCount.get()

    def createBoard(self):
        try:
            self.board.pack_forget()
            self.board.destroy()

            self.rowCount.set(self.model.rowCount)
            self.columnCount.set(self.model.columnCount)
            self.mineCount.set(self.model.mineCount)
        except:
            pass

        self.board = Frame(self)
        self.board.pack()
        self.buttonsTable = []
        for row in range(self.model.rowCount):
            line = Frame(self.board)
            line.pack(side=TOP)
            self.buttonsRow = []
            for column in range(self.model.columnCount):
                btn = Button(
                    line,
                    width=2,
                    height=1,
                    command=lambda row=row, column=column: self.controller.onLeftClick(row, column),
                    padx=0,
                    pady=0
                )
                btn.pack(side=LEFT)
                btn.bind(
                    '<Button-3>',
                    lambda e, row=row, column=column: self.controller.onRightClick(row, column)
                )
                self.buttonsRow.append(btn)

            self.buttonsTable.append(self.buttonsRow)

    def showWinMessage(self):
        showinfo('Поздравляем!', 'Вы победили!')

    def showGameOverMessage(self):
        showinfo('Игра окончена!', 'Вы проиграли!')