import sys
import main_window


def run_from_right_click(arg):
    main_window.main_window()


def run_as_standalone_application():
    print("Right Click Menu Not Configured Properly.")
    return None


if __name__ == "__main__":
    try:
        run_from_right_click(sys.argv[1])
    except:
        run_as_standalone_application()
