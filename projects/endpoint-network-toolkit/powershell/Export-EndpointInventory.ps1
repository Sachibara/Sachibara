[CmdletBinding()]
param([string]$OutputPath = '.\endpoint-inventory.json')
$ErrorActionPreference = 'Stop'
$os = Get-CimInstance Win32_OperatingSystem
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($env:SystemDrive)'"
if (-not $disk -or $disk.Size -le 0) { throw 'Unable to read system disk.' }
$profiles = @(Get-NetFirewallProfile)
if ($profiles.Count -eq 0) { throw 'Unable to read firewall profiles.' }
$row = [ordered]@{
    name = $env:COMPUTERNAME
    os = $os.Caption
    disk_free_percent = [math]::Round(100 * $disk.FreeSpace / $disk.Size, 1)
    firewall_enabled = (@($profiles | Where-Object { -not $_.Enabled }).Count -eq 0)
    observed_at = [DateTime]::UtcNow.ToString('o')
}
ConvertTo-Json -InputObject @($row) -Depth 4 | Set-Content -LiteralPath $OutputPath -Encoding utf8
Write-Output "Inventory written to $OutputPath. No system settings changed."
