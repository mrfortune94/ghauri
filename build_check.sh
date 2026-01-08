#!/bin/bash
# Ghauri Android App - Quick Build Test Script
# This script helps verify that the build environment is set up correctly

set -e  # Exit on error

echo "=========================================="
echo "Ghauri Android App - Build Test"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "1. Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
    echo -e "${GREEN}✓${NC} Python version: $(python3 --version)"
else
    echo -e "${RED}✗${NC} Python 3.7+ required, found: $(python3 --version)"
    exit 1
fi

# Check if pip is installed
echo "2. Checking pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip3 is installed: $(pip3 --version)"
else
    echo -e "${RED}✗${NC} pip3 is not installed"
    exit 1
fi

# Check if buildozer is installed
echo "3. Checking buildozer..."
if command -v buildozer &> /dev/null; then
    echo -e "${GREEN}✓${NC} Buildozer is installed: $(buildozer --version 2>&1 | head -1)"
else
    echo -e "${YELLOW}⚠${NC} Buildozer is not installed"
    echo "   Installing buildozer..."
    pip3 install --user buildozer
    echo -e "${GREEN}✓${NC} Buildozer installed"
fi

# Validate buildozer.spec
echo "4. Validating buildozer.spec..."
if [ -f "buildozer.spec" ]; then
    echo -e "${GREEN}✓${NC} buildozer.spec exists"
    
    # Check for required fields
    if grep -q "^title = " buildozer.spec && \
       grep -q "^package.name = " buildozer.spec && \
       grep -q "^requirements = " buildozer.spec; then
        echo -e "${GREEN}✓${NC} buildozer.spec has required fields"
    else
        echo -e "${RED}✗${NC} buildozer.spec is missing required fields"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} buildozer.spec not found"
    exit 1
fi

# Validate main.py
echo "5. Validating main.py..."
if [ -f "main.py" ]; then
    echo -e "${GREEN}✓${NC} main.py exists"
    
    # Check Python syntax
    if python3 -m py_compile main.py 2>/dev/null; then
        echo -e "${GREEN}✓${NC} main.py has valid Python syntax"
    else
        echo -e "${RED}✗${NC} main.py has syntax errors"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} main.py not found"
    exit 1
fi

# Check if required dependencies can be installed
echo "6. Checking Python dependencies..."
DEPS="tldextract colorama requests chardet ua_generator"
MISSING_DEPS=""

for dep in $DEPS; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $dep is installed"
    else
        MISSING_DEPS="$MISSING_DEPS $dep"
    fi
done

if [ -n "$MISSING_DEPS" ]; then
    echo -e "${YELLOW}⚠${NC} Some dependencies are missing:$MISSING_DEPS"
    echo "   You can install them with: pip3 install -r requirements.txt"
else
    echo -e "${GREEN}✓${NC} All core dependencies are installed"
fi

# Check for Java (required for Android builds)
echo "7. Checking Java..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -1)
    echo -e "${GREEN}✓${NC} Java is installed: $JAVA_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Java is not installed"
    echo "   Install with: sudo apt install openjdk-11-jdk"
fi

# Check for system dependencies (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "8. Checking system build dependencies..."
    MISSING_PKGS=""
    
    # Check for essential build tools
    for cmd in git zip unzip; do
        if ! command -v $cmd &> /dev/null; then
            MISSING_PKGS="$MISSING_PKGS $cmd"
        fi
    done
    
    if [ -n "$MISSING_PKGS" ]; then
        echo -e "${YELLOW}⚠${NC} Some system packages are missing:$MISSING_PKGS"
        echo "   Install with: sudo apt install$MISSING_PKGS"
    else
        echo -e "${GREEN}✓${NC} Essential system packages are installed"
    fi
else
    echo "8. Skipping system dependency check (not on Linux)"
fi

echo ""
echo "=========================================="
echo "Build Environment Check Complete!"
echo "=========================================="
echo ""

if [ -z "$MISSING_DEPS" ] && [ -z "$MISSING_PKGS" ]; then
    echo -e "${GREEN}✓ Your environment is ready for building!${NC}"
    echo ""
    echo "To build the Android APK, run:"
    echo "  buildozer android debug"
    echo ""
    echo "For more information, see ANDROID_BUILD.md"
else
    echo -e "${YELLOW}⚠ Some dependencies are missing${NC}"
    echo ""
    echo "Install missing dependencies and run this script again."
    echo "See ANDROID_BUILD.md for complete setup instructions."
fi

echo ""
