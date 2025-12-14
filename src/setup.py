#!/usr/bin/env python3
"""
Setup script for UCB Driver Coupon Analysis EDA Project
This script checks for required packages and virtual environment setup.
"""

import sys
import subprocess
import os
import importlib.util
from pathlib import Path

# Required packages for the EDA project 
# TODO - can this be synced with requirements.txt automatically?
REQUIRED_PACKAGES = {
    'pandas': 'pandas>=1.3.0',
    'numpy': 'numpy>=1.21.0',
    'seaborn': 'seaborn>=0.11.0',
    'plotly': 'plotly>=5.0.0',
    'jupyter': 'jupyter>=1.0.0',
    'matplotlib': 'matplotlib>=3.3.0',
    'kaleido': 'kaleido>=0.2.1'
}

def check_python_version():
    """Check if Python version is compatible."""
    min_version = (3, 7) # I am using 3.14 locally, check and modify later. Explore if you can check for Conda instead
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"Python {min_version[0]}.{min_version[1]}+ is required. Current version: {sys.version}")
        return False
    
    print(f"Python version {sys.version.split()[0]} is compatible")
    return True

def check_virtual_environment():
    """Check if running in a virtual environment."""
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )
    
    if in_venv:
        venv_path = os.environ.get('VIRTUAL_ENV', sys.prefix)
        print(f"Virtual environment detected: {venv_path}")
        return True
    else:
        print("No virtual environment detected")
        return False

def check_package_installed(package_name):
    """Check if a package is installed and importable."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            # Try to import to ensure it's working
            __import__(package_name)
            return True
    except ImportError:
        pass
    return False

def get_package_version(package_name):
    """Get the version of an installed package."""
    try:
        module = __import__(package_name)
        return getattr(module, '__version__', 'Unknown')
    except (ImportError, AttributeError):
        return None

def install_package(package_spec):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_spec])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_packages():
    """Check for required packages and offer to install missing ones."""
    missing_packages = []
    installed_packages = []
    
    print("\n Checking required packages...")
    print("-" * 50)
    
    for package_name, package_spec in REQUIRED_PACKAGES.items():
        if check_package_installed(package_name):
            version = get_package_version(package_name)
            print(f"{package_name} {version}")
            installed_packages.append(package_name)
        else:
            print(f"{package_name} - Not installed")
            missing_packages.append((package_name, package_spec))
    
    if missing_packages:
        print(f"\nMissing {len(missing_packages)} required package(s)")
        print("\nMissing packages:")
        for pkg_name, pkg_spec in missing_packages:
            print(f"  - {pkg_name}")
        
        response = input("\nWould you like to install missing packages? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            print("\n🔧 Installing missing packages...")
            failed_installs = []
            
            for pkg_name, pkg_spec in missing_packages:
                print(f"Installing {pkg_name}...")
                if install_package(pkg_spec):
                    print(f"Successfully installed {pkg_name}")
                else:
                    print(f"Failed to install {pkg_name}")
                    failed_installs.append(pkg_name)
            
            if failed_installs:
                print(f"\nFailed to install: {', '.join(failed_installs)}")
                print("Please install them manually using:")
                for pkg_name in failed_installs:
                    pkg_spec = next(spec for name, spec in missing_packages if name == pkg_name)
                    print(f"  pip install {pkg_spec}")
                return False
            else:
                print("\nAll packages installed successfully!")
                return True
        else:
            print("\nSetup cancelled. Please install required packages manually:")
            for pkg_name, pkg_spec in missing_packages:
                print(f"  pip install {pkg_spec}")
            return False
    else:
        print("\nAll required packages are installed!")
        return True

def create_requirements_file():
    """Create a requirements.txt file for easy installation."""
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_path.exists():
        print(f"\nCreating requirements.txt file...")
        with open(requirements_path, 'w') as f:
            f.write("# UCB Driver Coupon Analysis EDA Requirements\n")
            f.write("# Install with: pip install -r requirements.txt\n\n")
            for package_spec in REQUIRED_PACKAGES.values():
                f.write(f"{package_spec}\n")
        print(f"Created {requirements_path}")
    else:
        print(f"Requirements file already exists: {requirements_path}")

def print_setup_instructions():
    """Print setup instructions for users."""
    print("\n" + "="*60)
    print("UCB DRIVER COUPON ANALYSIS - SETUP GUIDE")
    print("="*60)
    
    print("\nRECOMMENDED SETUP STEPS:")
    print("1. Create a virtual environment:")
    print("   python -m venv venv")
    print("\n2. Activate the virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   macOS/Linux: source venv/bin/activate")
    print("\n3. Install required packages:")
    print("   pip install -r requirements.txt")
    print("   OR run this setup script again")
    print("\n4. Start Jupyter Notebook:")
    print("   jupyter notebook")
    print("\n5. Open the analysis notebook:")
    print("   prompt.ipynb")

def main():
    """Main setup function."""
    print("UCB Driver Coupon Analysis - Environment Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    venv_active = check_virtual_environment()
    
    if not venv_active:
        print("\nRECOMMENDATION: Use a virtual environment")
        print("This helps avoid package conflicts with your system Python.")
        
        response = input("\nContinue without virtual environment? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            print_setup_instructions()
            sys.exit(0)
    
    # Create requirements file
    create_requirements_file()
    
    # Check and install packages
    packages_ready = check_and_install_packages()
    
    if packages_ready:
        print("\nSETUP COMPLETE!")
        print("="*30)
        print("All dependencies are installed")
        
        print("\nNext steps:")
        print("1. Open Jupyter Notebook: jupyter notebook")
        print("2. Navigate to and open: prompt.ipynb")
        print("3. Run the cells to start your EDA!")
        
        # Check if Jupyter is available
        if check_package_installed('jupyter'):
            response = input("\nWould you like to start Jupyter Notebook now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                try:
                    subprocess.run([sys.executable, '-m', 'jupyter', 'notebook'])
                except KeyboardInterrupt:
                    print("\nJupyter Notebook stopped")
                except Exception as e:
                    print(f"\nError starting Jupyter: {e}")
    else:
        print("\nSETUP INCOMPLETE")
        print("Please resolve the package installation issues above.")
        print_setup_instructions()
        sys.exit(1)

if __name__ == "__main__":
    main()