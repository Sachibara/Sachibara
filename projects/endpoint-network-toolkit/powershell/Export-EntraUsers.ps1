[CmdletBinding()]
param([string]$OutputPath='.\entra-users.json')
$ErrorActionPreference='Stop'
Import-Module Microsoft.Graph.Users
if (-not (Get-MgContext)) { throw 'Connect-MgGraph with User.Read.All before running this report.' }
$users = @(Get-MgUser -All -Property Id,DisplayName,UserPrincipalName,AccountEnabled | Select-Object Id,DisplayName,UserPrincipalName,AccountEnabled)
ConvertTo-Json -InputObject $users -Depth 4 | Set-Content -LiteralPath $OutputPath -Encoding utf8
Write-Output "Exported $($users.Count) users. No account was changed."
