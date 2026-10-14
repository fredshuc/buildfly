$ErrorActionPreference = 'Stop'
$meta = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'SHA256.json') -Raw | ConvertFrom-Json
$destination = Join-Path $PSScriptRoot $meta.original_name
if (Test-Path -LiteralPath $destination) { throw 'Output ZIP already exists. Move it elsewhere before joining.' }
foreach ($part in $meta.parts) {
    $partPath = Join-Path $PSScriptRoot $part.name
    if ((Get-Item -LiteralPath $partPath).Length -ne $part.bytes) { throw "Incorrect size: $($part.name)" }
    if ((Get-FileHash -LiteralPath $partPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $part.sha256) { throw "Incorrect hash: $($part.name)" }
}
$outputStream = [System.IO.File]::Open($destination, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
try {
    foreach ($part in $meta.parts) {
        $inputStream = [System.IO.File]::OpenRead((Join-Path $PSScriptRoot $part.name))
        try { $inputStream.CopyTo($outputStream) } finally { $inputStream.Dispose() }
    }
} finally { $outputStream.Dispose() }
if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $meta.original_sha256) { throw 'Reassembled ZIP hash mismatch.' }
Write-Output "Verified ZIP ready: $destination"
