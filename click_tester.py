import argparse
import time
from pywinauto.application import Application

def main():
    parser = argparse.ArgumentParser(description='Automated Screen Clicker')
    parser.add_argument('--button_top', type=int, default=347, help='Button Top coordinate')
    parser.add_argument('--button_left', type=int, default=1538, help='Button Left coordinate')
    parser.add_argument('--button_width', type=int, default=50, help='Button Width')
    parser.add_argument('--button_height', type=int, default=50, help='Button Height')
    parser.add_argument('--repeat', type=int, default=2, help='Number of times to repeat the clicking process')
    args = parser.parse_args()

    # Connect to the window named "Newton"
    app = Application(backend="uia").connect(title='Newton')
    dlg = app.window(title='Newton')

    for _ in range(args.repeat):
        dlg.click_input(coords=(args.button_left + args.button_width // 2, args.button_top + args.button_height // 2))
        time.sleep(1)  # Wait for 1 second between clicks

if __name__ == "__main__":
    main()