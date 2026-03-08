#!/usr/bin/env python3
"""
DevForge Project Verification Script
This script verifies that all components are properly set up.
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print_success(f"{description}: Found")
        return True
    else:
        print_error(f"{description}: Missing")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if Path(dirpath).is_dir():
        print_success(f"{description}: Found")
        return True
    else:
        print_error(f"{description}: Missing")
        return False

def count_files_in_dir(dirpath, pattern="*"):
    """Count files in a directory."""
    return len(list(Path(dirpath).glob(pattern)))

def main():
    print_header("DevForge Project Verification")
    
    # Get project root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    issues = []
    
    # 1. Check Project Structure
    print_header("1. Project Structure")
    
    dirs_to_check = [
        ("backend", "Backend directory"),
        ("backend/agents", "Agents directory"),
        ("backend/api", "API directory"),
        ("backend/workflows", "Workflows directory"),
        ("backend/project_manager", "Project Manager directory"),
        ("frontend", "Frontend directory"),
        ("frontend/app", "Frontend app directory"),
        ("frontend/components", "Components directory"),
        ("frontend/lib", "Lib directory"),
        ("docs", "Documentation directory"),
        ("generated_projects", "Generated projects directory"),
    ]
    
    for dir_path, description in dirs_to_check:
        if not check_directory_exists(dir_path, description):
            issues.append(f"Missing directory: {dir_path}")
    
    # 2. Check Backend Files
    print_header("2. Backend Files")
    
    backend_files = [
        ("backend/main.py", "Main application"),
        ("backend/config.py", "Configuration"),
        ("backend/database.py", "Database models"),
        ("backend/requirements.txt", "Requirements"),
        ("backend/.env.example", "Environment template"),
        ("backend/agents/base_agent.py", "Base agent"),
        ("backend/agents/product_manager.py", "Product Manager agent"),
        ("backend/agents/software_architect.py", "Software Architect agent"),
        ("backend/agents/backend_developer.py", "Backend Developer agent"),
        ("backend/agents/frontend_developer.py", "Frontend Developer agent"),
        ("backend/agents/qa_tester.py", "QA Tester agent"),
        ("backend/agents/code_reviewer.py", "Code Reviewer agent"),
    ]
    
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            issues.append(f"Missing backend file: {file_path}")
    
    # Count agent files
    agent_count = count_files_in_dir("backend/agents", "*.py")
    print_info(f"Total agent files: {agent_count}")
    
    # 3. Check Frontend Files
    print_header("3. Frontend Files")
    
    frontend_files = [
        ("frontend/package.json", "Package configuration"),
        ("frontend/tsconfig.json", "TypeScript configuration"),
        ("frontend/tailwind.config.js", "Tailwind configuration"),
        ("frontend/.env.local.example", "Environment template"),
        ("frontend/app/layout.tsx", "Root layout"),
        ("frontend/app/page.tsx", "Home page"),
        ("frontend/lib/api.ts", "API client"),
        ("frontend/lib/utils.ts", "Utilities"),
        ("frontend/components/Navbar.tsx", "Navbar component"),
        ("frontend/components/CreateProjectDialog.tsx", "Create dialog"),
        ("frontend/components/ProjectCard.tsx", "Project card"),
    ]
    
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            issues.append(f"Missing frontend file: {file_path}")
    
    # Count component files
    component_count = count_files_in_dir("frontend/components", "*.tsx")
    print_info(f"Total component files: {component_count}")
    
    # 4. Check Documentation
    print_header("4. Documentation")
    
    doc_files = [
        ("README.md", "Main README"),
        ("QUICKSTART.md", "Quick start guide"),
        ("CONTRIBUTING.md", "Contributing guide"),
        ("LICENSE", "License file"),
        ("CHANGELOG.md", "Changelog"),
        ("ROADMAP.md", "Roadmap"),
        ("docs/GETTING_STARTED.md", "Getting started"),
        ("docs/SETUP.md", "Setup guide"),
        ("docs/ARCHITECTURE.md", "Architecture docs"),
        ("docs/API.md", "API reference"),
        ("docs/AGENTS.md", "Agents guide"),
    ]
    
    for file_path, description in doc_files:
        if not check_file_exists(file_path, description):
            issues.append(f"Missing documentation: {file_path}")
    
    # 5. Check Configuration Files
    print_header("5. Configuration Files")
    
    config_files = [
        (".gitignore", "Git ignore"),
        (".env.example", "Environment example"),
        ("docker-compose.yml", "Docker Compose"),
        ("backend/Dockerfile", "Backend Dockerfile"),
        ("frontend/Dockerfile", "Frontend Dockerfile"),
        ("setup.sh", "Linux setup script"),
        ("setup.bat", "Windows setup script"),
    ]
    
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            issues.append(f"Missing configuration: {file_path}")
    
    # 6. Check Environment Setup
    print_header("6. Environment Setup")
    
    if Path("backend/.env").exists():
        print_success("Backend .env file exists")
        # Check if API key is set
        with open("backend/.env") as f:
            content = f.read()
            if "OPENAI_API_KEY=sk-" in content and "your" not in content.lower():
                print_success("OpenAI API key appears to be set")
            else:
                print_warning("OpenAI API key may not be configured")
                issues.append("OpenAI API key not properly configured")
    else:
        print_warning("Backend .env file not created (run setup script)")
    
    if Path("frontend/.env.local").exists():
        print_success("Frontend .env.local file exists")
    else:
        print_warning("Frontend .env.local not created (run setup script)")
    
    # Check virtual environment
    if Path("backend/venv").is_dir():
        print_success("Python virtual environment exists")
    else:
        print_warning("Python virtual environment not created (run setup script)")
    
    # Check node_modules
    if Path("frontend/node_modules").is_dir():
        print_success("Node modules installed")
    else:
        print_warning("Node modules not installed (run setup script)")
    
    # 7. Project Statistics
    print_header("7. Project Statistics")
    
    # Count Python files
    py_files = list(Path("backend").rglob("*.py"))
    print_info(f"Python files: {len(py_files)}")
    
    # Count TypeScript/TSX files
    ts_files = list(Path("frontend").rglob("*.ts")) + list(Path("frontend").rglob("*.tsx"))
    print_info(f"TypeScript files: {len(ts_files)}")
    
    # Count markdown files
    md_files = list(Path(".").rglob("*.md"))
    print_info(f"Documentation files: {len(md_files)}")
    
    # Estimate lines of code
    total_lines = 0
    for file_path in py_files + ts_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    
    print_info(f"Estimated lines of code: {total_lines}")
    
    # 8. Final Report
    print_header("Verification Summary")
    
    if issues:
        print_error(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print_success("All checks passed! ✨")
    
    print("\n" + "="*60)
    
    if Path("backend/venv").is_dir() and Path("frontend/node_modules").is_dir():
        print_success("Project appears to be fully set up!")
        print_info("\nTo start the application:")
        print_info("  1. Backend: cd backend && source venv/bin/activate && python main.py")
        print_info("  2. Frontend: cd frontend && npm run dev")
    else:
        print_warning("Project structure exists but dependencies not installed")
        print_info("\nRun the setup script:")
        print_info("  ./setup.sh (Linux/Mac) or setup.bat (Windows)")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if not issues else 1

if __name__ == "__main__":
    sys.exit(main())
