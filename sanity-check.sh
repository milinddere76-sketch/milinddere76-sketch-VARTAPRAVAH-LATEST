#!/bin/bash

# VartaPravah Pre-Deployment Sanity Check
# Run this script to verify your system is ready for deployment

echo "=================================="
echo "VartaPravah Sanity Check"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((CHECKS_FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((CHECKS_WARNING++))
}

# 1. Check Docker
echo "1. Checking Docker Installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    pass "Docker installed: $DOCKER_VERSION"
else
    fail "Docker not installed"
fi

# 2. Check Docker Compose
echo ""
echo "2. Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    DC_VERSION=$(docker-compose --version)
    pass "Docker Compose installed: $DC_VERSION"
else
    fail "Docker Compose not installed"
fi

# 3. Check Docker daemon
echo ""
echo "3. Checking Docker Daemon..."
if docker ps &> /dev/null; then
    pass "Docker daemon is running"
else
    fail "Docker daemon is not running"
fi

# 4. Check .env file
echo ""
echo "4. Checking Configuration..."
if [ -f .env ]; then
    pass ".env file exists"
    if grep -q "YOUTUBE_STREAM_KEY=" .env; then
        STREAM_KEY=$(grep "YOUTUBE_STREAM_KEY=" .env | cut -d= -f2)
        if [ "$STREAM_KEY" != "" ] && [ "$STREAM_KEY" != "your_stream_key_here" ]; then
            pass "YouTube Stream Key is configured"
        else
            fail "YouTube Stream Key not set (use 'your actual key')"
        fi
    else
        fail "YOUTUBE_STREAM_KEY not found in .env"
    fi
else
    fail ".env file not found (copy from .env.example)"
fi

# 5. Check docker-compose.yml
echo ""
echo "5. Checking Docker Compose Configuration..."
if [ -f docker-compose.yml ]; then
    pass "docker-compose.yml exists"
    if docker-compose config &> /dev/null; then
        pass "docker-compose.yml is valid"
    else
        fail "docker-compose.yml validation failed"
    fi
else
    fail "docker-compose.yml not found"
fi

# 6. Check required files
echo ""
echo "6. Checking Project Files..."
REQUIRED_FILES=("main.py" "requirements.txt" "Dockerfile")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        pass "$file exists"
    else
        fail "$file missing"
    fi
done

# 7. Check asset directories
echo ""
echo "7. Checking Asset Directories..."
ASSET_DIRS=("app/assets" "app/assets/fonts" "app/assets/anchors" "app/encoder")
for dir in "${ASSET_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        pass "$dir exists"
    else
        fail "$dir missing"
    fi
done

# 8. Check asset files
echo ""
echo "8. Checking Asset Files..."
if [ -f "app/assets/fonts/NotoSansDevanagari-Bold.ttf" ]; then
    pass "Devanagari font found"
else
    warn "Devanagari font not found (will be needed for text rendering)"
fi

if [ -f "app/assets/anchors/male.png" ]; then
    pass "Male anchor image found"
else
    warn "Male anchor image not found"
fi

if [ -f "app/assets/anchors/female.png" ]; then
    pass "Female anchor image found"
else
    warn "Female anchor image not found"
fi

# 9. Check system resources
echo ""
echo "9. Checking System Resources..."
if command -v free &> /dev/null; then
    RAM=$(free -h | awk '/^Mem:/ {print $2}')
    pass "Available RAM: $RAM"
fi

if command -v df &> /dev/null; then
    DISK=$(df -h / | awk 'NR==2 {print $4}')
    pass "Available Disk: $DISK"
fi

# 10. Check Python (optional)
echo ""
echo "10. Checking Python (Optional)..."
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version)
    pass "Python available: $PY_VERSION"
else
    warn "Python3 not found (not needed if using Docker)"
fi

# 11. Check network connectivity
echo ""
echo "11. Checking Network Connectivity..."
if ping -c 1 8.8.8.8 &> /dev/null; then
    pass "Internet connection available"
else
    fail "No internet connection (needed for YouTube streaming)"
fi

# 12. Check ports
echo ""
echo "12. Checking Port Availability..."
if command -v lsof &> /dev/null; then
    if ! lsof -i :8000 &> /dev/null; then
        pass "Port 8000 is available"
    else
        fail "Port 8000 is already in use"
    fi
else
    warn "Cannot check port availability (install lsof)"
fi

# Summary
echo ""
echo "=================================="
echo "Summary:"
echo "Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo "Failed: ${RED}$CHECKS_FAILED${NC}"
echo "Warnings: ${YELLOW}$CHECKS_WARNING${NC}"
echo "=================================="
echo ""

# Final verdict
if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ System is ready for deployment!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Generate a test video:"
    echo "   docker-compose up -d"
    echo "   curl -X POST http://localhost:8000/generate-news \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"headline\": \"परीक्षण\", \"content\": \"परीक्षण\", \"category\": \"परीक्षण\", \"breaking\": false}'"
    echo ""
    echo "2. Start streaming:"
    echo "   curl -X POST http://localhost:8000/start-stream"
    echo ""
    echo "3. Check API docs:"
    echo "   http://localhost:8000/docs"
    exit 0
else
    echo -e "${RED}✗ System is not ready. Fix the errors above and run again.${NC}"
    exit 1
fi