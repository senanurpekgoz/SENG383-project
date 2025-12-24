#!/usr/bin/env python3
"""
Test script to verify BeePlan can run
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Importing PyQt5...")
    from PyQt5.QtWidgets import QApplication
    print("✓ PyQt5 imported successfully")
    
    print("Importing scheduler...")
    from scheduler import Course, Instructor, Room
    print("✓ Scheduler imported successfully")
    
    print("Importing main_gui...")
    from main_gui import BeePlanGUI
    print("✓ Main GUI imported successfully")
    
    print("\nStarting application...")
    app = QApplication(sys.argv)
    window = BeePlanGUI()
    window.show()
    print("✓ Application started! Window should be visible now.")
    print("\nPress Ctrl+C to exit or close the window.")
    
    sys.exit(app.exec_())
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nPlease install PyQt5:")
    print("  pip install PyQt5")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


