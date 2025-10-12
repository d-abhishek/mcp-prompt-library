# PowerShell script to build stateless Python Lambda for MCP Streamable HTTP

Write-Host "Building Stateless Python Lambda for MCP Streamable HTTP..." -ForegroundColor Green

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

# Copy Python Lambda handler
Write-Host "Copying stateless Python Lambda handler..." -ForegroundColor Blue
Copy-Item "stateless_lambda.py" -Destination $BuildDir

# Create minimal requirements for stateless operation
Write-Host "Installing minimal Python dependencies for ARM64 Linux..." -ForegroundColor Blue
$Requirements = "minimal-requirements.txt"

# Only essential dependencies for stateless operation (no FastMCP, no SSE)
@"
python-frontmatter>=1.1.0
jinja2>=3.1.0
MarkupSafe>=2.0
PyYAML>=6.0
"@ | Out-File -FilePath $Requirements -Encoding UTF8

# Install Python packages for ARM64 Linux
pip install -r $Requirements --platform manylinux2014_aarch64 --only-binary=:all: --target "$BuildDir" --no-deps

# Remove temp requirements
Remove-Item $Requirements

# Copy prompts and data
Write-Host "Copying prompts and data..." -ForegroundColor Blue
if (Test-Path "prompts") {
    Copy-Item -Recurse "prompts" -Destination $BuildDir
}
if (Test-Path "data") {
    Copy-Item -Recurse "data" -Destination $BuildDir
}

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
Write-Host "Architecture: Stateless Python Lambda (MCP Streamable HTTP)" -ForegroundColor Magenta