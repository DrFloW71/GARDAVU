# Rasterisation des primitives du SVG local avec System.Drawing, sans dépendance réseau.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = Split-Path -Parent $PSScriptRoot
$folder = Join-Path $root 'gardavu\assets'
[xml]$svg = Get-Content -LiteralPath (Join-Path $folder 'gardavu.svg') -Raw
$canvas = [System.Drawing.Bitmap]::new(1024, 1024)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
try {
    $graphics.Clear([System.Drawing.Color]::Transparent)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.ScaleTransform(4, 4)
    foreach ($shape in $svg.DocumentElement.ChildNodes) {
        if ($shape.LocalName -eq 'title') { continue }
        if ($shape.LocalName -notin @('circle', 'rect')) { throw "Primitive SVG non prise en charge : $($shape.LocalName)" }
        $state = $graphics.Save()
        $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
        $brush = $null
        $pen = $null
        try {
            $transform = $shape.GetAttribute('transform')
            if ($transform) {
                if ($transform -notmatch '^rotate\((-?[\d.]+) ([\d.]+) ([\d.]+)\)$') { throw "Transformation SVG non prise en charge : $transform" }
                $graphics.TranslateTransform([single]$Matches[2], [single]$Matches[3])
                $graphics.RotateTransform([single]$Matches[1])
                $graphics.TranslateTransform(-[single]$Matches[2], -[single]$Matches[3])
            }
            if ($shape.LocalName -eq 'circle') {
                $radius = [single]$shape.r
                $path.AddEllipse([single]$shape.cx - $radius, [single]$shape.cy - $radius, 2 * $radius, 2 * $radius)
            } else {
                $x = [single]$shape.x
                $y = [single]$shape.y
                $width = [single]$shape.width
                $height = [single]$shape.height
                $diameter = 2 * [single]$shape.rx
                if ($diameter -gt 0) {
                    $path.AddArc($x, $y, $diameter, $diameter, 180, 90)
                    $path.AddArc($x + $width - $diameter, $y, $diameter, $diameter, 270, 90)
                    $path.AddArc($x + $width - $diameter, $y + $height - $diameter, $diameter, $diameter, 0, 90)
                    $path.AddArc($x, $y + $height - $diameter, $diameter, $diameter, 90, 90)
                    $path.CloseFigure()
                } else {
                    $path.AddRectangle([System.Drawing.RectangleF]::new($x, $y, $width, $height))
                }
            }
            $fill = $shape.GetAttribute('fill')
            if ($fill -and $fill -ne 'none') {
                $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($fill))
                $graphics.FillPath($brush, $path)
            }
            $stroke = $shape.GetAttribute('stroke')
            if ($stroke -and $stroke -ne 'none') {
                $pen = [System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml($stroke), [single]$shape.GetAttribute('stroke-width'))
                $pen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round
                $graphics.DrawPath($pen, $path)
            }
        } finally {
            if ($brush) { $brush.Dispose() }
            if ($pen) { $pen.Dispose() }
            $path.Dispose()
            $graphics.Restore($state)
        }
    }
    $sizes = @(16, 24, 32, 48, 64, 128, 256)
    $frames = [System.Collections.Generic.List[byte[]]]::new()
    foreach ($size in $sizes) {
        $bitmap = [System.Drawing.Bitmap]::new($size, $size)
        $scaled = [System.Drawing.Graphics]::FromImage($bitmap)
        $stream = [System.IO.MemoryStream]::new()
        try {
            $scaled.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $scaled.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $scaled.DrawImage($canvas, 0, 0, $size, $size)
            $bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
            $frames.Add($stream.ToArray())
            if ($size -eq 256) { [System.IO.File]::WriteAllBytes((Join-Path $folder 'gardavu.png'), $stream.ToArray()) }
        } finally {
            $stream.Dispose()
            $scaled.Dispose()
            $bitmap.Dispose()
        }
    }
    $output = [System.IO.File]::Create((Join-Path $folder 'gardavu.ico'))
    $writer = [System.IO.BinaryWriter]::new($output)
    try {
        $writer.Write([uint16]0)
        $writer.Write([uint16]1)
        $writer.Write([uint16]$sizes.Count)
        $offset = 6 + 16 * $sizes.Count
        for ($n = 0; $n -lt $sizes.Count; $n++) {
            $dimension = if ($sizes[$n] -eq 256) { 0 } else { $sizes[$n] }
            $writer.Write([byte]$dimension)
            $writer.Write([byte]$dimension)
            $writer.Write([byte]0)
            $writer.Write([byte]0)
            $writer.Write([uint16]1)
            $writer.Write([uint16]32)
            $writer.Write([uint32]$frames[$n].Length)
            $writer.Write([uint32]$offset)
            $offset += $frames[$n].Length
        }
        foreach ($frame in $frames) { $writer.Write([byte[]]$frame) }
    } finally {
        $writer.Dispose()
    }
} finally {
    $graphics.Dispose()
    $canvas.Dispose()
}
Get-Item -LiteralPath (Join-Path $folder 'gardavu.ico'), (Join-Path $folder 'gardavu.png') | Select-Object Name, Length
