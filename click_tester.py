import argparse
import subprocess
# python click_tester_cli.py --button_top 347 --button_left 1538 --button_width 50 --button_height 50
def main():
    parser = argparse.ArgumentParser(description='Automated Screen Clicker')
    parser.add_argument('--button_top', type=int, default=347, help='Button Top coordinate')
    parser.add_argument('--button_left', type=int, default=1538, help='Button Left coordinate')
    parser.add_argument('--button_width', type=int, default=50, help='Button Width')
    parser.add_argument('--button_height', type=int, default=50, help='Button Height')
    args = parser.parse_args()

    click_process = subprocess.Popen([
        'python', 'click_process.py', str(args.button_top), str(args.button_left), str(args.button_width), str(args.button_height)
    ])

    input("Press Enter to stop the clicking process...")
    click_process.terminate()

if __name__ == "__main__":
    main()