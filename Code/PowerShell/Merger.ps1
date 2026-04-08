<#
.SYNOPSIS
    Объединяет файлы из указанной папки (и подпапок) по шаблону в один файл или группирует их по расширению.

.PARAMETER InputFolder
    Путь к папке, файлы из которой нужно объединить.

.PARAMETER Pattern
    Шаблон файлов (например, "*.py").

.PARAMETER OutputFile
    Путь к результирующему файлу. При группировке используется как основа имени (к базовому имени добавляется расширение найденных файлов).

.PARAMETER GroupByType
    1 - группировать файлы по расширению (создаётся отдельный файл для каждого типа). 
    0 - объединить все файлы в один указанный файл (по умолчанию).

.EXAMPLE
    # Обычный режим: всё в один файл
    .\Merger.ps1 -InputFolder "C:\path\to\folder" -Pattern "*.py" -OutputFile "C:\path\to\output.txt"

    # Режим группировки: создаст output_py.txt, output_sql.txt и т.д.
    .\Merger.ps1 -InputFolder ""C:\path\to\folder" -Pattern "*.*" -OutputFile "C:\path\to\merged.txt" -GroupByType 1
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$InputFolder,

    [Parameter(Mandatory=$true)]
    [string]$Pattern,

    [Parameter(Mandatory=$true)]
    [string]$OutputFile,

    [Parameter(Mandatory=$true)]
    [ValidateSet(0, 1)]
    [int]$GroupByType = 0
)

# Убираем возможный слеш в конце пути, чтобы корректно работал Substring
$InputFolder = $InputFolder.TrimEnd('\', '/')

# Проверка существования папки
if (-not (Test-Path $InputFolder)) {
    Write-Error "Папка '$InputFolder' не найдена."
    exit 1
}

# Рекурсивный поиск файлов по шаблону
$files = Get-ChildItem -Path $InputFolder -Recurse -Filter $Pattern -File
# Гарантируем, что $totalFiles будет числом (даже если найден 0 или 1 файл)
$totalFiles = @($files).Count

if ($totalFiles -eq 0) {
    Write-Warning "Файлы, соответствующие шаблону '$Pattern', не найдены в папке '$InputFolder'."
    exit 0
}

$counter = 0

if ($GroupByType -eq 1) {
    # ---------------- РЕЖИМ ГРУППИРОВКИ ПО РАСШИРЕНИЮ ----------------
    $outDir      = Split-Path -Path $OutputFile
    $outBase     = [System.IO.Path]::GetFileNameWithoutExtension($OutputFile)
    $outExt      = [System.IO.Path]::GetExtension($OutputFile)

    $groupedFiles = $files | Group-Object -Property Extension

    foreach ($group in $groupedFiles) {
        $ext        = $group.Name
        $extClean   = $ext.TrimStart('.')
        # Формируем имя выходного файла: <Base>_<Расширение><ИсходноеРасширение>
        $currentOut = Join-Path $outDir "${outBase}_${extClean}$outExt"

        # Создаём или очищаем файл группы
        if (Test-Path $currentOut) {
            Clear-Content -Path $currentOut -ErrorAction SilentlyContinue
        } else {
            New-Item -Path $currentOut -ItemType File -Force | Out-Null
        }

        foreach ($file in $group.Group) {
            $counter++
            $percent = [math]::Round(($counter / $totalFiles) * 100)

            Write-Progress -Activity "Объединение файлов (группировка по типу)" -Status "Обработка: $counter/$totalFiles ($percent%)" -PercentComplete $percent

            $relativePath = $file.FullName.Substring($InputFolder.Length).TrimStart('\')
            Add-Content -Path $currentOut -Value "=== File: $relativePath"
            Add-Content -Path $currentOut -Value (Get-Content $file.FullName -Raw)
            Add-Content -Path $currentOut -Value ""
        }
        Write-Host "[$ext] Файлы объединены в: $currentOut" -ForegroundColor Cyan
    }
    Write-Progress -Activity "Объединение файлов (группировка по типу)" -Completed

} else {
    # ---------------- ОРИГИНАЛЬНЫЙ РЕЖИМ (ВСЁ В ОДИН ФАЙЛ) ----------------
    Clear-Content -Path $OutputFile -ErrorAction SilentlyContinue

    foreach ($file in $files) {
        $counter++
        $percent = [math]::Round(($counter / $totalFiles) * 100)

        Write-Progress -Activity "Объединение файлов" -Status "Обработка: $counter/$totalFiles ($percent%)" -PercentComplete $percent

        $relativePath = $file.FullName.Substring($InputFolder.Length).TrimStart('\')
        Add-Content -Path $OutputFile -Value "=== File: $relativePath"
        Add-Content -Path $OutputFile -Value (Get-Content $file.FullName -Raw)
        Add-Content -Path $OutputFile -Value ""
    }
    Write-Progress -Activity "Объединение файлов" -Completed

    Write-Host ""
    Write-Host "Файлы успешно объединены в: " -NoNewline
    Write-Host "$OutputFile" -ForegroundColor Green
}