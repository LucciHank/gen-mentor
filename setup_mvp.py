#!/usr/bin/env python3
"""
GenMentor MVP Setup Script
Automates the complete setup process for the MVP demo
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def check_prerequisites():
    """Check if required tools are installed"""
    print("Checking prerequisites...")
    
    required_tools = {
        'python': 'python --version',
        'pip': 'pip --version',
        'psql': 'psql --version'
    }
    
    missing_tools = []
    
    for tool, command in required_tools.items():
        result = run_command(command, check=False)
        if result.returncode != 0:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"Missing required tools: {', '.join(missing_tools)}")
        print("Please install the missing tools and run this script again.")
        return False
    
    print("All prerequisites are installed.")
    return True

def setup_backend():
    """Setup backend environment and dependencies"""
    print("\n=== Setting up Backend ===")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Backend directory not found!")
        return False
    
    # Create virtual environment
    print("Creating virtual environment...")
    run_command("python -m venv .venv", cwd=backend_dir)
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = backend_dir / ".venv" / "Scripts" / "activate"
        pip_path = backend_dir / ".venv" / "Scripts" / "pip"
        python_path = backend_dir / ".venv" / "Scripts" / "python"
    else:  # Unix/Linux/Mac
        activate_script = backend_dir / ".venv" / "bin" / "activate"
        pip_path = backend_dir / ".venv" / "bin" / "pip"
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    # Install dependencies
    print("Installing Python dependencies...")
    run_command(f"{pip_path} install --upgrade pip", cwd=backend_dir)
    run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
    
    # Copy environment file
    env_example = backend_dir / ".env.example"
    env_file = backend_dir / ".env"
    
    if env_example.exists() and not env_file.exists():
        print("Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print("Please edit backend/.env with your actual configuration values.")
    
    # Create necessary directories
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "uploads").mkdir(exist_ok=True)
    (data_dir / "vectorstore").mkdir(exist_ok=True)
    
    print("Backend setup completed.")
    return True

def setup_frontend():
    """Setup frontend environment and dependencies"""
    print("\n=== Setting up Frontend ===")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("Frontend directory not found!")
        return False
    
    # Create virtual environment
    print("Creating virtual environment...")
    run_command("python -m venv .venv", cwd=frontend_dir)
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = frontend_dir / ".venv" / "Scripts" / "pip"
    else:  # Unix/Linux/Mac
        pip_path = frontend_dir / ".venv" / "bin" / "pip"
    
    # Install dependencies
    print("Installing Python dependencies...")
    run_command(f"{pip_path} install --upgrade pip", cwd=frontend_dir)
    run_command(f"{pip_path} install -r requirements.txt", cwd=frontend_dir)
    
    print("Frontend setup completed.")
    return True

def setup_database():
    """Setup database and seed data"""
    print("\n=== Setting up Database ===")
    
    # Check if PostgreSQL is running
    result = run_command("pg_isready", check=False)
    if result.returncode != 0:
        print("PostgreSQL is not running. Please start PostgreSQL and run this script again.")
        print("On Ubuntu/Debian: sudo systemctl start postgresql")
        print("On macOS with Homebrew: brew services start postgresql")
        print("On Windows: Start PostgreSQL service from Services panel")
        return False
    
    # Run database setup script
    backend_dir = Path("backend")
    if os.name == 'nt':  # Windows
        python_path = backend_dir / ".venv" / "Scripts" / "python"
    else:  # Unix/Linux/Mac
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    print("Running database setup script...")
    run_command(f"{python_path} scripts/setup_database.py", cwd=backend_dir)
    
    print("Running document ingestion script...")
    run_command(f"{python_path} scripts/ingest_documents.py", cwd=backend_dir)
    
    print("Database setup completed.")
    return True

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n=== Creating startup scripts ===")
    
    # Backend startup script
    backend_script_content = """#!/bin/bash
# GenMentor Backend Startup Script

echo "Starting GenMentor Backend..."
cd backend

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Start the server
python main.py
"""
    
    with open("start_backend.sh", "w") as f:
        f.write(backend_script_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod("start_backend.sh", 0o755)
    
    # Frontend startup script
    frontend_script_content = """#!/bin/bash
# GenMentor Frontend Startup Script

echo "Starting GenMentor Frontend..."
cd frontend

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Start Streamlit
streamlit run main.py
"""
    
    with open("start_frontend.sh", "w") as f:
        f.write(frontend_script_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod("start_frontend.sh", 0o755)
    
    # Windows batch files
    if os.name == 'nt':
        backend_bat = """@echo off
echo Starting GenMentor Backend...
cd backend
call .venv\\Scripts\\activate
python main.py
"""
        with open("start_backend.bat", "w") as f:
            f.write(backend_bat)
        
        frontend_bat = """@echo off
echo Starting GenMentor Frontend...
cd frontend
call .venv\\Scripts\\activate
streamlit run main.py
"""
        with open("start_frontend.bat", "w") as f:
            f.write(frontend_bat)
    
    print("Startup scripts created.")

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "="*60)
    print("🎉 GenMentor MVP Setup Complete!")
    print("="*60)
    
    print("\nNext steps:")
    print("1. Edit backend/.env with your API keys and database credentials")
    print("2. Make sure PostgreSQL is running")
    print("3. Start the backend server:")
    if os.name == 'nt':
        print("   - Windows: double-click start_backend.bat")
        print("   - Or run: cd backend && .venv\\Scripts\\activate && python main.py")
    else:
        print("   - Run: ./start_backend.sh")
        print("   - Or run: cd backend && source .venv/bin/activate && python main.py")
    
    print("4. Start the frontend (in a new terminal):")
    if os.name == 'nt':
        print("   - Windows: double-click start_frontend.bat")
        print("   - Or run: cd frontend && .venv\\Scripts\\activate && streamlit run main.py")
    else:
        print("   - Run: ./start_frontend.sh")
        print("   - Or run: cd frontend && source .venv/bin/activate && streamlit run main.py")
    
    print("\n📍 Access points:")
    print("   - Backend API: http://localhost:5000")
    print("   - Frontend UI: http://localhost:8501")
    print("   - API Documentation: http://localhost:5000/docs")
    
    print("\n🔧 Configuration:")
    print("   - Backend config: backend/.env")
    print("   - Frontend config: frontend/config.py")
    
    print("\n📚 Documentation:")
    print("   - Project structure: .kiro/steering/structure.md")
    print("   - Technology stack: .kiro/steering/tech.md")
    print("   - Product overview: .kiro/steering/product.md")

def main():
    """Main setup function"""
    print("GenMentor MVP Setup")
    print("==================")
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Setup components
    if not setup_backend():
        return False
    
    if not setup_frontend():
        return False
    
    if not setup_database():
        print("Database setup failed. You can run it manually later:")
        print("cd backend && python scripts/setup_database.py")
    
    # Create startup scripts
    create_startup_scripts()
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)