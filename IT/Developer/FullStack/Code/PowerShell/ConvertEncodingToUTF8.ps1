# Укажите расширение файлов, которые нужно проверить и конвертировать
$extension = "*.md"

# Получаем все файлы с указанным расширением в текущей папке и подпапках
Get-ChildItem -Path . -Recurse -Filter $extension -File | ForEach-Object {
    $filePath = $_.FullName

    # Читаем первые несколько байтов файла, чтобы определить кодировку
    $bytes = [System.IO.File]::ReadAllBytes($filePath)

    # Проверяем наличие BOM для UTF-8
    $isUtf8 = $false
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        $isUtf8 = $true
    }
    # Проверяем, что файл не содержит недопустимых байтов для UTF-8 (упрощённая проверка)
    else {
        $isUtf8 = $true
        for ($i = 0; $i -lt $bytes.Length; $i++) {
            if ($bytes[$i] -gt 0x7F) {
                # Проверяем, что это допустимый UTF-8 байт
                if (($bytes[$i] -band 0xE0) -eq 0xC0) {
                    # Двухбайтовая последовательность
                    if ($i + 1 -ge $bytes.Length -or ($bytes[$i + 1] -band 0xC0) -ne 0x80) {
                        $isUtf8 = $false
                        break
                    }
                    $i++
                }
                elseif (($bytes[$i] -band 0xF0) -eq 0xE0) {
                    # Трехбайтовая последовательность
                    if ($i + 2 -ge $bytes.Length -or
                        ($bytes[$i + 1] -band 0xC0) -ne 0x80 -or
                        ($bytes[$i + 2] -band 0xC0) -ne 0x80) {
                        $isUtf8 = $false
                        break
                    }
                    $i += 2
                }
                elseif (($bytes[$i] -band 0xF8) -eq 0xF0) {
                    # Четырехбайтовая последовательность
                    if ($i + 3 -ge $bytes.Length -or
                        ($bytes[$i + 1] -band 0xC0) -ne 0x80 -or
                        ($bytes[$i + 2] -band 0xC0) -ne 0x80 -or
                        ($bytes[$i + 3] -band 0xC0) -ne 0x80) {
                        $isUtf8 = $false
                        break
                    }
                    $i += 3
                }
                else {
                    $isUtf8 = $false
                    break
                }
            }
        }
    }

    if (-not $isUtf8) {
        # Читаем содержимое файла в исходной кодировке
        $content = Get-Content -Path $filePath -Raw -Encoding Default

        # Сохраняем файл в кодировке UTF-8 (без BOM)
        $content | Out-File -FilePath $filePath -Encoding utf8 -Force
        Write-Host "Конвертирован файл: $filePath"
    }
    else {
        Write-Host "Файл уже в UTF-8, пропускаем: $filePath"
    }
}