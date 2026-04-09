#Requires -Version 5.1
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Глобальные переменные ---
$script:SelectedFile = $null
$script:ErrorLine    = 0

# --- Цвета для вывода (безопасный синтаксис) ---
$colBlack  = [System.Drawing.Color]::FromName("Black")
$colBlue   = [System.Drawing.Color]::FromName("Blue")
$colCyan   = [System.Drawing.Color]::FromName("DarkCyan")
$colRed    = [System.Drawing.Color]::FromName("Red")
$colGreen  = [System.Drawing.Color]::FromName("DarkGreen")
$colOrange = [System.Drawing.Color]::FromName("Orange")
$colGray   = [System.Drawing.Color]::FromName("Gray")

# --- Инициализация формы ---
$form = New-Object System.Windows.Forms.Form
$form.Text = "Валидатор XML/JSON"
$form.Size = New-Object System.Drawing.Size(720, 620)
$form.StartPosition = "CenterScreen"
$form.MaximizeBox = $false
$form.MinimumSize = New-Object System.Drawing.Size(720, 620)

# --- Элементы управления ---
$btnSelect = New-Object System.Windows.Forms.Button
$btnSelect.Text = "Выбрать файл"
$btnSelect.Location = New-Object System.Drawing.Point(20, 20)
$btnSelect.Size = New-Object System.Drawing.Size(120, 30)
$btnSelect.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)

$lblPath = New-Object System.Windows.Forms.Label
$lblPath.Text = "Файл не выбран"
$lblPath.Location = New-Object System.Drawing.Point(150, 25)
$lblPath.Size = New-Object System.Drawing.Size(520, 20)
$lblPath.ForeColor = $colGray
$lblPath.AutoEllipsis = $true

$btnValidate = New-Object System.Windows.Forms.Button
$btnValidate.Text = "Проверить"
$btnValidate.Location = New-Object System.Drawing.Point(20, 65)
$btnValidate.Size = New-Object System.Drawing.Size(120, 30)
$btnValidate.Enabled = $false
$btnValidate.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)

$btnOpenEditor = New-Object System.Windows.Forms.Button
$btnOpenEditor.Text = "Открыть в редакторе"
$btnOpenEditor.Location = New-Object System.Drawing.Point(150, 65)
$btnOpenEditor.Size = New-Object System.Drawing.Size(160, 30)
$btnOpenEditor.Enabled = $false
$btnOpenEditor.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
#$btnOpenEditor.ToolTipText = "Откроет файл и перейдёт на строку с ошибкой"

$rtbOutput = New-Object System.Windows.Forms.RichTextBox
$rtbOutput.Location = New-Object System.Drawing.Point(20, 115)
$rtbOutput.Size = New-Object System.Drawing.Size(660, 460)
$rtbOutput.ReadOnly = $true
$rtbOutput.Font = New-Object System.Drawing.Font("Consolas", 10)
$rtbOutput.WordWrap = $true
$rtbOutput.ScrollBars = [System.Windows.Forms.RichTextBoxScrollBars]::Vertical
$rtbOutput.BorderStyle = [System.Windows.Forms.BorderStyle]::Fixed3D

$form.Controls.AddRange(@($btnSelect, $lblPath, $btnValidate, $btnOpenEditor, $rtbOutput))

# --- Логика вывода ---
function Write-OutputMessage {
    param([string]$Message, [System.Drawing.Color]$Color = $colBlack)
    $rtbOutput.SelectionStart = $rtbOutput.TextLength
    $rtbOutput.SelectionLength = 0
    $rtbOutput.SelectionColor = $Color
    $rtbOutput.AppendText("$Message`n")
    $rtbOutput.SelectionColor = $rtbOutput.ForeColor
}

# --- Открытие файла с переходом на строку ---
function Open-FileAtLine {
    param([string]$FilePath, [int]$Line)
    
    if ($Line -le 0) {
        Write-OutputMessage "⚠️ Номер строки не определён. Открываю файл без перехода." -Color $colOrange
        Start-Process -FilePath $FilePath
        return
    }

    $editors = @(
        @{Name="VS Code"; Cmd="code.exe"; Args=@("-g", "${FilePath}:$Line")}
        @{Name="Notepad++"; Cmd="notepad++.exe"; Args=@("-n$Line", $FilePath)}
        @{Name="Sublime Text"; Cmd="subl.exe"; Args=@("-n", "$Line", $FilePath)}
        @{Name="Notepad"; Cmd="notepad.exe"; Args=@($FilePath); NoLineJump=$true}
    )

    foreach ($ed in $editors) {
        # Берём только первый найденный исполняемый файл, чтобы избежать ошибки "System.Object[]"
        $cmd = Get-Command $ed.Cmd -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        
        if ($cmd -and $cmd.Source) {
            Start-Process -FilePath $cmd.Source -ArgumentList $ed.Args
            if ($ed.NoLineJump) {
                Write-OutputMessage "📂 Открыто в Notepad. Перейдите на строку $Line вручную (Ctrl+G)." -Color $colOrange
            } else {
                Write-OutputMessage "📂 Открыто в $($ed.Name) на строке $Line" -Color $colGreen
            }
            return
        }
    }

    # Фолбэк: открытие ассоциированным приложением
    Start-Process -FilePath $FilePath
    Write-OutputMessage "📂 Открыто в редакторе по умолчанию. Строка: $Line" -Color $colGray
}

# --- Валидация XML ---
function Test-Xml {
    param([string]$FilePath)
    $settings = [System.Xml.XmlReaderSettings]::new()
    $settings.CheckCharacters = $true
    $settings.IgnoreComments = $true
    $settings.IgnoreWhitespace = $false
    $reader = $null

    try {
        $reader = [System.Xml.XmlReader]::Create($FilePath, $settings)
        while ($reader.Read()) {}
        $script:ErrorLine = 0
        $btnOpenEditor.Enabled = $false
        Write-OutputMessage "✅ Файл XML корректен. Ошибок не найдено." -Color $colGreen
    }
    catch [System.Xml.XmlException] {
        $script:ErrorLine = $_.Exception.LineNumber
        $pos  = $_.Exception.LinePosition
        $msg  = $_.Exception.Message
        $btnOpenEditor.Enabled = $true
        Write-OutputMessage "❌ ОШИБКА XML (Строка $script:ErrorLine, Позиция $pos):" -Color $colRed
        Write-OutputMessage "   $msg" -Color $colRed
    }
    catch {
        Write-OutputMessage "❌ Неизвестная ошибка при чтении XML: $_" -Color $colRed
    }
    finally {
        if ($reader) { $reader.Close() }
    }
}

# --- Валидация JSON ---
function Test-Json {
    param([string]$Content)
    
    if ([System.Type]::GetType("System.Text.Json.JsonDocument")) {
        try {
            $null = [System.Text.Json.JsonDocument]::Parse($Content)
            $script:ErrorLine = 0
            $btnOpenEditor.Enabled = $false
            Write-OutputMessage "✅ Файл JSON корректен. Ошибок не найдено." -Color $colGreen
        }
        catch [System.Text.Json.JsonException] {
            $script:ErrorLine = $_.Exception.LineNumber
            if (-not $script:ErrorLine -or $script:ErrorLine -le 0) { $script:ErrorLine = 1 }
            $msg  = $_.Exception.Message
            $btnOpenEditor.Enabled = $true
            Write-OutputMessage "❌ ОШИБКА JSON (Строка $script:ErrorLine):" -Color $colRed
            Write-OutputMessage "   $msg" -Color $colRed
        }
    }
    else {
        # Фолбэк для PowerShell 5.1
        try {
            $null = $Content | ConvertFrom-Json
            $script:ErrorLine = 0
            $btnOpenEditor.Enabled = $false
            Write-OutputMessage "✅ Файл JSON корректен. Ошибок не найдено." -Color $colGreen
        }
        catch {
            $msg = $_.Exception.Message
            if ($msg -match 'Line:\s*(\d+)') {
                $script:ErrorLine = [int]$Matches[1]
            } else {
                $script:ErrorLine = 1
            }
            $btnOpenEditor.Enabled = $true
            Write-OutputMessage "❌ ОШИБКА JSON (Строка $script:ErrorLine):" -Color $colRed
            Write-OutputMessage "   $msg" -Color $colRed
        }
    }
}

# --- Обработчики событий ---
$btnSelect.Add_Click({
    $dlg = New-Object System.Windows.Forms.OpenFileDialog
    $dlg.Title = "Выберите XML или JSON файл"
    $dlg.Filter = "XML/JSON файлы|*.xml;*.json|XML файлы|*.xml|JSON файлы|*.json|Все файлы|*.*"
    $dlg.InitialDirectory = [System.Environment]::GetFolderPath("MyDocuments")
    
    if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $script:SelectedFile = $dlg.FileName
        $lblPath.Text = $script:SelectedFile
        $lblPath.ForeColor = $colBlack
        $btnValidate.Enabled = $true
        $btnOpenEditor.Enabled = $false
        $script:ErrorLine = 0
        $rtbOutput.Clear()
    }
})

$btnValidate.Add_Click({
    $rtbOutput.Clear()
    $script:ErrorLine = 0
    $btnOpenEditor.Enabled = $false

    if (-not (Test-Path $script:SelectedFile)) {
        Write-OutputMessage "❌ Файл не найден по указанному пути." -Color $colRed
        return
    }

    $ext = [System.IO.Path]::GetExtension($script:SelectedFile).ToLower()
    Write-OutputMessage "📁 Файл: $script:SelectedFile" -Color $colBlue
    Write-OutputMessage "🔍 Проверка синтаксиса..." -Color $colCyan

    switch ($ext) {
        ".xml" { Test-Xml -FilePath $script:SelectedFile }
        ".json" {
            $content = Get-Content -Path $script:SelectedFile -Raw -Encoding UTF8
            Test-Json -Content $content
        }
        default { Write-OutputMessage "⚠️ Неподдерживаемый формат. Выберите .xml или .json" -Color $colOrange }
    }
})

$btnOpenEditor.Add_Click({
    if ($script:ErrorLine -gt 0 -and $script:SelectedFile) {
        Open-FileAtLine -FilePath $script:SelectedFile -Line $script:ErrorLine
    }
})

# --- Запуск приложения ---
[System.Windows.Forms.Application]::EnableVisualStyles()
[System.Windows.Forms.Application]::Run($form)
