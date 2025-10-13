# PowerShell script to build Simple Python Lambda with direct MCP integration

Write-Host "Building Simple Python Lambda with direct MCP integration..." -ForegroundColor Green

# Define paths
$BuildDir = "build"
$ZipPath = "mcp-prompt-library.zip"

# Clean previous build
if (Test-Path $BuildDir) {
    Write-Host "Cleaning previous build directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $BuildDir
}

if (Test-Path $ZipPath) {
    Write-Host "Removing previous ZIP file..." -ForegroundColor Yellow
    Remove-Item -Force $ZipPath
}

# Create build directory
Write-Host "Creating build directory..." -ForegroundColor Blue
New-Item -ItemType Directory -Path $BuildDir | Out-Null

# Copy Simple Python Lambda handler
Write-Host "Copying Simple Python Lambda handler..." -ForegroundColor Blue
Copy-Item "src\lambda_function.py" -Destination "$BuildDir\lambda_function.py"

# Copy Python server modules  
Write-Host "Copying Python MCP server modules..." -ForegroundColor Blue
Copy-Item -Recurse "server" -Destination $BuildDir

# Install only essential Python dependencies for ARM64 Linux
Write-Host "Installing essential Python dependencies for ARM64 Linux..." -ForegroundColor Blue

# Install minimal dependencies needed for our simplified approach
pip install --platform manylinux2014_aarch64 --only-binary=:all: --target $BuildDir --no-deps --upgrade `
    "python-frontmatter>=1.1.0" `
    "jinja2>=3.1.0" `
    "pyyaml>=6.0" `
    "MarkupSafe"

# Copy prompts and data
Write-Host "Copying prompts and data..." -ForegroundColor Blue
if (Test-Path "prompts") {
    Copy-Item -Recurse "prompts" -Destination $BuildDir
}
if (Test-Path "data") {
    Copy-Item -Recurse "data" -Destination $BuildDir
}

# Create __init__.py files to make server a proper Python package
New-Item -ItemType File -Path "$BuildDir\server\__init__.py" -Force | Out-Null

# Create the ZIP file
Write-Host "Creating deployment package..." -ForegroundColor Blue
Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipPath -Force

# Get ZIP size
$ZipSize = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)

# Clean up build directory
Write-Host "Cleaning up build directory..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $BuildDir

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "ZIP Location: $(Resolve-Path $ZipPath)" -ForegroundColor Cyan
Write-Host "ZIP Size: $ZipSize MB" -ForegroundColor Cyan
Write-Host ""
Write-Host "Architecture: Simple Python Lambda with direct MCP integration" -ForegroundColor Magenta
Write-Host "Handler: lambda_function.handler" -ForegroundColor Magenta
Write-Host "Runtime: Python 3.13 with minimal dependencies" -ForegroundColor Magenta