# main.py
# ---------------------------------------------------------------
# Entry point for the Bond Calculator application.
# This file simply imports the UI and launches the app.
# All logic lives in logic/calculator.py
# All UI lives in ui/app_window.py
# ---------------------------------------------------------------

from ui.app_window import BondCalculatorApp

if __name__ == "__main__":
    # Create an instance of the app and start the UI event loop.
    # mainloop() keeps the window open and listening for user input.
    app = BondCalculatorApp()
    app.mainloop()
    