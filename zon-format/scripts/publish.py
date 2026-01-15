import os
import sys
import subprocess
import shutil
import argparse

def run_command(command, description=None):
    if description:
        print(f"🔄 {description}...")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during: {description or command}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="LUX Project Publishing Tool (Powered by UV)")
    parser.add_argument("--env", choices=["test", "prod"], default="test", help="Target environment (test or prod)")
    parser.add_argument("--skip-build", action="store_true", help="Skip the build step")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    print(f"🏗️  Preparing to publish LUX to {args.env.upper()} (using UV)...")

    # 1. Check for UV
    try:
        subprocess.check_output("uv --version", shell=True)
    except:
        print("❌ UV is not installed. Please install it from https://github.com/astral-sh/uv")
        sys.exit(1)

    # 2. Clean
    if not args.skip_build:
        print("🧹 Cleaning old builds...")
        for folder in ['build', 'dist']:
            shutil.rmtree(folder, ignore_errors=True)
        # Clean egg-info
        for path in os.listdir('.'):
            if path.endswith('.egg-info'):
                shutil.rmtree(path, ignore_errors=True)

        # 3. Build using UV
        run_command("uv build", "Building package (using uv build)")

    # 4. Check using UVX
    run_command("uvx twine check dist/*", "Checking distribution archives (using uvx twine)")

    # 5. Upload using UVX
    if args.env == "test":
        print("\n🚀 Uploading to TestPyPI...")
        run_command("uvx twine upload --repository testpypi dist/*", "Uploading to TestPyPI")
    else:
        print("\n🔥 WARNING: Uploading to PRODUCTION PyPI...")
        confirm = input("Are you sure you want to upload to production? (y/N): ")
        if confirm.lower() == 'y':
            run_command("uvx twine upload dist/*", "Uploading to PyPI")
        else:
            print("🚫 Upload cancelled.")

    print("\n✅ Process completed!")

if __name__ == "__main__":
    main()
