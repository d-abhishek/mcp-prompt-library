# Clean previous build
Write-Host "Cleaning build directory..." -ForegroundColor Cyan
Remove-Item -Recurse -Force .\build\* -ErrorAction SilentlyContinue

# Install dependencies
Write-Host "Installing dependencies for ARM64 Linux..." -ForegroundColor Cyan
python -m pip install -r .\server\requirements.txt --target build/ --platform manylinux2014_aarch64 --only-binary=:all:

# Copy application code (flat structure - all .py files at root)
Write-Host "Copying application code..." -ForegroundColor Cyan
Copy-Item -Force .\server\server.py .\build\
Copy-Item -Force .\server\prompt_handlers.py .\build\
Copy-Item -Force .\server\prompt_tools.py .\build\
Copy-Item -Force .\server\tools.py .\build\

# Copy lambda handler
Write-Host "Copying lambda handler..." -ForegroundColor Cyan
Copy-Item -Force .\lambda-handler.py .\build\

# Copy prompts
Write-Host "Copying prompts..." -ForegroundColor Cyan
Copy-Item -Recurse -Force .\prompts .\build\prompts

# Copy data
Write-Host "Copying data..." -ForegroundColor Cyan
Copy-Item -Recurse -Force .\data .\build\data

# Create dist directory
Write-Host "Creating distribution package..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path .\server\dist | Out-Null

# Create ZIP
Compress-Archive -Path .\build\* -DestinationPath .\server\dist\lambda-handler.zip -Force

# Show results
Write-Host "`nBuild complete!" -ForegroundColor Green
$zipFile = Get-Item .\server\dist\lambda-handler.zip
Write-Host "ZIP Location: $($zipFile.FullName)" -ForegroundColor Yellow
Write-Host "ZIP Size: $([math]::Round($zipFile.Length / 1MB, 2)) MB" -ForegroundColor Yellow

if ($zipFile.Length -gt 50MB) {
    Write-Host "`nWARNING: ZIP is larger than 50 MB. You may need to use Lambda Layers or Container Images." -ForegroundColor Red
}