#!/bin/bash

# Git Commit Helper - Stage and commit all CI/CD files

echo "📦 Staging CI/CD files..."
echo ""

# Stage all new files
git add .github/
git add .gitignore
git add pytest.ini
git add Makefile
git add Dockerfile
git add docker-compose.yml
git add *.sh
git add *.bat
git add README.md
git add SETUP_SUMMARY.md
git add CI_README.md
git add utils/driver_setup.py

echo "✓ Files staged"
echo ""

# Show what will be committed
echo "Files to be committed:"
git status --short

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ready to commit with message:"
echo "  'Add CI/CD automation setup with GitHub Actions'"
echo ""
echo "Run the following commands:"
echo "  git commit -m 'Add CI/CD automation setup with GitHub Actions'"
echo "  git push origin main"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
