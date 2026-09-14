# Fallback setup: OpenSSH from GitHub ZIP (no Windows Update) + Tailscale
# Run in an ELEVATED PowerShell window.

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = 3072

function Step($m) { Write-Host "[*] $m" -ForegroundColor Cyan }
function Good($m) { Write-Host "[+] $m" -ForegroundColor Green }
function Bad ($m) { Write-Host "[!] $m" -ForegroundColor Red }

$id = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $id.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Bad 'NOT ELEVATED. Press Win+X, choose "Windows PowerShell (Admin)", run again.'
    return
}
Good "Elevated OK. Host=$(hostname) Date=$(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# --- 1. OpenSSH Server from GitHub ZIP ---------------------------------------
if (Get-Service sshd -ErrorAction SilentlyContinue) {
    Good 'sshd service already present, skipping install'
} else {
    $dst = Join-Path $env:ProgramFiles 'OpenSSH'
    $zip = Join-Path $env:TEMP 'OpenSSH-Win64.zip'
    $tmp = Join-Path $env:TEMP 'OpenSSH-extract'

    Step 'Downloading OpenSSH-Win64.zip from GitHub (about 5 MB)'
    Invoke-WebRequest 'https://github.com/PowerShell/Win32-OpenSSH/releases/latest/download/OpenSSH-Win64.zip' `
        -OutFile $zip -UseBasicParsing

    Step 'Extracting'
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    Expand-Archive -LiteralPath $zip -DestinationPath $tmp -Force
    $src = (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName
    if (-not $src) { $src = $tmp }

    if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Path $dst -Force | Out-Null }
    Copy-Item -Path (Join-Path $src '*') -Destination $dst -Recurse -Force
    Good "Files in $dst"

    Step 'Registering sshd service'
    & powershell.exe -ExecutionPolicy Bypass -File (Join-Path $dst 'install-sshd.ps1')
}

Step 'Starting sshd'
Set-Service sshd -StartupType Automatic
Start-Service sshd
Good "sshd: $((Get-Service sshd).Status)"

# --- 2. Authorized key -------------------------------------------------------
Step 'Installing authorized key'
$key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBEOshy4GAA58Vw1Z/NfxfJeLVNp2rX0j4rKJLEDqLmN claudia@win-cveqto2is7r'
$sshDir = Join-Path $env:ProgramData 'ssh'
if (-not (Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }
$akf = Join-Path $sshDir 'administrators_authorized_keys'

$lines = @()
if (Test-Path $akf) {
    $lines = @(Get-Content -LiteralPath $akf -ErrorAction SilentlyContinue | Where-Object { $_.Trim() -ne '' })
}
if ($lines -notcontains $key) { $lines += $key }
[IO.File]::WriteAllLines($akf, $lines, (New-Object Text.ASCIIEncoding))

$adm = (New-Object Security.Principal.SecurityIdentifier 'S-1-5-32-544').Translate([Security.Principal.NTAccount]).Value
$sys = (New-Object Security.Principal.SecurityIdentifier 'S-1-5-18').Translate([Security.Principal.NTAccount]).Value
icacls $akf /inheritance:r /grant "${adm}:F" /grant "${sys}:F" | Out-Null
Good "Key file ready: $akf ($($lines.Count) key(s))"

# --- 3. Default shell --------------------------------------------------------
if (-not (Test-Path 'HKLM:\SOFTWARE\OpenSSH')) { New-Item -Path 'HKLM:\SOFTWARE\OpenSSH' -Force | Out-Null }
New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell -PropertyType String -Force `
    -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' | Out-Null

# --- 4. Firewall -------------------------------------------------------------
if (-not (Get-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue)) {
    Step 'Adding firewall rule for port 22'
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' `
        -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
}
Restart-Service sshd
Good "sshd restarted: $((Get-Service sshd).Status)"

# --- 5. Tailscale ------------------------------------------------------------
$ts = Join-Path $env:ProgramFiles 'Tailscale\tailscale.exe'
if (-not (Test-Path $ts)) {
    Step 'Downloading Tailscale MSI (about 37 MB)'
    $msi = Join-Path $env:TEMP 'tailscale-setup.msi'
    Invoke-WebRequest 'https://pkgs.tailscale.com/stable/tailscale-setup-latest-amd64.msi' -OutFile $msi -UseBasicParsing
    Step 'Installing Tailscale'
    $p = Start-Process msiexec.exe -ArgumentList "/i `"$msi`" /quiet /norestart" -Wait -PassThru
    if ($p.ExitCode -ne 0) { Bad "msiexec exit code $($p.ExitCode)" }
}
if (-not (Test-Path $ts)) { Bad 'Tailscale not installed - stopping here'; return }

for ($i = 0; $i -lt 30 -and -not (Get-Service Tailscale -ErrorAction SilentlyContinue); $i++) { Start-Sleep 1 }
Step 'Connecting to Tailscale (a browser login page may open)'
& $ts up --unattended

# --- 6. Summary --------------------------------------------------------------
Write-Host ''
Write-Host '================ RESULT ================' -ForegroundColor Yellow
"hostname   : $(hostname)"
"user       : $(whoami)"
"sshd       : $((Get-Service sshd).Status) / $((Get-Service sshd).StartType)"
"tailscale  : $(& $ts ip -4 2>&1)"
Write-Host '========================================' -ForegroundColor Yellow
