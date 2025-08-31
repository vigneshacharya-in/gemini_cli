import pathlib
import os

def validate_assets_folder():
    """
    This script checks for the existence of an 'assets' folder
    in the same directory and lists its contents. It specifically
    looks for 'icon.png'.
    """
    print("--- Flet Assets Validator ---")

    try:
        # Get the directory where this script is running from
        script_dir = pathlib.Path(__file__).parent.resolve()
        print(f"\n🔎 Searching in directory: {script_dir}\n")

        # Define the expected path to the 'assets' folder
        assets_path = script_dir / "assets"

        # --- Check 1: Does the 'assets' folder exist? ---
        if not assets_path.exists():
            print(f"❌ ERROR: The 'assets' folder was NOT found.")
            print(f"   Expected location: {assets_path}")
            print("\n   ACTION: Please create an 'assets' folder in the same directory as your script.")
            return # Stop the script
        
        if not assets_path.is_dir():
            print(f"❌ ERROR: A file named 'assets' was found, but it is NOT a folder.")
            print(f"   Location: {assets_path}")
            print("\n   ACTION: Please remove the 'assets' file and create a folder with that name.")
            return # Stop the script

        print(f"✅ SUCCESS: 'assets' folder found at: {assets_path}")

        # --- Check 2: List the contents of the 'assets' folder ---
        print("\n--- Listing contents of 'assets' folder ---")
        
        try:
            contents = list(assets_path.iterdir())
            if not contents:
                print("   The 'assets' folder is empty.")
            else:
                for item in contents:
                    item_type = "[Folder]" if item.is_dir() else "[File]"
                    print(f"   {item_type.ljust(8)} {item.name}")
        except OSError as e:
            print(f"   ❌ ERROR: Could not read the contents of the 'assets' folder due to a permission error: {e}")
            return
            
        print("-------------------------------------------\n")

        # --- Check 3: Specifically look for 'icon.png' ---
        icon_path = assets_path / "icon.png"
        
        if icon_path.exists() and icon_path.is_file():
            print("✅ SUCCESS: 'icon.png' was found inside the 'assets' folder.")
            print("   The path './assets/icon.png' should now work in your Flet app.")
        else:
            print("❌ WARNING: 'icon.png' was NOT found inside the 'assets' folder.")
            print("   ACTION: Make sure your icon file is:")
            print("   1. Placed directly inside the 'assets' folder.")
            print("   2. Named exactly 'icon.png' (lowercase).")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please ensure you are running this script with Python.")

if __name__ == "__main__":
    validate_assets_folder()