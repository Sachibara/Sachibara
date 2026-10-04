[CmdletBinding()]
param([string]$OutputPath='.\intune-devices.json')
$ErrorActionPreference='Stop'
Import-Module Microsoft.Graph.DeviceManagement
if (-not (Get-MgContext)) { throw 'Connect-MgGraph with DeviceManagementManagedDevices.Read.All before running this report.' }
$devices = @(Get-MgDeviceManagementManagedDevice -All | Select-Object Id, DeviceName, OperatingSystem, OsVersion, ComplianceState, LastSyncDateTime)
ConvertTo-Json -InputObject $devices -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding utf8
Write-Output "Exported $($devices.Count) Intune devices. No configuration was changed."
