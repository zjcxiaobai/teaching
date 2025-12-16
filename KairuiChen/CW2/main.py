import main_window

if __name__ == '__main__':
    import os
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent
    os.chdir(BASE_DIR)
    print("CWD is now:", os.getcwd())

    window = main_window.MainWindow()
    window.run()
