$sourceFile = "\\server\Magnum Opus\NFT\Bambi Cloud Podcast NFT v1.0\1.wmv"
$destinationFolder = (Get-Item $sourceFile).DirectoryName

$numberOfCopies = 42

for ($i = 2; $i -le $numberOfCopies; $i++) {
    $destFile = Join-Path $destinationFolder "$i.wmv"
    Copy-Item $sourceFile $destFile
    Write-Host "Copied $sourceFile to $destFile"
}

Write-Host "All copies completed."
