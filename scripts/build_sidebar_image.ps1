# Réduction lissée de l'image haute définition ; aucun traitement à l'exécution.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = Split-Path -Parent $PSScriptRoot
$folder = Join-Path $root 'gardavu\assets'
$source = [System.Drawing.Image]::FromFile((Join-Path $folder 'handcuffs-source.png'))
$canvas = [System.Drawing.Bitmap]::new(88, 66, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
try {
    $graphics.Clear([System.Drawing.Color]::Transparent)
    $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $scale = [Math]::Min(88.0 / $source.Width, 66.0 / $source.Height)
    $width = [single]($source.Width * $scale)
    $height = [single]($source.Height * $scale)
    $rectangle = [System.Drawing.RectangleF]::new(([single](88 - $width) / 2), ([single](66 - $height) / 2), $width, $height)
    $graphics.DrawImage($source, $rectangle)
    $canvas.Save((Join-Path $folder 'handcuffs-sidebar.png'), [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose()
    $canvas.Dispose()
    $source.Dispose()
}
Get-Item -LiteralPath (Join-Path $folder 'handcuffs-sidebar.png') | Select-Object Name, Length
