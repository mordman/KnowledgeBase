#Requires -Version 5.1
<#
.SYNOPSIS
    Анализатор размеров файлов и папок: дерево каталогов + отсортированный список
    с цветовой подсветкой (отдельные правила для файлов и папок).
    Поддерживает учёт скрытых и системных элементов.
#>

# ====================== ПАРАМЕТРЫ СКРИПТА ======================
param(
    [Parameter(Position = 0)]
    [string]$Path
)

# Безопасная установка кодировки (в ISE/VSCode может падать)
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }

#region ====================== НАСТРОЙКИ ======================

$Settings = @{
    TargetPath            = "C:\GIT"
    ShowTopN              = 10
    SortProperty          = "Length"
    SortDescending        = $true
    ShowTree              = $true
    ShowFilesInTree       = $false
    ShowStatsInTree       = $true
    ShowFullPath          = $false
    DefaultColor          = "Gray"
    FolderDefaultColor    = "Cyan"

    # // НОВОЕ: учитывать скрытые и системные файлы/папки
    IncludeHidden         = $true
}

# --- Правила подсветки ФАЙЛОВ ---
$ColorRules = @(
    @{ Operator = '=';  Value = 0;        Color = 'Red'        }
    @{ Operator = '>';  Value = '1GB';    Color = 'Cyan'       }
    @{ Operator = '>';  Value = '100MB';  Color = 'Magenta'    }
    @{ Operator = '>';  Value = '10MB';   Color = 'Yellow'     }
    @{ Operator = '<';  Value = '1KB';    Color = 'DarkGray'   }
)

# --- Правила подсветки ПАПОК (по суммарному размеру) ---
$FolderColorRules = @(
    @{ Operator = '=';  Value = 0;        Color = 'DarkGray'   }
    @{ Operator = '>';  Value = '1GB';    Color = 'Red'        }
    @{ Operator = '>';  Value = '100MB';  Color = 'Magenta'    }
    @{ Operator = '>';  Value = '10MB';   Color = 'Yellow'     }
    @{ Operator = '<';  Value = '1KB';    Color = 'DarkCyan'   }
)

#endregion ====================================================

# -------- Вспомогательные функции --------

function ConvertTo-Bytes {
    param($Value)
    if ($null -eq $Value) { return 0 }
    if ($Value -is [long] -or $Value -is [int] -or $Value -is [double]) {
        return [long]$Value
    }
    $s = "$Value".Trim().ToUpper()
    switch -Regex ($s) {
        '^([0-9]+(?:\.[0-9]+)?)\s*TB$' { return [long]([double]$matches[1] * 1TB) }
        '^([0-9]+(?:\.[0-9]+)?)\s*GB$' { return [long]([double]$matches[1] * 1GB) }
        '^([0-9]+(?:\.[0-9]+)?)\s*MB$' { return [long]([double]$matches[1] * 1MB) }
        '^([0-9]+(?:\.[0-9]+)?)\s*KB$' { return [long]([double]$matches[1] * 1KB) }
        '^([0-9]+(?:\.[0-9]+)?)\s*B$'  { return [long][double]$matches[1] }
        default {
            $n = 0L
            if ([long]::TryParse($s, [ref]$n)) { return $n }
            throw "Невозможно распознать размер: '$Value'"
        }
    }
}

function Format-FileSize {
    param([long]$Bytes)
    if ($Bytes -ge 1TB) { return "{0,8:N2} TB" -f ($Bytes / 1TB) }
    if ($Bytes -ge 1GB) { return "{0,8:N2} GB" -f ($Bytes / 1GB) }
    if ($Bytes -ge 1MB) { return "{0,8:N2} MB" -f ($Bytes / 1MB) }
    if ($Bytes -ge 1KB) { return "{0,8:N2} KB" -f ($Bytes / 1KB) }
    return "{0,8}  B" -f $Bytes
}

function Get-ColorForFileSize {
    param([long]$Size)
    foreach ($rule in $ColorRules) {
        $threshold = ConvertTo-Bytes $rule.Value
        $hit = $false
        switch ($rule.Operator) {
            '='  { $hit = ($Size -eq $threshold) }
            '!=' { $hit = ($Size -ne $threshold) }
            '>'  { $hit = ($Size -gt  $threshold) }
            '<'  { $hit = ($Size -lt  $threshold) }
            '>=' { $hit = ($Size -ge  $threshold) }
            '<=' { $hit = ($Size -le  $threshold) }
        }
        if ($hit) { return $rule.Color }
    }
    return $Settings.DefaultColor
}

function Get-ColorForFolderSize {
    param([long]$Size)
    foreach ($rule in $FolderColorRules) {
        $threshold = ConvertTo-Bytes $rule.Value
        $hit = $false
        switch ($rule.Operator) {
            '='  { $hit = ($Size -eq $threshold) }
            '!=' { $hit = ($Size -ne $threshold) }
            '>'  { $hit = ($Size -gt  $threshold) }
            '<'  { $hit = ($Size -lt  $threshold) }
            '>=' { $hit = ($Size -ge  $threshold) }
            '<=' { $hit = ($Size -le  $threshold) }
        }
        if ($hit) { return $rule.Color }
    }
    return $Settings.FolderDefaultColor
}

function Show-DirectoryTree {
    param(
        [string]$CurrentPath,
        [string]$Indent      = "",
        [bool]  $IsLast      = $true,
        [bool]  $IsRoot      = $true
    )

    $dir = Get-Item -LiteralPath $CurrentPath -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue
    if (-not $dir) { return }

    if ($IsRoot) {
        $connector   = ""
        $childIndent = ""
    } else {
        if ($IsLast) {
            $connector   = "└── "
            $childIndent = $Indent + "    "
        } else {
            $connector   = "├── "
            $childIndent = $Indent + "│   "
        }
    }

    # // НОВОЕ: -Force добавлен для учёта скрытых файлов
    $filesInDir = @(Get-ChildItem -LiteralPath $CurrentPath -File -Recurse `
                    -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue)
    $count = $filesInDir.Count
    $total = ($filesInDir | Measure-Object -Property Length -Sum).Sum
    if ($null -eq $total) { $total = 0L }

    $folderColor = Get-ColorForFolderSize $total

    # Маркер скрытой папки
    $hiddenMark = ""
    if ($dir.Attributes -band [System.IO.FileAttributes]::Hidden) {
        $hiddenMark = " [hidden]"
    }

    $stats = ""
    if ($Settings.ShowStatsInTree) {
        $stats = "  [$count файл(ов), $(Format-FileSize $total)]"
    }

    Write-Host ($Indent + $connector) -NoNewline
    Write-Host $dir.Name -ForegroundColor $folderColor -NoNewline
    Write-Host $hiddenMark -ForegroundColor DarkMagenta -NoNewline   # // НОВОЕ: метка [hidden]
    Write-Host $stats -ForegroundColor DarkGray

    $children = @()
    # // НОВОЕ: -Force добавлен для дочерних папок и файлов
    $children += @(Get-ChildItem -LiteralPath $CurrentPath -Directory `
                   -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue | Sort-Object Name)
    if ($Settings.ShowFilesInTree) {
        $children += @(Get-ChildItem -LiteralPath $CurrentPath -File `
                       -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue | Sort-Object Name)
    }

    for ($i = 0; $i -lt $children.Count; $i++) {
        $last = ($i -eq $children.Count - 1)
        if ($children[$i] -is [System.IO.DirectoryInfo]) {
            Show-DirectoryTree -CurrentPath $children[$i].FullName `
                               -Indent $childIndent `
                               -IsLast $last `
                               -IsRoot $false
        } else {
            if ($last) { $c = "└── " } else { $c = "├── " }
            $sz    = Format-FileSize $children[$i].Length
            $color = Get-ColorForFileSize $children[$i].Length

            # // НОВОЕ: метка [hidden] для скрытых файлов в дереве
            $fileHiddenMark = ""
            if ($children[$i].Attributes -band [System.IO.FileAttributes]::Hidden) {
                $fileHiddenMark = " [hidden]"
            }

            Write-Host ($childIndent + $c) -NoNewline
            Write-Host $children[$i].Name -ForegroundColor $color -NoNewline
            Write-Host $fileHiddenMark -ForegroundColor DarkMagenta -NoNewline
            Write-Host ("  ($sz)") -ForegroundColor DarkGray
        }
    }
}

# -------- Основной код --------

$target = if ($Path) { $Path } else { $Settings.TargetPath }

if (-not (Test-Path -LiteralPath $target -PathType Container)) {
    Write-Error "Каталог не найден: $target"
    return
}
$target = (Resolve-Path -LiteralPath $target).Path

if ($Settings.SortDescending) { $sortDir = 'по убыв.' } else { $sortDir = 'по возр.' }
if ($Settings.ShowTopN -le 0) { $topNText = 'ВСЕ' } else { $topNText = "Топ $($Settings.ShowTopN)" }
# // НОВОЕ: текст статуса скрытых файлов
if ($Settings.IncludeHidden) { $hiddenText = 'ДА (скрытые + системные)' } else { $hiddenText = 'НЕТ' }

Write-Host "`n========================================" -ForegroundColor White
Write-Host " Анализ каталога: $target" -ForegroundColor White
Write-Host " Сортировка     : $($Settings.SortProperty) ($sortDir)" -ForegroundColor White
Write-Host " Показать файлов: $topNText" -ForegroundColor White
Write-Host " Скрытые файлы  : $hiddenText" -ForegroundColor White   # // НОВОЕ
Write-Host "========================================`n" -ForegroundColor White

if ($Settings.ShowTree) {
    Write-Host "── Структура каталогов ──" -ForegroundColor Yellow
    Show-DirectoryTree -CurrentPath $target
    Write-Host ""
}

# // НОВОЕ: -Force добавлен во все глобальные запросы
$allFiles   = @(Get-ChildItem -LiteralPath $target -File -Recurse `
                -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue)
$totalCount = $allFiles.Count
$totalSize  = ($allFiles | Measure-Object -Property Length -Sum).Sum
if ($null -eq $totalSize) { $totalSize = 0L }
$totalDirs  = @(Get-ChildItem -LiteralPath $target -Directory -Recurse `
                -Force:$Settings.IncludeHidden -ErrorAction SilentlyContinue).Count

# // НОВОЕ: отдельный счётчик скрытых элементов
$hiddenFilesCount = @($allFiles | Where-Object {
    $_.Attributes -band [System.IO.FileAttributes]::Hidden
}).Count

Write-Host "── Сводка ──" -ForegroundColor Yellow
Write-Host "Каталогов: $totalDirs (из них скрытых: $hiddenFilesCount)"
Write-Host "Файлов   : $totalCount "#(из них скрытых: $hiddenFilesCount)"
Write-Host "Общий размер: $(Format-FileSize $totalSize)" -ForegroundColor Green
Write-Host ""

$sorted = @($allFiles | Sort-Object -Property $Settings.SortProperty -Descending:$Settings.SortDescending)

if ($Settings.ShowTopN -gt 0 -and $sorted.Count -gt $Settings.ShowTopN) {
    $displayList = $sorted[0..($Settings.ShowTopN - 1)]
} else {
    $displayList = $sorted
}

Write-Host "── Список файлов ──" -ForegroundColor Yellow
Write-Host ("{0}   {1}" -f (" " * 8 + "РАЗМЕР"), "ПУТЬ") -ForegroundColor DarkGray
Write-Host ("{0}   {1}" -f ("-" * 14), ("-" * 60)) -ForegroundColor DarkGray

foreach ($file in $displayList) {
    $size  = Format-FileSize $file.Length
    $color = Get-ColorForFileSize $file.Length

    if ($Settings.ShowFullPath) {
        $displayPath = $file.FullName
    } else {
        $displayPath = $file.FullName.Substring($target.Length).TrimStart('\')
    }

    # // НОВОЕ: метка [hidden] в списке файлов
    $hiddenMark = ""
    if ($file.Attributes -band [System.IO.FileAttributes]::Hidden) {
        $hiddenMark = " [H]"
    }

    Write-Host "$size" -ForegroundColor $color -NoNewline
    Write-Host "   $displayPath" -ForegroundColor $color -NoNewline
    Write-Host $hiddenMark -ForegroundColor DarkMagenta
}

Write-Host "`nГотово. Показано файлов: $($displayList.Count) из $totalCount.`n" -ForegroundColor DarkGray