#!/usr/bin/env python3
"""
Quality check script for Django project.
Run with: python scripts/run_quality_checks.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} passed")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Run all quality checks."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    checks = [
        # Linting
        ("flake8 alx_travel_app/ --max-line-length=120 --exclude=migrations", "Flake8 linting"),
        
        # Formatting
        ("black --check alx_travel_app/", "Black formatting check"),
        
        # Import sorting
        ("isort --check-only alx_travel_app/", "Import sorting check"),
        
        # Type checking (optional)
        # ("mypy alx_travel_app/ --ignore-missing-imports", "MyPy type checking"),
        
        # Security
        ("bandit -r alx_travel_app/ -ll --exclude alx_travel_app/migrations", "Bandit security scan"),
        
        # Complexity
        ("radon cc alx_travel_app/ -s -a", "Radon complexity analysis"),
        
        # Maintainability
        ("radon mi alx_travel_app/ -s", "Radon maintainability index"),
    ]
    
    print("🔍 Running Django Project Quality Checks")
    print(f"Project: {project_root.name}")
    print(f"Directory: {project_root}")
    
    failed_checks = []
    
    for cmd, description in checks:
        if not run_command(cmd, description):
            failed_checks.append(description)
    
    # Summary
    print(f"\n{'='*60}")
    print("QUALITY CHECK SUMMARY")
    print('='*60)
    
    if failed_checks:
        print(f"❌ Failed checks ({len(failed_checks)}):")
        for check in failed_checks:
            print(f"  - {check}")
        sys.exit(1)
    else:
        print("✅ All quality checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
    