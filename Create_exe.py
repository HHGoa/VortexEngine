import subprocess
import sys

def create_exe_with_pyshield(script_name, exe_name, levels=1):
    try:
        # Note: Ensure the '-o' flag is properly used if PyShield expects it to be a directory or a file name.
        subprocess.run(['pyshield', '-f', script_name, '-l', str(levels), '-o', exe_name], check=True)
        print(f"Executable {exe_name} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the executable: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_exe.py <script_name> <exe_name> <levels>")
    else:
        script_name = sys.argv[1]
        exe_name = sys.argv[2]
        levels = int(sys.argv[3])
        create_exe_with_pyshield(script_name, exe_name, levels)
