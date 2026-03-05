# GitHub Setup & Push Instructions

Your local git repository is ready! Follow these steps to upload to GitHub.

## Step 1: Create a Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `network-anomaly-detector`
3. Add description: `Cross-platform network anomaly detector with pure Python implementation for Windows (no external tools required) and advanced packet analysis for Linux/macOS.`
4. Choose **Public** (or Private if you prefer)
5. ✅ Do NOT initialize with README/gitignore (we already have them)
6. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Here are the exact commands to run:

### Replace `YOUR_USERNAME` with your GitHub Username

```bash
cd /home/zakaria/Coding/Networking

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/network-anomaly-detector.git

# Rename branch to main (matches GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main

# Verify
git remote -v
```

### Example with actual username:
```bash
git remote add origin https://github.com/zakaria/network-anomaly-detector.git
git branch -M main
git push -u origin main
```

## Step 3: Authentication

When pushing, GitHub may ask for authentication:

### Option A: Personal Access Token (Recommended)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`
4. Copy the token
5. When prompted for password, paste the token

### Option B: SSH Key (Advanced)
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: https://github.com/settings/ssh/new
3. Use SSH URL: `git@github.com:YOUR_USERNAME/network-anomaly-detector.git`

### Option C: GitHub CLI (Easiest)
```bash
# Install gh CLI
sudo apt install gh          # Linux
brew install gh             # macOS
choco install gh            # Windows

# Authenticate
gh auth login

# Create and push
gh repo create network-anomaly-detector --public --source=. --remote=origin --push
```

## Step 4: Verify Upload

After pushing, verify everything is on GitHub:

```bash
# Check remote
git remote -v

# Check branch
git branch

# View commit history
git log --oneline

# Quick verification
echo "✅ Ready! Check: https://github.com/YOUR_USERNAME/network-anomaly-detector"
```

## Common Commands Going Forward

### After making changes:
```bash
git add .
git commit -m "Your commit message"
git push
```

### View what will be pushed:
```bash
git status
git log --oneline -5
```

### Reset if something goes wrong:
```bash
git reset --hard HEAD~1  # Undo last commit (careful!)
git push --force-with-lease origin main  # Force push after reset
```

## Updating .gitignore

Your `.gitignore` is already set up to exclude:
- `__pycache__/`
- `*.pyc`
- `.venv/` and `venv/`
- `.pytest_cache/`
- `*.egg-info/`
- `dist/` and `build/`

This means the `venv/` folder won't be uploaded (good!).

## Add a License

To add MIT License to your repo:

```bash
cd /home/zakaria/Coding/Networking

# Create LICENSE file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Zakaria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Commit and push
git add LICENSE
git commit -m "Add MIT License"
git push
```

## Add GitHub Workflows (Optional)

Create automated testing when you push code.

**File**: `.github/workflows/tests.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - run: pip install -r requirements.txt
    - run: python -m pytest tests/
```

## Repository Settings to Configure

After pushing, visit your GitHub repo and:

1. **Settings** → **General**
   - Add description
   - Add homepage URL (optional)

2. **Settings** → **Social preview**
   - Add a project image (optional)

3. **About** section (right sidebar)
   - Add description
   - Add topics: `network-monitoring`, `anomaly-detection`, `python`, `cross-platform`

## GitHub Pages (Optional - Create a Website)

To create a project website:

1. **Settings** → **Pages**
2. Set source to `main` branch
3. Choose a theme
4. GitHub will generate a website at `https://YOUR_USERNAME.github.io/network-anomaly-detector`

## Making Your Repository Stand Out

### Add a Badge to README
```markdown
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-blue)
```

### Add to README
Your README already has great content! Consider adding:
- Installation badge
- GitHub link
- Contributing section
- Citation if needed

## Troubleshooting

### "Repository not found" error
- Verify GitHub username spelling
- Make sure you created the repo on GitHub first
- Check that authentication is working

### "Permission denied" error
- Use Personal Access Token instead of password
- Check SSH key is added to GitHub
- Try `git push -u origin main` (with `-u` flag)

### "fatal: A branch named 'master' cannot be created"
- Run: `git branch -M main` before pushing

### Already pushed to master, want to rename to main
```bash
git branch -m master main
git push -u origin main
git push origin --delete master
```

## Next Steps

1. ✅ Create GitHub repo
2. ✅ Push your code
3. ✅ Share the link!
4. 🔄 Keep updating with improvements
5. 📣 Announce on social media/forums
6. ⭐ Hope for stars!

## Quick One-Liner (if you have gh CLI installed)

```bash
cd /home/zakaria/Coding/Networking && \
gh repo create network-anomaly-detector \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Cross-platform network anomaly detector with pure Python implementation"
```

---

**Your repository is ready to push!** 🚀

Just follow the steps above to get it on GitHub. If you get stuck, let me know!
