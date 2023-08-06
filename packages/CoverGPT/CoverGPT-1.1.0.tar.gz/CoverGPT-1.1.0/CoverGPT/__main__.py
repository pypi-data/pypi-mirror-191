import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gui import App

app = App()
app.mainloop()
