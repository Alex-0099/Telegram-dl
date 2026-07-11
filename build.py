import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Checks if PyInstaller is installed in the current Python environment."""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller is not installed. Installing it now...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            return True
        except Exception as e:
            print(f"Failed to install PyInstaller: {str(e)}")
            return False

def build_executable():
    if not check_pyinstaller():
        print("Error: PyInstaller is required to build the executable.")
        sys.exit(1)
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "telegram-dl.py")
    
    if not os.path.exists(main_script):
        print(f"Error: Main script not found at {main_script}")
        sys.exit(1)
        
    print("Building standard CLI executable...")
    
    # Define build command arguments
    # --onefile: bundle everything into a single EXE
    # --name: name of the output executable
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=telegram-dl",
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "--exclude-module=tkinter",
        main_script
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print(f"Your executable is located at: {os.path.join(current_dir, 'dist', 'telegram-dl.exe')}")
        
        # Clean up temporary build artifacts
        print("\nCleaning up temporary files...")
        build_dir = os.path.join(current_dir, "build")
        spec_file = os.path.join(current_dir, "telegram-dl.spec")
        
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
            print("Removed build/ directory.")
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print("Removed telegram-dl.spec file.")
            
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
