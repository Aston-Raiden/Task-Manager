# Save this as fix_venv.ps1, then run as Administrator

# Delete existing venv
if (Test-Path "venv") {
    Remove-Item -Path "venv" -Recurse -Force
}

# Get Python path
$pythonPath = (Get-Command python).Source
Write-Host "Using Python from: $pythonPath"

# Create venv
& $pythonPath -m venv venv

# Fix permissions
$venvScripts = "venv\Scripts"
if (Test-Path $venvScripts) {
    Get-ChildItem -Path $venvScripts | ForEach-Object {
        icacls $_.FullName /grant:r "$env:USERNAME:(F)" /inheritance:r
    }
}

Write-Host "Virtual environment created successfully!"
Write-Host "To activate: venv\Scripts\Activate.ps1"