[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param([Parameter(Mandatory)][string]$CsvPath, [switch]$Apply, [SecureString]$InitialPassword)
$ErrorActionPreference = 'Stop'
$rows = @(Import-Csv -LiteralPath $CsvPath)
if ($rows.Count -eq 0 -or $rows.Count -gt 100) { throw 'CSV must contain 1–100 users.' }
$seen = @{}
foreach ($row in $rows) {
    if ($row.SamAccountName -notmatch '^[A-Za-z][A-Za-z0-9._-]{0,19}$') { throw "Invalid account name: $($row.SamAccountName)" }
    $key = $row.SamAccountName.ToLowerInvariant()
    if ($seen.ContainsKey($key)) { throw "Duplicate account: $key" }
    $seen[$key] = $true
    if ([string]::IsNullOrWhiteSpace($row.DisplayName) -or $row.UserPrincipalName -notmatch '^[^\s@]+@[^\s@]+$' -or [string]::IsNullOrWhiteSpace($row.OU)) { throw 'DisplayName, UserPrincipalName and OU are required.' }
}
if (-not $Apply) {
    $rows | Select-Object SamAccountName, DisplayName, UserPrincipalName, OU, @{Name='Action';Expression={'Proposed create (not applied)'}}
    return
}
if (-not $InitialPassword) { throw 'Supply InitialPassword as a SecureString when using Apply.' }
Import-Module ActiveDirectory
foreach ($ou in ($rows.OU | Select-Object -Unique)) { $null = Get-ADOrganizationalUnit -Identity $ou }
foreach ($row in $rows) {
    $existing = $null
    try { $existing = Get-ADUser -Identity $row.SamAccountName } catch [Microsoft.ActiveDirectory.Management.ADIdentityNotFoundException] { }
    if ($existing) { Write-Warning "Skipping existing account: $($row.SamAccountName)"; continue }
    if ($PSCmdlet.ShouldProcess($row.UserPrincipalName, 'Create AD user')) {
        New-ADUser -Name $row.DisplayName -DisplayName $row.DisplayName -SamAccountName $row.SamAccountName -UserPrincipalName $row.UserPrincipalName -Path $row.OU -AccountPassword $InitialPassword -ChangePasswordAtLogon $true -Enabled $true
    }
}
