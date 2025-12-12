# Running GitHub Actions Locally with Act

This guide shows you how to use `act` to run GitHub Actions workflows locally without pushing to GitHub.

> ⚠️ **Important: This is an Optional Feature**
> 
> This documentation is **completely optional** and is intended for:
> - **Project maintainers** who want to test documentation deployment workflows locally
> - **Contributors** who are working on documentation or CI/CD improvements
> 
> **Core LeetCode practice functionality does NOT require this:**
> - ✅ Solving problems (`solutions/`, `generators/`)
> - ✅ Running tests (`run_tests.bat/sh`, `run_case.bat/sh`)
> - ✅ Using the runner framework (`runner/`)
> - ✅ All core practice features work without any CI/CD setup
> 
> **This CI/CD setup is ONLY for:**
> - 📚 Documentation website deployment (MkDocs + GitHub Pages)
> - 🧠 Mind map generation and hosting
> - 🔧 Development convenience for maintainers
> 
> **For open-source users:** You can completely ignore this guide and use the project normally for LeetCode practice. The CI/CD setup is only relevant if you want to contribute to documentation or deploy your own documentation site.

---

## ⚡ Quick Start

**Prerequisites:**
1. Docker (required)
2. act tool (required)

**Quick install act:**
- **Windows**: `winget install nektos.act` or [download manually](https://github.com/nektos/act/releases/latest)
- **macOS**: `brew install act`
- **Linux**: `curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash`

**Then run:**
```bash
# Navigate to your project root directory
cd /path/to/your/project

# List all workflows
act -l

# Run a specific job
act -j build

# Or specify workflow file explicitly
act -W .github/workflows/deploy-pages.yml -j build
```

---

## 📋 Table of Contents

- [What is Act?](#what-is-act)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Running Project Workflows](#running-project-workflows)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting) (See Appendix)
- [Limitations](#limitations)

---

## What is Act?

`act` is an open-source tool that lets you run GitHub Actions workflows locally on your machine without pushing to GitHub. This is useful for:

- ✅ Quickly testing workflow configurations
- ✅ Debugging CI/CD pipelines locally
- ✅ Saving GitHub Actions minutes
- ✅ Offline development and testing

---

## Installation

### Step 1: Install Docker

#### Windows

1. **Download Docker Desktop:**
   - Official site: https://www.docker.com/products/docker-desktop/
   - Or use winget: `winget install Docker.DockerDesktop`

2. **Install and start:**
   - Run the installer
   - Start Docker Desktop (you'll see a Docker icon in the system tray)

3. **Verify:**
   ```powershell
   docker --version
   docker ps
   ```

**Important for Windows:** Docker Desktop requires WSL 2. If you encounter issues, see [Windows-specific setup](#windows-wsl-setup) in the Troubleshooting section.

#### macOS

1. **Using Homebrew (recommended):**
   ```bash
   brew install --cask docker
   ```

2. **Or download manually:**
   - Official site: https://www.docker.com/products/docker-desktop/
   - Download the `.dmg` file and install

3. **Start and verify:**
   ```bash
   open -a Docker
   docker --version
   ```

#### Linux

1. **Using package manager:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   
   # Fedora/RHEL
   sudo dnf install docker docker-compose
   
   # Arch Linux
   sudo pacman -S docker docker-compose
   ```

2. **Start Docker service:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Add user to docker group (optional, to avoid sudo):**
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in for this to take effect
   ```

4. **Verify:**
   ```bash
   docker --version
   docker ps
   ```

---

### Step 2: Install act

> **💡 How to choose the right architecture?**
> 
> - **Windows**: Most modern computers are `x86_64` (64-bit)
> - **macOS**: Apple Silicon (M1/M2/M3) use `arm64`, Intel Macs use `x86_64`
> - **Linux**: Run `uname -m` to check architecture
>   - `x86_64` = 64-bit Intel/AMD
>   - `aarch64` or `arm64` = ARM 64-bit
>   - `armv7l` = ARM 32-bit
>   - `riscv64` = RISC-V 64-bit

#### Windows

**Method 1: Manual download (recommended)**

1. **Download act:**
   - Visit: https://github.com/nektos/act/releases/latest
   - Download the appropriate version for your architecture:
   
   | Architecture | File Name | Size | SHA256 |
   |-------------|-----------|------|--------|
   | x86_64 (64-bit) | `act_Windows_x86_64.zip` | 7.72 MB | `3e80345061ef4bfbb5a96da7a18f71578a0847b25a29ab0dc5f7e846ebb5a108` |
   | ARM64 | `act_Windows_arm64.zip` | 6.98 MB | `7b75ddf1fef53602091a08af0c7593250a4aa13478a9f43672443fdbb22b671e` |
   | ARMv7 | `act_Windows_armv7.zip` | 7.24 MB | `a44943c5017160cbefe2d5e3c19c82028e42e7efc647930d37b4c11890f1edb9` |
   | i386 (32-bit) | `act_Windows_i386.zip` | 7.45 MB | `3db1ac00dd564c06a6f5ef5ba73305efdf08ad39fed58b01528bb48a9b5adfcb` |

2. **Extract:**
   - Extract to any directory, e.g., `C:\Tools\act`
   - Or extract to user directory: `C:\Users\YourUsername\AppData\Local\act`

3. **Add to PATH:**
   
   **Option A: Using Environment Variables window (GUI)**
   
   1. Press `Win + R`, type `sysdm.cpl`, press Enter
   2. Click "Advanced" tab → "Environment Variables"
   3. Under "User variables", select `Path` → Click "Edit"
   4. Click "New", enter the act directory path (e.g., `C:\Tools\act`)
   5. Click "OK" to save all windows
   6. **Restart PowerShell or terminal** (important!)
   
   **Option B: Using PowerShell (temporary, current session only)**
   
   ```powershell
   $env:Path += ";C:\Tools\act"
   ```
   
   **Option C: Using PowerShell (permanent)**
   
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\act", "User")
   # Restart PowerShell for this to take effect
   ```

4. **Verify installation:**
   ```powershell
   # After restarting PowerShell
   act --version
   ```

**Quick install (PowerShell one-liner, x86_64):**

```powershell
$url = "https://github.com/nektos/act/releases/latest/download/act_Windows_x86_64.zip"
$output = "$env:TEMP\act.zip"
$installDir = "$env:LOCALAPPDATA\act"
Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
Expand-Archive -Path $output -DestinationPath $installDir -Force
$env:Path += ";$installDir"
# Optional: Add permanently
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$installDir", "User")
```

**Method 2: Using package managers**

```powershell
# winget
winget install nektos.act

# Chocolatey
choco install act-cli

# Scoop
scoop install act
```

#### macOS

**Method 1: Using Homebrew (recommended)**

```bash
brew install act
```

**Method 2: Manual download**

1. Visit: https://github.com/nektos/act/releases/latest
2. Download based on your processor:
   - **Apple Silicon (M1/M2/M3)**: `act_Darwin_arm64.tar.gz` (7.18 MB)
     - SHA256: `028d9705b9ce97e83e2b451622734e517b54240a6b0c6682c205e3da332dee56`
   - **Intel Mac**: `act_Darwin_x86_64.tar.gz` (7.64 MB)
     - SHA256: `62009dced61db01033e7e18c00704143eaa0b76d5f17f0c7e9d9d4c250a9068d`
3. Extract and install:
   ```bash
   tar -xzf act_Darwin_*.tar.gz
   sudo mv act /usr/local/bin/
   chmod +x /usr/local/bin/act
   ```

**Verify:**
```bash
act --version
```

#### Linux

**Method 1: Using official install script (recommended)**

```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

**Method 2: Using package managers**

```bash
# Arch Linux (AUR)
yay -S act-bin

# Nix
nix-env -iA nixpkgs.act

# Snap
sudo snap install act
```

**Method 3: Manual download**

1. Visit: https://github.com/nektos/act/releases/latest
2. Download based on architecture:
   
   | Architecture | File Name | Size | SHA256 |
   |-------------|-----------|------|--------|
   | x86_64 (64-bit) | `act_Linux_x86_64.tar.gz` | 7.51 MB | `ed37d29fc117b3075cf586bb9323ec6c16320a5a3c5c0df9f1859d271d303f0d` |
   | ARM64 | `act_Linux_arm64.tar.gz` | 6.9 MB | `30d9347a7ee8b91f33c25137387c52326c6092f14bc31a241fa0fe94e64accc5` |
   | ARMv7 | `act_Linux_armv7.tar.gz` | 7.09 MB | `f25ab2e2285ad049b285465e82c76549839e7729f43cda6a317e70b48cbf387f` |
   | ARMv6 | `act_Linux_armv6.tar.gz` | 7.1 MB | `8e0b2f72722e7ef9830e2b59d6ab30c9cb2fccc9901687ea6a499589b1a81319` |
   | i386 (32-bit) | `act_Linux_i386.tar.gz` | 7.15 MB | `0f1b3f9b41c8a37310925fb162a1234fbfdc465a3302eb2bfc3de63657fa28dd` |
   | RISC-V 64 | `act_Linux_riscv64.tar.gz` | 7.08 MB | `67dfb6cd5759eeb4faf65701b356446206ea38d42de0a9bd4a65e5bc9b512ad4` |

3. Extract and install:
   ```bash
   tar -xzf act_Linux_*.tar.gz
   sudo mv act /usr/local/bin/
   chmod +x /usr/local/bin/act
   ```

**Verify:**
```bash
act --version
```

---

### Verify Installation

After installation, confirm both tools are available:

```bash
# Windows (PowerShell)
docker --version
act --version

# macOS/Linux
docker --version
act --version
```

Both commands should display version numbers, indicating successful installation.

---

## Basic Usage

### List All Workflows

⚠️ **Important:** Must run from project root directory, or specify workflow path explicitly.

```bash
# Method 1: Run from project root directory (recommended)
cd /path/to/your/project
act -l

# Method 2: Specify workflow file explicitly
act -W .github/workflows/deploy-pages.yml -l
```

Example output:
```
Workflow: .github/workflows/deploy-pages.yml
  build    Build documentation
  deploy   Deploy to GitHub Pages
```

### Run a Specific Job

```bash
# Run build job
act -j build

# Specify workflow file
act -W .github/workflows/deploy-pages.yml -j build
```

### Use Recommended Platform Image

For better compatibility and speed, use the recommended image:

```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -j build
```

### Show Verbose Output

```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -v -j build
```

### Manually Trigger Workflow

```bash
# Trigger workflow_dispatch event
act workflow_dispatch -W .github/workflows/deploy-pages.yml

# Simulate push event
act push -W .github/workflows/deploy-pages.yml
```

---

## Running Project Workflows

### Current Project Workflow

> **Note:** This workflow is **optional** and only used for documentation deployment. It does NOT affect core LeetCode practice functionality.

This project contains a documentation deployment workflow: `.github/workflows/deploy-pages.yml`

**Purpose:** This workflow is designed for maintaining and deploying the project's documentation website (MkDocs + GitHub Pages). It is **not required** for:
- Writing or testing LeetCode solutions
- Using the runner framework
- Running local tests
- Any core practice features

The workflow contains two jobs:
- `build`: Build MkDocs documentation site
- `deploy`: Deploy to GitHub Pages

**When to use this:**
- You're a maintainer testing documentation changes locally
- You're contributing to documentation or CI/CD improvements
- You want to deploy your own documentation site

**When you can ignore this:**
- You're just practicing LeetCode problems
- You're using the project for algorithm learning
- You don't need to deploy documentation

### Test Build Job

Since the `deploy` job requires GitHub Pages environment, it's recommended to test the `build` job first:

```bash
# Basic execution
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -j build

# Verbose output
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -v -j build

# Debug mode
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -v --debug -j build
```

### Expected Execution Steps

1. ✅ Checkout code
2. ✅ Setup Python 3.11
3. ✅ Install dependencies
4. ✅ Generate Mind Maps (Markdown + HTML)
5. ✅ Build MkDocs site
6. ✅ Copy mind map HTML files
7. ✅ Setup Pages
8. ✅ Upload artifact

### Success Indicators

When you see the following output, act is running successfully:

```
time="..." level=info msg="Using docker host 'npipe:////./pipe/docker_engine'"
[Deploy Documentation/build] ⭐ Run Set up job
[Deploy Documentation/build] 🚀  Start image=catthehacker/ubuntu:act-latest
[Deploy Documentation/build]   🐳  docker pull image=catthehacker/ubuntu:act-latest
```

**What this means:**
- ✅ Docker connection successful
- ✅ Workflow started executing
- ✅ Pulling Docker image (first run may take a few minutes)

---

## Common Commands

### Quick Test Commands

```bash
# One-command test build job (recommended)
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -j build -v

# List all workflows
act -l

# Run all jobs in a specific workflow
act -W .github/workflows/deploy-pages.yml

# Simulate push to main branch
act push -W .github/workflows/deploy-pages.yml
```

### Advanced Options

```bash
# Use secrets file
act --secret-file .secrets

# Use environment variables file
act -e .env

# Bind ports (if needed)
act --container-options "-p 8000:8000"

# Dry run (don't actually execute)
act -n
```

---

## Limitations

⚠️ **Note:** `act` cannot fully simulate all GitHub Actions features:

- ❌ GitHub Secrets (need to provide manually using `--secret-file`)
- ❌ GitHub API calls
- ❌ Some special Actions (e.g., `actions/deploy-pages@v4`)
- ❌ Environment variables may need manual setup
- ❌ Some permission-related features

✅ **Good for testing:**
- Build processes
- Test execution
- Code checks
- Basic CI workflows

---

## Troubleshooting

See [Troubleshooting Appendix](#troubleshooting-appendix) for detailed error resolution.

Common issues:
- Docker Desktop won't start
- act command not found
- Workflow path not found
- Docker connection errors

---

## Reference Resources

- [Act Official Documentation](https://github.com/nektos/act)
- [Act GitHub Repository](https://github.com/nektos/act)
- [Docker Desktop Documentation](https://docs.docker.com/desktop/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Troubleshooting Appendix

### Docker Desktop Won't Start

**Error:** `Error response from daemon: Docker Desktop is unable to start`, `failed to list containers: EOF`, or `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`

**Solutions (try in order):**

1. **Start Docker Desktop application:**
   - Find "Docker Desktop" from Start menu
   - Click to start, wait for Docker to fully start (system tray icon stops spinning)
   - Confirm Docker icon (whale icon) appears in system tray

2. **Check Docker Desktop status:**
   ```powershell
   Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
   ```

3. **Check WSL 2 (Windows required):**
   ```powershell
   wsl --status
   wsl --list --verbose
   # ⚠️ Important: Must have at least one distribution!
   
   # If no distributions, install one:
   wsl --install -d Ubuntu
   ```

4. **Restart Docker Desktop:**
   - Right-click Docker icon in system tray
   - Select "Quit Docker Desktop"
   - Wait a few seconds, then restart Docker Desktop

5. **Check Docker Desktop settings:**
   - Open Docker Desktop
   - Settings → General
   - Confirm "Use WSL 2 based engine" is checked (Windows)
   - Settings → Resources → WSL Integration
   - Confirm your WSL distribution is enabled

**Windows WSL Setup:**

If you see `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`, the most common cause is **no WSL 2 distribution installed**.

**Solution:**
```powershell
# Install Ubuntu WSL 2 distribution
wsl --install -d Ubuntu

# Verify installation
wsl --list --verbose
# Should show:
#   NAME      STATE           VERSION
# * Ubuntu    Running         2

# Restart Docker Desktop
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 5
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -Verb RunAs

# Wait for Docker to fully start (1-2 minutes)
# Then verify
docker ps
```

### Act Command Not Found

**Error:** `CommandNotFoundException` or `'act' is not recognized`

**Solutions:**

1. **Confirm act is installed:**
   ```powershell
   Test-Path "C:\Tools\act\act.exe"
   ```

2. **Check PATH environment variable:**
   ```powershell
   $env:Path -split ';' | Select-String -Pattern 'act'
   ```

3. **Add to PATH:**
   - Use Environment Variables window (see Installation section)
   - Or use PowerShell:
     ```powershell
     # Temporary (current session)
     $env:Path += ";C:\Tools\act"
     
     # Permanent (requires PowerShell restart)
     [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\act", "User")
     ```

4. **Restart PowerShell/terminal**

5. **Use full path (temporary solution):**
   ```powershell
   C:\Tools\act\act.exe --version
   ```

### Workflow Path Not Found

**Error:** `Error: CreateFile C:\Users\Username\.github\workflows: The system cannot find the path specified`

**Cause:** act defaults to looking for workflows in user home directory, not project directory.

**Solutions:**

1. **Ensure you're in project root directory:**
   ```powershell
   cd C:\Developer\program\python\neetcode
   act -l
   ```

2. **Specify workflow file explicitly:**
   ```bash
   act -W .github/workflows/deploy-pages.yml -l
   ```

3. **Use absolute path:**
   ```powershell
   act -W C:\Developer\program\python\neetcode\.github\workflows\deploy-pages.yml -l
   ```

### Docker Connection Error

**Error:** `error during connect: in the default daemon configuration on Windows, the docker client must be run with elevated privileges to connect` or `open //./pipe/docker_engine: The system cannot find the file specified`

**Cause:** Docker Desktop not started or WSL backend not running.

**Solutions:**

1. **Confirm Docker Desktop is running:**
   ```powershell
   Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
   ```

2. **Start Docker Desktop:**
   ```powershell
   Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -Verb RunAs
   ```

3. **Wait for Docker to fully start:**
   - Wait 1-2 minutes
   - Confirm Docker icon in system tray stops spinning
   - Confirm Docker Desktop window shows "Docker Desktop is running"

4. **Confirm WSL integration is enabled:**
   - Open Docker Desktop
   - Settings → Resources → WSL Integration
   - Confirm "Enable integration with my default WSL distro" is checked
   - Confirm "Ubuntu" integration is enabled
   - If not enabled, check and click "Apply & Restart"

5. **Verify Docker connection:**
   ```powershell
   Test-Path "\\.\pipe\dockerDesktopLinuxEngine"
   # Should return True
   
   docker ps
   # Should execute normally
   ```

6. **Run PowerShell as administrator:**
   - Close current PowerShell
   - Right-click PowerShell shortcut
   - Select "Run as administrator"
   - Re-run act command

### Debugging Tips

**Enter container for debugging:**
```bash
act -j build --container-options "--entrypoint /bin/bash"
```

**Run to specific step:**
```bash
act -j build --step "Setup Python"
```

**View container logs:**
```bash
docker ps -a
docker logs <container_id>
```

**Clean up act containers:**
```bash
# macOS / Linux
docker ps -a | grep "act-" | awk '{print $1}' | xargs docker rm -f

# Windows (PowerShell)
docker ps -a | Select-String "act-" | ForEach-Object { docker rm -f $_.Split()[0] }
```

---

## Changelog

- **2025-12-12**: Complete cross-platform version
  - ✅ Added Windows, macOS, Linux installation guides
  - ✅ Included Docker installation instructions for all platforms
  - ✅ Provided multiple installation methods (package managers, manual download)
  - ✅ Updated all command examples to cross-platform format
  - ✅ Added cross-platform troubleshooting and solutions
  - ✅ Recorded actual environment information and testing process
