import Model
import View
import Control

model = Model.MinesweeperModel()
controller = Control.MinesweeperController(model)
view = View.MinesweeperView(model, controller)
view.pack()
view.mainloop()
