# ============================================================
# Simulate-Workday.ps1
# Полный симулятор рабочего дня
# ============================================================

[CmdletBinding()]
param(
    [int]$DurationMinutes = 0,
    [int]$DurationSeconds = 60,
    [int]$Seed = 0,

    [ValidateRange(0.1, 10.0)]
    [double]$Speed = 1.0,

    [string]$WorkDirectory = (Join-Path $env:TEMP 'SimWork'),

    [switch]$NoExcel,
    [switch]$NoWord,
    [switch]$NoVSCode,
    [switch]$NoNotepadPlus,
    [switch]$NoCmd,
    [switch]$NoPowerShell,
    [switch]$NoBrowser,
    [switch]$NoExplorer,

    [switch]$NoOutlook,
    [switch]$NoPowerPoint,
    [switch]$NoTerminal,
    [switch]$NoGit,
    [switch]$No7Zip,
    [switch]$NoCalculator,
    [switch]$NoTaskManager,
    [switch]$NoEventViewer,
    [switch]$NoSystemTools,

    [ValidateSet('Off', 'Instant', 'Smooth')]
    [string]$MouseMove = 'Smooth',

    [switch]$MouseClicks,
    [int]$MouseSteps = 16,
    [int]$MouseStepDelayMs = 18,

    [switch]$AllowSendKeys
)

# ============ Инициализация ============
$script:TotalSeconds = if ($DurationSeconds -gt 0) { $DurationSeconds } else { $DurationMinutes * 60 }
if ($script:TotalSeconds -le 0) { throw "Длительность должна быть больше 0." }

$script:Random = if ($Seed -ne 0) { [System.Random]::new($Seed) } else { [System.Random]::new() }
$script:Speed = $Speed
$script:StartTime = Get-Date
$script:Deadline = $script:StartTime.AddSeconds($script:TotalSeconds)
$script:Stopped = $false

$script:WorkDir = $WorkDirectory
if (-not (Test-Path $script:WorkDir)) {
    New-Item -ItemType Directory -Path $script:WorkDir -Force | Out-Null
}

$script:LogFile = Join-Path $script:WorkDir ("Simulate-Workday_{0:yyyyMMdd_HHmmss}.log" -f $script:StartTime)

$script:wdStyleNormal = -1
$script:wdStyleHeading1 = -2
$script:wdStyleHeading2 = -3

# ============ Логирование ============
function Write-LogLine {
    param(
        [string]$Message,
        [string]$Color = 'Gray',
        [int]$Indent = 0
    )

    $prefix = ' ' * $Indent
    $line = "[{0:HH:mm:ss}] {1}{2}" -f (Get-Date), $prefix, $Message

    try {
        Add-Content -Path $script:LogFile -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
    } catch {}

    Write-Host $line -ForegroundColor $Color
}

function WS { param($t) Write-LogLine -Message $t -Color Cyan }
function WA { param($t) Write-LogLine -Message "-> $t" -Color DarkYellow -Indent 4 }

# ============ Скорость и время ============
function ScaleSeconds {
    param([double]$Seconds)
    [math]::Max(0.02, $Seconds / $script:Speed)
}

function ScaleMs {
    param([double]$Ms)
    [int][math]::Max(10, $Ms / $script:Speed)
}

function LeftSec {
    [int]([math]::Round(($script:Deadline - (Get-Date)).TotalSeconds))
}

function Rnd {
    param([int]$Min, [int]$Max)
    if ($Min -eq $Max) { return $Min }
    $script:Random.Next($Min, $Max)
}

function RndDouble {
    param([double]$Min, [double]$Max)
    ($script:Random.NextDouble() * ($Max - $Min)) + $Min
}

function Pick-Random {
    param([array]$Items)
    if (-not $Items -or $Items.Count -eq 0) { return $null }
    $Items[$script:Random.Next(0, $Items.Count)]
}

function Assert-TimeLeft {
    param([int]$Reserve = 0)

    if ($script:Stopped) {
        throw "STOPPED: Остановлен пользователем."
    }

    if ((Get-Date) -ge $script:Deadline.AddSeconds(-$Reserve)) {
        if ($Reserve) {
            throw "TIMEOUT: Мало времени (запас $Reserve сек.)"
        } else {
            throw "TIMEOUT: Истекло время ($($script:TotalSeconds) сек.)"
        }
    }
}

function Wait-Safe {
    param([double]$Seconds)

    $target = (Get-Date).AddSeconds((ScaleSeconds $Seconds))

    while ((Get-Date) -lt $target) {
        Assert-TimeLeft

        $t = ($target - (Get-Date)).TotalMilliseconds
        $d = ($script:Deadline - (Get-Date)).TotalMilliseconds
        $s = [math]::Min(200, [math]::Min($t, $d))

        if ($s -gt 0) {
            Start-Sleep -Milliseconds $s
        }
    }
}

# ============ Retry для COM ============
function Invoke-WithRetry {
    param(
        [scriptblock]$Action,
        [int]$MaxRetries = 20,
        [int]$DelayMs = 400,
        [string]$Context = "COM"
    )

    $n = 0

    while ($true) {
        $n++

        try {
            return & $Action
        } catch {
            $m = $_.Exception.Message
            $isComBusy = $m -match "RPC_E_CALL_REJECTED|0x80010001|Вызов был отклонен|Call was rejected"

            if (-not $isComBusy -or $n -ge $MaxRetries) {
                throw
            }

            $sleepMs = ScaleMs $DelayMs
            Write-LogLine "    [retry $n/$MaxRetries] $Context занят, ждём ${sleepMs}мс..." -Color DarkGray -Indent 4
            Start-Sleep -Milliseconds $sleepMs
        }
    }
}

# ============ Мышь ============
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

if (-not ('NativeMethods' -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public struct RECT {
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
}

public static class NativeMethods {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
}
"@
}

function Get-ForegroundRect {
    try {
        $hwnd = [NativeMethods]::GetForegroundWindow()
        $rect = New-Object RECT

        if ([NativeMethods]::GetWindowRect($hwnd, [ref]$rect)) {
            return [PSCustomObject]@{
                Left   = $rect.Left
                Top    = $rect.Top
                Right  = $rect.Right
                Bottom = $rect.Bottom
                Width  = $rect.Right - $rect.Left
                Height = $rect.Bottom - $rect.Top
            }
        }
    } catch {}

    $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen

    return [PSCustomObject]@{
        Left   = $screen.Left
        Top    = $screen.Top
        Right  = $screen.Right
        Bottom = $screen.Bottom
        Width  = $screen.Width
        Height = $screen.Height
    }
}

function Invoke-MouseClick {
    param(
        [ValidateSet('Left')]
        [string]$Button = 'Left'
    )

    if (-not $MouseClicks) { return }

    [NativeMethods]::mouse_event([uint32]0x0002, 0, 0, 0, 0)
    Start-Sleep -Milliseconds (ScaleMs 70)
    [NativeMethods]::mouse_event([uint32]0x0004, 0, 0, 0, 0)

    Wait-Safe 0.12
}

function Move-MouseToPoint {
    param(
        [int]$X,
        [int]$Y
    )

    if ($MouseMove -eq 'Off') { return }

    $screen = [System.Windows.Forms.SystemInformation]::VirtualScreen

    $X = [math]::Max($screen.Left, [math]::Min($screen.Right - 1, $X))
    $Y = [math]::Max($screen.Top, [math]::Min($screen.Bottom - 1, $Y))

    if ($MouseMove -eq 'Instant') {
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($X, $Y)
        return
    }

    $start = [System.Windows.Forms.Cursor]::Position
    $steps = [math]::Max(2, [int]($MouseSteps / $script:Speed))

    for ($i = 1; $i -le $steps; $i++) {
        Assert-TimeLeft

        $t = $i / $steps
        $nx = [int]($start.X + ($X - $start.X) * $t)
        $ny = [int]($start.Y + ($Y - $start.Y) * $t)

        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($nx, $ny)
        Start-Sleep -Milliseconds (ScaleMs $MouseStepDelayMs)
    }
}

function Move-MouseToActiveWindowPoint {
    param(
        [double]$XRatio = 0.5,
        [double]$YRatio = 0.5,
        [int]$Jitter = 25,
        [switch]$Click
    )

    if ($MouseMove -eq 'Off') { return }

    $XRatio = [math]::Max(0.0, [math]::Min(1.0, $XRatio))
    $YRatio = [math]::Max(0.0, [math]::Min(1.0, $YRatio))

    $r = Get-ForegroundRect

    $jx = 0
    $jy = 0

    if ($Jitter -gt 0) {
        $jx = Rnd -$Jitter $Jitter
        $jy = Rnd -$Jitter $Jitter
    }

    $x = [int]($r.Left + ($r.Width * $XRatio) + $jx)
    $y = [int]($r.Top + ($r.Height * $YRatio) + $jy)

    Move-MouseToPoint -X $x -Y $y

    if ($Click) {
        Invoke-MouseClick
    }
}

function Move-MouseForTextInput {
    param(
        [ValidateSet('text', 'grid', 'terminal', 'ribbon', 'browser')]
        [string]$Target = 'text'
    )

    if ($MouseMove -eq 'Off') { return }

    switch ($Target) {
        'text' {
            $xr = RndDouble 0.35 0.75
            $yr = RndDouble 0.35 0.75
        }

        'grid' {
            $xr = RndDouble 0.30 0.80
            $yr = RndDouble 0.30 0.80
        }

        'terminal' {
            $xr = RndDouble 0.25 0.80
            $yr = RndDouble 0.50 0.85
        }

        'ribbon' {
            $xr = RndDouble 0.20 0.80
            $yr = RndDouble 0.12 0.25
        }

        'browser' {
            $xr = RndDouble 0.30 0.85
            $yr = RndDouble 0.25 0.75
        }

        default {
            $xr = 0.5
            $yr = 0.5
        }
    }

    Move-MouseToActiveWindowPoint -XRatio $xr -YRatio $yr -Jitter 25
    Wait-Safe 0.12
}

function Send-TextSafe {
    param(
        [string]$Text,
        [switch]$Enter
    )

    if (-not $AllowSendKeys) { return }

    Move-MouseForTextInput 'text'

    if ($MouseClicks) {
        Invoke-MouseClick
    }

    $escaped = $Text -replace '([+^%~(){}\[\]])', '{$1}'

    if ($Enter) {
        $escaped += '{ENTER}'
    }

    try {
        [System.Windows.Forms.SendKeys]::SendWait($escaped)
    } catch {}

    Wait-Safe 0.2
}

function Send-KeysRaw {
    param([string]$Keys)

    if (-not $AllowSendKeys) { return }

    try {
        [System.Windows.Forms.SendKeys]::SendWait($Keys)
    } catch {}

    Wait-Safe 0.15
}

# ============ Процессы и фокус ============
function Get-AppProc {
    param([string[]]$Name)

    if (-not $Name -or @($Name).Count -eq 0) { return $null }

    Get-Process -Name $Name -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 } |
        Sort-Object StartTime |
        Select-Object -Last 1
}

function Focus-App {
    param(
        [string[]]$Names,
        [int]$WaitMs = 500
    )

    if (-not $Names -or @($Names).Count -eq 0) { return $null }

    $p = Get-AppProc $Names

    if ($p) {
        try {
            $shell = New-Object -ComObject WScript.Shell
            $shell.AppActivate($p.Id) | Out-Null
        } catch {}

        Start-Sleep -Milliseconds (ScaleMs $WaitMs)

        Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.25 0.75) -YRatio (RndDouble 0.25 0.75) -Jitter 40
    }

    return $p
}

function Focus-AppByTitle {
    param(
        [string[]]$Titles,
        [int]$WaitMs = 500
    )

    if (-not $Titles -or @($Titles).Count -eq 0) { return $false }

    try {
        $shell = New-Object -ComObject WScript.Shell
    } catch {
        return $false
    }

    foreach ($t in $Titles) {
        try {
            $ok = $shell.AppActivate($t)

            if ($ok) {
                Start-Sleep -Milliseconds (ScaleMs $WaitMs)
                Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.25 0.75) -YRatio (RndDouble 0.25 0.75) -Jitter 35
                return $true
            }
        } catch {}
    }

    return $false
}

function Get-FocusNames {
    param([string]$App)

    switch ($App) {
        'Excel'       { @('EXCEL') }
        'Word'        { @('WINWORD') }
        'VSCode'      { @('Code', 'Code - Insiders') }
        'NotepadPlus' { @('notepad++') }
        'Cmd'         { @('cmd', 'WindowsTerminal', 'conhost') }
        'PowerShell'  { @('powershell', 'pwsh', 'WindowsTerminal') }
        'Browser'     { @('msedge', 'chrome', 'firefox', 'brave') }
        'Explorer'    { @('explorer') }

        'Outlook'     { @('OUTLOOK') }
        'PowerPoint'  { @('POWERPNT') }
        'Terminal'    { @('WindowsTerminal', 'wt') }
        'Git'         { @() }
        'SevenZip'    { @() }
        'Calculator'  { @('Calculator', 'CalculatorApp', 'ApplicationFrameHost') }
        'TaskManager' { @('Taskmgr') }
        'EventViewer' { @('mmc', 'eventvwr') }
        'SystemTools' { @() }

        default       { @() }
    }
}

# ============ Поиск приложений ============
function Get-NotepadPlusPath {
    $cmd = Get-Command notepad++ -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        "$env:ProgramFiles\Notepad++\notepad++.exe",
        "${env:ProgramFiles(x86)}\Notepad++\notepad++.exe",
        "$env:LOCALAPPDATA\Programs\Notepad++\notepad++.exe"
    )

    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }

    return $null
}

function Get-BrowserPath {
    $names = @('msedge', 'chrome', 'firefox', 'brave')

    foreach ($n in $names) {
        $cmd = Get-Command $n -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    }

    $candidates = @(
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
        "$env:ProgramFiles\Mozilla Firefox\firefox.exe",
        "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe",
        "$env:ProgramFiles\BraveSoftware\Brave-Browser\Application\brave.exe"
    )

    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }

    return $null
}

function Get-7ZipPath {
    $cmd = Get-Command 7z -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $cmd = Get-Command 7zG -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        "$env:ProgramFiles\7-Zip\7z.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7z.exe",
        "$env:ProgramFiles\7-Zip\7zG.exe",
        "${env:ProgramFiles(x86)}\7-Zip\7zG.exe"
    )

    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }

    return $null
}

$script:VSCodeCommand = Get-Command code -ErrorAction SilentlyContinue
$script:NotepadPlusExe = Get-NotepadPlusPath
$script:BrowserExe = Get-BrowserPath
$script:TerminalCommand = Get-Command wt -ErrorAction SilentlyContinue
$script:GitCommand = Get-Command git -ErrorAction SilentlyContinue
$script:SevenZipExe = Get-7ZipPath

$script:PowerShellExe = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
if (-not $script:PowerShellExe) {
    $script:PowerShellExe = (Get-Command powershell -ErrorAction SilentlyContinue).Source
}

$script:AppEnabled = @{
    Excel       = [bool](-not $NoExcel)
    Word        = [bool](-not $NoWord)
    VSCode      = [bool]((-not $NoVSCode) -and $script:VSCodeCommand)
    NotepadPlus = [bool]((-not $NoNotepadPlus) -and $script:NotepadPlusExe)
    Cmd         = [bool](-not $NoCmd)
    PowerShell  = [bool]((-not $NoPowerShell) -and $script:PowerShellExe)
    Browser     = [bool]((-not $NoBrowser) -and $script:BrowserExe)
    Explorer    = [bool](-not $NoExplorer)

    Outlook     = [bool](-not $NoOutlook)
    PowerPoint  = [bool](-not $NoPowerPoint)
    Terminal    = [bool]((-not $NoTerminal) -and $script:TerminalCommand)
    Git         = [bool]((-not $NoGit) -and $script:GitCommand)
    SevenZip    = [bool]((-not $No7Zip) -and $script:SevenZipExe)
    Calculator  = [bool](-not $NoCalculator)
    TaskManager = [bool](-not $NoTaskManager)
    EventViewer = [bool](-not $NoEventViewer)
    SystemTools = [bool](-not $NoSystemTools)
}

# ============ Контекст ============
$script:Ctx = @{
    Excel      = $null
    ExcelWb    = $null
    ExcelWs    = $null
    ExcelChart = $null
    Word       = $null
    WordDoc    = $null
    VSCodeFile = $null
}

# ============ Хелперы приложений ============
function Ensure-Excel {
    if ($script:Ctx.Excel -and $script:Ctx.ExcelWb) { return }

    $script:Ctx.Excel = New-Object -ComObject Excel.Application
    $script:Ctx.Excel.Visible = $true
    $script:Ctx.Excel.DisplayAlerts = $false

    Wait-Safe 1.2
    [void](Focus-App @('EXCEL') -WaitMs 700)

    $script:Ctx.ExcelWb = Invoke-WithRetry -Context "Excel.Workbooks.Add" -Action {
        $script:Ctx.Excel.Workbooks.Add()
    }

    $script:Ctx.ExcelWs = Invoke-WithRetry -Context "Excel.Worksheet" -Action {
        $script:Ctx.ExcelWb.Worksheets.Item(1)
    }

    WA "Excel: книга и лист созданы"
}

function Ensure-Word {
    if ($script:Ctx.Word -and $script:Ctx.WordDoc) { return }

    $script:Ctx.Word = New-Object -ComObject Word.Application
    $script:Ctx.Word.Visible = $true

    Wait-Safe 2.0
    [void](Focus-App @('WINWORD') -WaitMs 900)

    $script:Ctx.WordDoc = Invoke-WithRetry -Context "Word.Documents.Add" -MaxRetries 30 -DelayMs 500 -Action {
        $script:Ctx.Word.Documents.Add()
    }

    $null = Invoke-WithRetry -Context "Word warm-up" -MaxRetries 30 -DelayMs 500 -Action {
        $s = $script:Ctx.Word.Selection
        $null = $s.Start
        $s
    }

    WA "Word: документ создан"
}

function Ensure-VSCode {
    if (-not $script:VSCodeCommand) {
        throw "VS Code не найден."
    }

    $file = Join-Path $script:WorkDir "Scratch.ps1"

    if (-not (Test-Path $file)) {
        "# Scratch.ps1`r`n# Рабочий файл симулятора`r`n" | Set-Content -Path $file -Encoding UTF8
    }

    $script:Ctx.VSCodeFile = $file

    Start-Process -FilePath $script:VSCodeCommand.Source -ArgumentList "`"$file`""
    Wait-Safe 1.0
    [void](Focus-App @('Code', 'Code - Insiders') -WaitMs 500)
}

function Open-VSCodeFile {
    param([string]$Path)

    if (-not $script:VSCodeCommand) {
        throw "VS Code не найден."
    }

    Start-Process -FilePath $script:VSCodeCommand.Source -ArgumentList "`"$Path`""
    Wait-Safe 0.8

    [void](Focus-App @('Code', 'Code - Insiders') -WaitMs 500)
    Move-MouseForTextInput 'text'
}

function Ensure-NotepadPlus {
    if (-not $script:NotepadPlusExe) {
        throw "Notepad++ не найден."
    }
}

function Open-NotepadPlusFile {
    param([string]$Path)

    Ensure-NotepadPlus

    Start-Process -FilePath $script:NotepadPlusExe -ArgumentList "`"$Path`""
    Wait-Safe 0.7
    [void](Focus-App @('notepad++') -WaitMs 500)
}

function Invoke-CmdSim {
    param(
        [string]$Arguments,
        [string]$Description = "CMD"
    )

    $stamp = Get-Date -Format yyyyMMddHHmmssfff
    $out = Join-Path $script:WorkDir "cmd_out_$stamp.log"
    $err = Join-Path $script:WorkDir "cmd_err_$stamp.log"

    $p = Start-Process -FilePath $env:ComSpec `
        -ArgumentList '/c', $Arguments `
        -Wait `
        -PassThru `
        -NoNewWindow `
        -RedirectStandardOutput $out `
        -RedirectStandardError $err

    if (Test-Path $out) {
        $lines = Get-Content $out -TotalCount 5
        foreach ($line in $lines) {
            WA "$Description output: $line"
        }
    }

    if ($p.ExitCode -ne 0 -and (Test-Path $err) -and (Get-Item $err).Length -gt 0) {
        $errLine = Get-Content $err -TotalCount 1
        WA "$Description error: $errLine"
    }

    return $p.ExitCode
}

function Invoke-PowerShellScriptSim {
    param(
        [string]$ScriptContent,
        [string]$Description = "PowerShell"
    )

    $stamp = Get-Date -Format yyyyMMddHHmmssfff
    $file = Join-Path $script:WorkDir "ps_sim_$stamp.ps1"
    $out = Join-Path $script:WorkDir "ps_out_$stamp.log"
    $err = Join-Path $script:WorkDir "ps_err_$stamp.log"

    Set-Content -Path $file -Value $ScriptContent -Encoding UTF8

    $p = Start-Process -FilePath $script:PowerShellExe `
        -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $file `
        -Wait `
        -PassThru `
        -NoNewWindow `
        -RedirectStandardOutput $out `
        -RedirectStandardError $err

    if (Test-Path $out) {
        Get-Content $out -TotalCount 5 | ForEach-Object {
            WA "$Description output: $_"
        }
    }

    if ($p.ExitCode -ne 0 -and (Test-Path $err) -and (Get-Item $err).Length -gt 0) {
        $errLine = Get-Content $err -TotalCount 1
        WA "$Description error: $errLine"
    }

    return $p.ExitCode
}

function New-SimHtmlFile {
    param(
        [string]$Title,
        [string]$BodyHtml
    )

    $stamp = Get-Date -Format yyyyMMddHHmmssfff
    $path = Join-Path $script:WorkDir "page_$stamp.html"

    $html = @"
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>$Title</title>
<style>
body { font-family: Segoe UI, Arial, sans-serif; margin: 40px; background: #f7f9fc; }
h1 { color: #1f3b73; }
table { border-collapse: collapse; width: 100%; background: white; }
th, td { border: 1px solid #cfd8e3; padding: 8px; }
th { background: #e0f0ff; }
.footer { margin-top: 24px; color: #666; font-size: 12px; }
</style>
</head>
<body>
<h1>$Title</h1>
$BodyHtml
<div class="footer">Создано симулятором: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</div>
</body>
</html>
"@

    Set-Content -Path $path -Value $html -Encoding UTF8
    return $path
}

function Open-BrowserFile {
    param([string]$Path)

    if (-not $script:BrowserExe) {
        throw "Браузер не найден."
    }

    $uri = "file:///" + ($Path -replace '\\', '/')
    Start-Process -FilePath $script:BrowserExe -ArgumentList "`"$uri`""

    Wait-Safe 1.0
    [void](Focus-App @('msedge', 'chrome', 'firefox', 'brave') -WaitMs 700)
}

function Open-ExplorerTarget {
    param([string]$Target)

    if ($Target -like 'shell:*') {
        Start-Process explorer.exe -ArgumentList $Target
    } else {
        Start-Process explorer.exe -ArgumentList "`"$Target`""
    }

    Wait-Safe 0.7
    [void](Focus-App @('explorer') -WaitMs 400)
}

function Invoke-SevenZipSim {
    param(
        [string[]]$Arguments,
        [string]$Description = "7-Zip"
    )

    if (-not $script:SevenZipExe) {
        throw "7-Zip не найден."
    }

    $stamp = Get-Date -Format yyyyMMddHHmmssfff
    $out = Join-Path $script:WorkDir "7z_out_$stamp.log"
    $err = Join-Path $script:WorkDir "7z_err_$stamp.log"

    $p = Start-Process -FilePath $script:SevenZipExe `
        -ArgumentList $Arguments `
        -Wait `
        -PassThru `
        -NoNewWindow `
        -RedirectStandardOutput $out `
        -RedirectStandardError $err

    if (Test-Path $out) {
        Get-Content $out -TotalCount 5 | ForEach-Object {
            WA "$Description output: $_"
        }
    }

    if ($p.ExitCode -ne 0 -and (Test-Path $err) -and (Get-Item $err).Length -gt 0) {
        $errLine = Get-Content $err -TotalCount 1
        WA "$Description error: $errLine"
    }

    return $p.ExitCode
}

function Invoke-GitSim {
    param(
        [string[]]$Arguments,
        [string]$Description = "Git"
    )

    if (-not $script:GitCommand) {
        throw "Git не найден."
    }

    if (-not $script:GitRepoDir) {
        $script:GitRepoDir = Join-Path $script:WorkDir 'GitDemo'
    }

    if (-not (Test-Path $script:GitRepoDir)) {
        New-Item -ItemType Directory -Path $script:GitRepoDir -Force | Out-Null
    }

    $stamp = Get-Date -Format yyyyMMddHHmmssfff
    $out = Join-Path $script:WorkDir "git_out_$stamp.log"
    $err = Join-Path $script:WorkDir "git_err_$stamp.log"

    $p = Start-Process -FilePath $script:GitCommand.Source `
        -ArgumentList $Arguments `
        -WorkingDirectory $script:GitRepoDir `
        -Wait `
        -PassThru `
        -NoNewWindow `
        -RedirectStandardOutput $out `
        -RedirectStandardError $err

    if (Test-Path $out) {
        Get-Content $out -TotalCount 5 | ForEach-Object {
            WA "$Description output: $_"
        }
    }

    if ($p.ExitCode -ne 0 -and (Test-Path $err) -and (Get-Item $err).Length -gt 0) {
        $errLine = Get-Content $err -TotalCount 1
        WA "$Description error: $errLine"
    }

    return $p.ExitCode
}

function Ensure-GitRepo {
    if (-not $script:GitCommand) {
        throw "Git не найден."
    }

    if (-not $script:GitRepoDir) {
        $script:GitRepoDir = Join-Path $script:WorkDir 'GitDemo'
    }

    if (-not (Test-Path (Join-Path $script:GitRepoDir '.git'))) {
        New-Item -ItemType Directory -Path $script:GitRepoDir -Force | Out-Null

        $null = Invoke-GitSim -Arguments @('init') -Description "Git init"
        $null = Invoke-GitSim -Arguments @('config', 'user.name', 'SimWork') -Description "Git config name"
        $null = Invoke-GitSim -Arguments @('config', 'user.email', 'simwork@example.com') -Description "Git config email"

        Set-Content -Path (Join-Path $script:GitRepoDir 'README.md') -Value "# SimWork Git Demo" -Encoding UTF8

        $null = Invoke-GitSim -Arguments @('add', '.') -Description "Git add"
        $null = Invoke-GitSim -Arguments @('commit', '-m', 'Initial sim commit') -Description "Git initial commit"
    }
}

function Invoke-OutlookItemAction {
    param(
        [scriptblock]$Action,
        [string]$Extension = '.msg',
        [int]$SaveAsFormat = 4
    )

    $wasRunning = [bool](Get-Process OUTLOOK -ErrorAction SilentlyContinue)

    $app = New-Object -ComObject Outlook.Application
    $item = & $Action $app

    $path = Join-Path $script:WorkDir ("OutlookItem_" + (Get-Date -Format 'yyyyMMddHHmmssfff') + $Extension)

    try {
        $item.SaveAs($path, $SaveAsFormat)
    } catch {}

    try {
        $item.Close(1)
    } catch {}

    if (-not $wasRunning) {
        try {
            $app.Quit()
        } catch {}
    }

    try { [Runtime.InteropServices.Marshal]::ReleaseComObject($item) | Out-Null } catch {}
    try { [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null } catch {}

    return $path
}

function Invoke-PowerPointAction {
    param(
        [scriptblock]$Action,
        [string]$Description = "PowerPoint"
    )

    $wasRunning = [bool](Get-Process POWERPNT -ErrorAction SilentlyContinue)

    $app = New-Object -ComObject PowerPoint.Application

    try {
        $app.Visible = $true
    } catch {}

    $pres = $app.Presentations.Add()

    $path = Join-Path $script:WorkDir ("PPT_" + (Get-Date -Format 'yyyyMMddHHmmssfff') + ".pptx")

    try {
        & $Action $app $pres

        try {
            $pres.SaveAs($path, 24)
        } catch {}
    } finally {
        try { $pres.Close() } catch {}

        if (-not $wasRunning) {
            try { $app.Quit() } catch {}
        }

        try { [Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null } catch {}
        try { [Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null } catch {}
    }

    return $path
}

function Open-Calculator {
    Start-Process calc.exe

    Wait-Safe 0.7

    [void](Focus-AppByTitle @('Калькулятор', 'Calculator') -WaitMs 400)

    Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.30 0.70) -YRatio (RndDouble 0.30 0.70) -Jitter 18
}

function Get-OrCreateTestZip {
    if (-not $script:SevenZipExe) {
        throw "7-Zip не найден."
    }

    $zip = Get-ChildItem -Path $script:WorkDir -Filter *.zip -File -ErrorAction SilentlyContinue |
        Select-Object -First 1

    if ($zip) {
        return $zip.FullName
    }

    $src = Join-Path $script:WorkDir "archive_source.txt"
    Set-Content -Path $src -Value "SimWork archive source file" -Encoding UTF8

    $zipPath = Join-Path $script:WorkDir ("archive_" + (Get-Date -Format 'yyyyMMddHHmmssfff') + ".zip")

    $null = Invoke-SevenZipSim -Arguments @('a', $zipPath, $src) -Description "7-Zip create"

    return $zipPath
}

# ============ Сценарии Excel ============
$script:ExcelScenarios = @(
    @{
        Name = "Квартальный отчёт с диаграммой"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel header" -Action {
                $ws.Cells.Item(1, 1) = "Квартальный отчёт"
                $ws.Range("A1:E1").Merge()
                $ws.Cells.Item(1, 1).Font.Bold = $true
                $ws.Cells.Item(1, 1).Font.Size = 14
                $ws.Cells.Item(1, 1).HorizontalAlignment = -4108
            }

            Wait-Safe 0.3
            WA "Заголовок записан"

            Invoke-WithRetry -Context "Excel table header" -Action {
                $h = @("Менеджер", "Янв", "Фев", "Мар", "Итого")
                for ($c = 0; $c -lt 5; $c++) {
                    $ws.Cells.Item(3, $c + 1) = $h[$c]
                    $ws.Cells.Item(3, $c + 1).Font.Bold = $true
                    $ws.Cells.Item(3, $c + 1).Interior.Color = 15773696
                }
            }

            $names = @("Иванов", "Петрова", "Сидоров", "Козлова", "Морозов")

            Invoke-WithRetry -Context "Excel data" -Action {
                for ($r = 0; $r -lt $names.Count; $r++) {
                    $ws.Cells.Item($r + 4, 1) = $names[$r]

                    for ($c = 2; $c -le 4; $c++) {
                        $ws.Cells.Item($r + 4, $c) = (Rnd 80000 200000)
                    }

                    $ws.Cells.Item($r + 4, 5).Formula = "=SUM(B$($r + 4):D$($r + 4))"
                }
            }

            WA "Данные менеджеров записаны"
            Wait-Safe 0.4

            $last = 3 + $names.Count + 1

            Invoke-WithRetry -Context "Excel total" -Action {
                $ws.Cells.Item($last, 1) = "ИТОГО"

                for ($c = 2; $c -le 5; $c++) {
                    $col = [char](64 + $c)
                    $ws.Cells.Item($last, $c).Formula = "=SUM($col`4:$col$($last - 1))"
                    $ws.Cells.Item($last, $c).Font.Bold = $true
                    $ws.Cells.Item($last, $c).Interior.Color = 13551615
                }

                $ws.Columns.Item("A:E").AutoFit() | Out-Null
            }

            WA "Итоговая строка готова"
            Wait-Safe 0.3

            Invoke-WithRetry -Context "Excel chart" -Action {
                $rng = $ws.Range("A3:E$($last - 1)")

                try {
                    $script:Ctx.ExcelChart = $ws.Shapes.AddChart2(240, 201)
                } catch {
                    $script:Ctx.ExcelChart = $ws.Shapes.AddChart()
                }

                $script:Ctx.ExcelChart.Chart.SetSourceData($rng)
                $script:Ctx.ExcelChart.Chart.HasTitle = $true
                $script:Ctx.ExcelChart.Chart.ChartTitle.Text = "Продажи"
            }

            WA "Диаграмма построена"
        }
    },
    @{
        Name = "Добавление и удаление строк"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            $sr = Invoke-WithRetry -Context "Excel UsedRange" -Action {
                ($ws.UsedRange.Rows.Count) + 2
            }

            if ($sr -lt 4) { $sr = 4 }

            $names = @("Новиков", "Фёдорова", "Белов")

            for ($i = 0; $i -lt 3; $i++) {
                Invoke-WithRetry -Context "Excel add row" -Action {
                    $ws.Cells.Item($sr + $i, 1) = $names[$i]
                    $ws.Cells.Item($sr + $i, 2) = (Rnd 50000 180000)
                    $ws.Cells.Item($sr + $i, 3) = (Rnd 50000 180000)
                }

                WA "Строка добавлена: $($names[$i])"
                Wait-Safe 0.3
            }

            Invoke-WithRetry -Context "Excel delete row" -Action {
                $ws.Rows.Item($sr + 1).Delete() | Out-Null
            }

            WA "Средняя строка удалена"
            Wait-Safe 0.3

            Invoke-WithRetry -Context "Excel insert row" -Action {
                $ws.Rows.Item($sr).Insert(-4121) | Out-Null
                $ws.Cells.Item($sr, 1) = "Вставлен"
                $ws.Cells.Item($sr, 2) = 123456
            }

            WA "Строка вставлена"
        }
    },
    @{
        Name = "Формулы и вычисления"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel formulas init" -Action {
                $ws.Cells.Item(1, 1) = "Формулы"
                $ws.Cells.Item(1, 1).Font.Bold = $true

                $ws.Cells.Item(3, 1) = "A"
                $ws.Cells.Item(3, 2) = "B"
                $ws.Cells.Item(3, 3) = "Результат"

                $ws.Cells.Item(4, 1) = (Rnd 10 100)
                $ws.Cells.Item(4, 2) = (Rnd 10 100)
            }

            $fs = @(
                @{ R = 5; F = "=A4+B4"; D = "Сумма" },
                @{ R = 6; F = "=A4-B4"; D = "Разность" },
                @{ R = 7; F = "=A4*B4"; D = "Произведение" },
                @{ R = 8; F = "=A4/B4"; D = "Деление" },
                @{ R = 9; F = "=POWER(A4,2)"; D = "Квадрат" }
            )

            foreach ($f in $fs) {
                Invoke-WithRetry -Context "Excel formula" -Action {
                    $ws.Cells.Item($f.R, 1) = "$($f.D):"
                    $ws.Cells.Item($f.R, 3).Formula = $f.F
                }

                WA "Формула: $($f.D)"
                Wait-Safe 0.25
            }

            Invoke-WithRetry -Context "Excel calculate" -Action {
                $script:Ctx.Excel.Calculate()
            }

            WA "Пересчёт выполнен"
        }
    },
    @{
        Name = "Сводная таблица (SUMIF)"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel raw data" -Action {
                $ws.Cells.Item(1, 1) = "Регион"
                $ws.Cells.Item(1, 2) = "Продажи"
                $ws.Cells.Item(1, 3) = "Квартал"

                $reg = @("Север", "Юг", "Запад", "Восток")
                $qs = @("Q1", "Q2", "Q3", "Q4")

                for ($i = 0; $i -lt 12; $i++) {
                    $ws.Cells.Item($i + 2, 1) = (Pick-Random $reg)
                    $ws.Cells.Item($i + 2, 2) = (Rnd 50000 250000)
                    $ws.Cells.Item($i + 2, 3) = (Pick-Random $qs)
                }
            }

            WA "Сырые данные записаны"
            Wait-Safe 0.4

            Invoke-WithRetry -Context "Excel SUMIF" -Action {
                $ws.Cells.Item(1, 5) = "Регион"
                $ws.Cells.Item(1, 6) = "Сумма"

                $reg = @("Север", "Юг", "Запад", "Восток")

                for ($i = 0; $i -lt $reg.Count; $i++) {
                    $ws.Cells.Item($i + 2, 5) = $reg[$i]
                    $ws.Cells.Item($i + 2, 6).Formula = "=SUMIF(A2:A13,E$($i + 2),B2:B13)"
                }

                $script:Ctx.Excel.Calculate()
                $ws.Columns.Item("A:F").AutoFit() | Out-Null
            }

            WA "SUMIF по регионам готов"
        }
    },
    @{
        Name = "Автофильтр и данные"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel filter data" -Action {
                $ws.Cells.Item(1, 1) = "Менеджер"
                $ws.Cells.Item(1, 2) = "Сумма"
                $ws.Cells.Item(1, 3) = "Статус"

                for ($i = 0; $i -lt 7; $i++) {
                    $ws.Cells.Item($i + 2, 1) = "Менеджер $($i + 1)"
                    $ws.Cells.Item($i + 2, 2) = (Rnd 50000 200000)
                    $ws.Cells.Item($i + 2, 3) = (Pick-Random @('OK', 'Hold', 'Review'))
                }

                $ws.Range("A1:C8").AutoFilter() | Out-Null
            }

            WA "Excel: автофильтр добавлен"
        }
    },
    @{
        Name = "Комментарий к ячейке"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel comment" -Action {
                $cell = $ws.Cells.Item(2, 2)
                $cell.Value2 = (Rnd 1000 9999)

                try {
                    $cell.AddComment("Проверить это значение")
                } catch {}
            }

            WA "Excel: комментарий к ячейке добавлен"
        }
    },
    @{
        Name = "Новый лист"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'ribbon'

            $newWs = Invoke-WithRetry -Context "Excel add sheet" -Action {
                $script:Ctx.ExcelWb.Worksheets.Add()
            }

            Invoke-WithRetry -Context "Excel rename sheet" -Action {
                $newWs.Name = "Лист_" + (Get-Date -Format 'HHmmssfff')
                $newWs.Cells.Item(1, 1) = "Создано симулятором"
            }

            WA "Excel: новый лист создан"
        }
    },
    @{
        Name = "Числовые форматы"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel number formats" -Action {
                for ($i = 1; $i -le 6; $i++) {
                    $ws.Cells.Item($i, 1) = "Показатель $i"
                    $ws.Cells.Item($i, 2) = (Rnd -50000 150000) / 10.0
                    $ws.Cells.Item($i, 2).NumberFormat = "#,##0.00;[Red]-#,##0.00"
                }

                $ws.Columns.Item("A:B").AutoFit() | Out-Null
            }

            WA "Excel: числовые форматы применены"
        }
    },
    @{
        Name = "Закрепление области"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'grid'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel freeze panes" -Action {
                $ws.Cells.Item(1, 1) = "Строка"
                $ws.Cells.Item(1, 2) = "Значение"

                for ($i = 2; $i -le 12; $i++) {
                    $ws.Cells.Item($i, 1) = "Показатель $($i - 1)"
                    $ws.Cells.Item($i, 2) = (Rnd 100 999)
                }

                $ws.Range("B2").Select() | Out-Null
                $script:Ctx.Excel.ActiveWindow.FreezePanes = $false
                $script:Ctx.Excel.ActiveWindow.FreezePanes = $true
            }

            WA "Excel: область закреплена"
        }
    },
    @{
        Name = "Защита и снятие защиты листа"
        Run  = {
            Ensure-Excel
            Move-MouseForTextInput 'ribbon'

            $ws = Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }

            Invoke-WithRetry -Context "Excel protect" -Action {
                $ws.Cells.Item(1, 1) = "Защищённая ячейка"
                $ws.Protect("Sim123")
            }

            Wait-Safe 0.35

            Invoke-WithRetry -Context "Excel unprotect" -Action {
                $ws.Unprotect("Sim123")
            }

            WA "Excel: защита листа добавлена и снята"
        }
    }
)

# ============ Сценарии Word ============
$script:WordScenarios = @(
    @{
        Name = "Служебная записка с таблицей"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word memo" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                $sel.Style = $script:wdStyleHeading1
                $sel.TypeText("Служебная записка от $(Get-Date -Format 'dd.MM.yyyy')")
                $sel.TypeParagraph()

                $sel.Style = $script:wdStyleNormal
                $sel.TypeText("Направляю сводку по продажам.")
                $sel.TypeParagraph()

                $tbl = $script:Ctx.WordDoc.Tables.Add($sel.Range, 4, 3)
                $tbl.Cell(1, 1).Range.Text = "Менеджер"
                $tbl.Cell(1, 2).Range.Text = "Сумма"
                $tbl.Cell(1, 3).Range.Text = "План"

                $nm = @("Иванов", "Петрова", "Сидоров")

                for ($i = 0; $i -lt 3; $i++) {
                    $tbl.Cell($i + 2, 1).Range.Text = $nm[$i]
                    $tbl.Cell($i + 2, 2).Range.Text = "$((Rnd 200000 500000))"
                    $tbl.Cell($i + 2, 3).Range.Text = "$((Rnd 80 130))%"
                }

                $tbl.Rows.Item(1).Range.Font.Bold = $true
                $tbl.Rows.Item(1).Shading.BackgroundPatternColor = 15773696
            }

            WA "Записка с таблицей создана"
        }
    },
    @{
        Name = "Список задач"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word task list" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                $sel.Style = $script:wdStyleHeading2
                $sel.TypeText("План на день")
                $sel.TypeParagraph()

                $sel.Style = $script:wdStyleNormal

                foreach ($t in @("Проверить отчёт", "Ответить на письма", "Обновить документацию", "Созвон в 15:00", "Подготовить презентацию")) {
                    $sel.TypeText("• $t")
                    $sel.TypeParagraph()
                }
            }

            WA "Список задач создан"
        }
    },
    @{
        Name = "Поиск и замена"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word text for replace" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()
                $sel.TypeText("Отчёт за первый квартал. Первый квартал был успешным. Первый квартал завершён.")
            }

            WA "Текст для замены добавлен"
            Wait-Safe 0.3

            Invoke-WithRetry -Context "Word find 1" -MaxRetries 30 -DelayMs 500 -Action {
                $script:Ctx.WordDoc.Content.Find.Execute(
                    "первый квартал", $false, $false, $false, $false, $false,
                    $true, 1, $false, "I квартал", 2
                ) | Out-Null
            }

            WA "Замена: первый квартал -> I квартал"

            Invoke-WithRetry -Context "Word find 2" -MaxRetries 30 -DelayMs 500 -Action {
                $script:Ctx.WordDoc.Content.Find.Execute(
                    "успешным", $false, $false, $false, $false, $false,
                    $true, 1, $false, "очень успешным", 2
                ) | Out-Null
            }

            WA "Замена: успешным -> очень успешным"
        }
    },
    @{
        Name = "Форматирование"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word formatting" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                $sel.TypeText("ВАЖНОЕ ОБЪЯВЛЕНИЕ: совещание в 16:00.")
                $sel.HomeKey(5) | Out-Null
                $sel.EndKey(5, $true) | Out-Null

                $sel.Font.Bold = $true
                $sel.Font.Size = 14
                $sel.Font.Color = 255
            }

            WA "Форматирование применено"
            Wait-Safe 0.3

            Invoke-WithRetry -Context "Word normal paragraph" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                $sel.TypeText("Подтвердите участие.")
                $sel.Font.Bold = $false
                $sel.Font.Size = 11
                $sel.Font.Color = 0
            }

            WA "Обычный абзац добавлен"
        }
    },
    @{
        Name = "Быстрые абзацы"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word quick paragraphs" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                for ($i = 1; $i -le 4; $i++) {
                    $sel.TypeText("Абзац $i. Текст сгенерирован симулятором.")
                    $sel.TypeParagraph()
                }
            }

            WA "Word: добавлены быстрые абзацы"
        }
    },
    @{
        Name = "Ориентация страницы"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'ribbon'

            Invoke-WithRetry -Context "Word landscape" -MaxRetries 30 -DelayMs 500 -Action {
                $script:Ctx.WordDoc.PageSetup.Orientation = 1
            }

            Wait-Safe 0.35

            Invoke-WithRetry -Context "Word portrait" -MaxRetries 30 -DelayMs 500 -Action {
                $script:Ctx.WordDoc.PageSetup.Orientation = 0
            }

            WA "Word: ориентация страницы изменена и возвращена"
        }
    },
    @{
        Name = "Гиперссылка"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word hyperlink" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()
                $sel.TypeText("Ссылка: ")

                $script:Ctx.WordDoc.Hyperlinks.Add(
                    $sel.Range,
                    "https://example.com",
                    $null,
                    "Пример"
                ) | Out-Null
            }

            WA "Word: гиперссылка добавлена"
        }
    },
    @{
        Name = "Дата и время"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word datetime" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()
                $sel.TypeText("Документ обновлён: $(Get-Date -Format 'dd.MM.yyyy HH:mm:ss')")
                $sel.TypeParagraph()
            }

            WA "Word: дата и время вставлены"
        }
    },
    @{
        Name = "Вставка таблицы 3x3"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'text'

            Invoke-WithRetry -Context "Word table 3x3" -MaxRetries 30 -DelayMs 500 -Action {
                $sel = $script:Ctx.Word.Selection
                $sel.EndKey(6) | Out-Null
                $sel.TypeParagraph()

                $tbl = $script:Ctx.WordDoc.Tables.Add($sel.Range, 3, 3)

                for ($r = 1; $r -le 3; $r++) {
                    for ($c = 1; $c -le 3; $c++) {
                        $tbl.Cell($r, $c).Range.Text = "Ячейка $r-$c"
                    }
                }

                $tbl.Borders.Enable = $true
            }

            WA "Word: таблица 3x3 добавлена"
        }
    },
    @{
        Name = "Верхний колонтитул"
        Run  = {
            Ensure-Word
            Move-MouseForTextInput 'ribbon'

            Invoke-WithRetry -Context "Word header" -MaxRetries 30 -DelayMs 500 -Action {
                $script:Ctx.WordDoc.Sections.Item(1).Headers.Item(1).Range.Text = "Симулятор рабочего дня"
            }

            WA "Word: верхний колонтитул изменён"
        }
    }
)

# ============ Сценарии VS Code ============
$script:VSCodeScenarios = @(
    @{
        Name = "Функция обработки данных"
        Run  = {
            Ensure-VSCode

            Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @'

function Process-SalesData {
    param([array]$Rows)

    $result = @()

    foreach ($row in $Rows) {
        $total = $row.Q1 + $row.Q2 + $row.Q3
        $avg = [math]::Round($total / 3, 2)

        $result += [PSCustomObject]@{
            Manager = $row.Name
            Total   = $total
            Average = $avg
        }
    }

    return $result
}
'@

            WA "Функция Process-SalesData добавлена"
            Start-Process -FilePath $script:VSCodeCommand.Source -ArgumentList "`"$($script:Ctx.VSCodeFile)`""
            Wait-Safe 0.8
            [void](Focus-App @('Code', 'Code - Insiders') -WaitMs 400)
        }
    },
    @{
        Name = "Класс ReportBuilder"
        Run  = {
            Ensure-VSCode

            Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @'

class ReportBuilder {
    [string]$Title
    [array]$Items

    ReportBuilder([string]$t) {
        $this.Title = $t
        $this.Items = @()
    }

    [void]AddItem([string]$n, [int]$v) {
        $this.Items += [PSCustomObject]@{ Name = $n; Value = $v }
    }

    [int]GetTotal() {
        $s = 0
        foreach ($i in $this.Items) { $s += $i.Value }
        return $s
    }
}
'@

            WA "Класс ReportBuilder добавлен"
            Start-Process -FilePath $script:VSCodeCommand.Source -ArgumentList "`"$($script:Ctx.VSCodeFile)`""
            Wait-Safe 0.8
            [void](Focus-App @('Code', 'Code - Insiders') -WaitMs 400)
        }
    },
    @{
        Name = "TODO/FIXME комментарии"
        Run  = {
            Ensure-VSCode

            Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @"

# TODO: добавить валидацию входных данных
# TODO: вынести константы в отдельный файл
# FIXME: обработка пустого массива
"@

            WA "TODO/FIXME комментарии добавлены"
            Start-Process -FilePath $script:VSCodeCommand.Source -ArgumentList "`"$($script:Ctx.VSCodeFile)`""
            Wait-Safe 0.8
            [void](Focus-App @('Code', 'Code - Insiders') -WaitMs 400)
        }
    },
    @{
        Name = "Markdown заметка"
        Run  = {
            $file = Join-Path $script:WorkDir "note.md"

            @"
# Заметка $(Get-Date -Format 'yyyy-MM-dd HH:mm')

## Задачи
- Проверить данные
- Обновить отчёт
- Подготовить статус

## Случайное значение
$((Rnd 100 999))
"@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: Markdown заметка открыта"
        }
    },
    @{
        Name = "JavaScript snippet"
        Run  = {
            $file = Join-Path $script:WorkDir "snippet.js"

            @'
function calculateTotal(items) {
    let total = 0;

    for (const item of items) {
        total += item.price * item.qty;
    }

    return total;
}

console.log(calculateTotal([
    { price: 100, qty: 2 },
    { price: 50, qty: 4 }
]));
'@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: JavaScript snippet открыт"
        }
    },
    @{
        Name = "Python snippet"
        Run  = {
            $file = Join-Path $script:WorkDir "snippet.py"

            @'
def calculate_average(values):
    if not values:
        return 0
    return sum(values) / len(values)

numbers = [10, 20, 30, 40]
print(calculate_average(numbers))
'@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: Python snippet открыт"
        }
    },
    @{
        Name = "CSS snippet"
        Run  = {
            $file = Join-Path $script:WorkDir "style.css"

            @'
.card {
    border: 1px solid #d0d7e2;
    border-radius: 8px;
    padding: 16px;
    background: #ffffff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.card-title {
    font-weight: 600;
    margin-bottom: 8px;
}
'@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: CSS snippet открыт"
        }
    },
    @{
        Name = ".gitignore"
        Run  = {
            $file = Join-Path $script:WorkDir ".gitignore"

            @'
node_modules/
dist/
temp/
*.log
.env
'@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: .gitignore открыт"
        }
    },
    @{
        Name = "Dockerfile"
        Run  = {
            $file = Join-Path $script:WorkDir "Dockerfile"

            @'
FROM mcr.microsoft.com/powershell:latest

WORKDIR /app
COPY . .

CMD ["pwsh", "./script.ps1"]
'@ | Set-Content -Path $file -Encoding UTF8

            Open-VSCodeFile $file
            WA "VS Code: Dockerfile открыт"
        }
    }
)

# ============ Сценарии Notepad++ ============
$script:NotepadPlusScenarios = @(
    @{
        Name = "TODO список"
        Run  = {
            Ensure-NotepadPlus

            $file = Join-Path $script:WorkDir "TODO.md"

            $content = @"
# TODO $(Get-Date -Format 'yyyy-MM-dd HH:mm')

- [ ] Проверить отчёт
- [ ] Обновить документацию
- [ ] Подготовить письмо команде
- [ ] Проверить задачи в трекере
- [ ] Сделать резервную копию файлов

Случайное значение: $((Rnd 100 999))
"@

            Set-Content -Path $file -Value $content -Encoding UTF8
            Open-NotepadPlusFile $file
            WA "TODO.md создан/обновлён"
        }
    },
    @{
        Name = "CSV файл"
        Run  = {
            Ensure-NotepadPlus

            $file = Join-Path $script:WorkDir "data.csv"

            $lines = @("Manager,Amount,Status")

            foreach ($name in @("Иванов", "Петрова", "Сидоров", "Козлова")) {
                $amount = Rnd 50000 250000
                $status = Pick-Random @("OK", "Pending", "Review")
                $lines += "$name,$amount,$status"
            }

            $lines | Set-Content -Path $file -Encoding UTF8
            Open-NotepadPlusFile $file
            WA "CSV файл создан"
        }
    },
    @{
        Name = "JSON конфиг"
        Run  = {
            Ensure-NotepadPlus

            $file = Join-Path $script:WorkDir "config.json"

            $json = @"
{
  "generated": "$(Get-Date -Format 's')",
  "retries": $(Rnd 1 5),
  "timeoutMs": $(Rnd 100 900),
  "enableLogging": true,
  "mode": "$(Pick-Random @('demo','test','prod'))"
}
"@

            Set-Content -Path $file -Value $json -Encoding UTF8
            Open-NotepadPlusFile $file
            WA "JSON конфиг создан"
        }
    },
    @{
        Name = "Лог-файл"
        Run  = {
            Ensure-NotepadPlus

            $file = Join-Path $script:WorkDir "app.log"

            if (-not (Test-Path $file)) {
                New-Item -ItemType File -Path $file | Out-Null
            }

            for ($i = 0; $i -lt 5; $i++) {
                $level = Pick-Random @("INFO", "WARN", "DEBUG", "ERROR")
                $msg = Pick-Random @(
                    "Проверка данных завершена",
                    "Ожидание ответа сервиса",
                    "Файл успешно обработан",
                    "Повторное подключение",
                    "Обновление кэша",
                    "Проверка прав доступа"
                )

                $line = "[{0:yyyy-MM-dd HH:mm:ss}] [{1}] {2}" -f (Get-Date), $level, $msg
                Add-Content -Path $file -Value $line -Encoding UTF8
                Wait-Safe 0.15
            }

            Open-NotepadPlusFile $file
            WA "Лог-файл пополнен"
        }
    },
    @{
        Name = "INI файл"
        Run  = {
            $file = Join-Path $script:WorkDir "settings.ini"

            @"
[general]
mode = $(Pick-Random @('demo','test','prod'))
retries = $(Rnd 1 5)
timeout_ms = $(Rnd 100 900)

[logging]
level = $(Pick-Random @('INFO','DEBUG','WARN'))
file = app.log
"@ | Set-Content -Path $file -Encoding UTF8

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'
            WA "Notepad++: INI файл создан"
        }
    },
    @{
        Name = "XML файл"
        Run  = {
            $file = Join-Path $script:WorkDir "data.xml"

            @"
<?xml version="1.0" encoding="utf-8"?>
<report>
  <item id="1">
    <name>Отчёт</name>
    <value>$((Rnd 1000 9999))</value>
  </item>
  <item id="2">
    <name>Проверка</name>
    <value>$((Rnd 1000 9999))</value>
  </item>
</report>
"@ | Set-Content -Path $file -Encoding UTF8

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'
            WA "Notepad++: XML файл создан"
        }
    },
    @{
        Name = "SQL скрипт"
        Run  = {
            $file = Join-Path $script:WorkDir "query.sql"

            @"
-- Симулятор запроса
SELECT
    id,
    name,
    amount,
    created_at
FROM sales
WHERE amount > $((Rnd 10000 100000))
ORDER BY amount DESC;
"@ | Set-Content -Path $file -Encoding UTF8

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'
            WA "Notepad++: SQL скрипт создан"
        }
    },
    @{
        Name = "Печать текста"
        Run  = {
            $file = Join-Path $script:WorkDir "typing.txt"

            if (-not (Test-Path $file)) {
                Set-Content -Path $file -Value "Файл для печати.`r`n" -Encoding UTF8
            }

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'

            Send-TextSafe "Симулятор напечатал строку $(Rnd 100 999)" -Enter

            WA "Notepad++: файл открыт, при включенном AllowSendKeys выполняется печать"
        }
    },
    @{
        Name = "YAML файл"
        Run  = {
            $file = Join-Path $script:WorkDir "config.yaml"

            @"
app:
  name: SimWork
  mode: $(Pick-Random @('demo','test','prod'))
  retries: $(Rnd 1 5)
  timeoutMs: $(Rnd 100 900)
logging:
  level: $(Pick-Random @('INFO','DEBUG','WARN'))
"@ | Set-Content -Path $file -Encoding UTF8

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'

            WA "Notepad++: YAML файл создан"
        }
    },
    @{
        Name = "Batch файл"
        Run  = {
            $file = Join-Path $script:WorkDir "demo.bat"

            @"
@echo off
echo SimWork batch demo
set /a A=$(Rnd 1 20)
set /a B=$(Rnd 1 20)
set /a SUM=A+B
echo SUM=%SUM%
"@ | Set-Content -Path $file -Encoding ASCII

            Open-NotepadPlusFile $file
            Move-MouseForTextInput 'text'

            WA "Notepad++: Batch файл создан"
        }
    }
)

# ============ Сценарии CMD ============
$script:CmdScenarios = @(
    @{
        Name = "Быстрая диагностика"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'ver & hostname & whoami & date /t & time /t' -Description "CMD quick info"
            WA "CMD диагностика выполнена"
        }
    },
    @{
        Name = "Просмотр TEMP"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'dir /b "%TEMP%"' -Description "CMD dir TEMP"
            WA "CMD: список временных файлов получен"
        }
    },
    @{
        Name = "Сетевой статус"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'ipconfig | findstr IPv4' -Description "CMD ipconfig"
            WA "CMD: сетевой статус запрошен"
        }
    },
    @{
        Name = "Batch математика"
        Run  = {
            $bat = Join-Path $script:WorkDir "math_demo.bat"

            $a = Rnd 10 99
            $b = Rnd 10 99

            @"
@echo off
set /a A=$a
set /a B=$b
set /a SUM=A+B
set /a MUL=A*B
echo A=%A% B=%B% SUM=%SUM% MUL=%MUL%
"@ | Set-Content -Path $bat -Encoding ASCII

            $null = Invoke-CmdSim -Arguments "`"$bat`"" -Description "CMD batch math"
            WA "CMD batch выполнен"
        }
    },
    @{
        Name = "Видимое окно CMD"
        Run  = {
            $ticks = Rnd 2 4

            Start-Process -FilePath $env:ComSpec `
                -ArgumentList '/c', "title SimWork CMD && echo Имитация CMD && ping -n $ticks 127.0.0.1 >nul && exit" `
                -WindowStyle Normal

            Wait-Safe 0.3
            [void](Focus-App @('cmd', 'WindowsTerminal', 'conhost') -WaitMs 400)

            WA "Открыто окно CMD примерно на $ticks сек."
        }
    },
    @{
        Name = "Переменные окружения"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'set COMPUTERNAME & set USERNAME' -Description "CMD env"
            WA "CMD: переменные окружения запрошены"
        }
    },
    @{
        Name = "Количество процессов"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'tasklist /nh | find /c /v ""' -Description "CMD process count"
            WA "CMD: количество процессов получено"
        }
    },
    @{
        Name = "Цикл echo"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'for /L %i in (1,1,3) do @echo iteration %i' -Description "CMD loop"
            WA "CMD: цикл echo выполнен"
        }
    },
    @{
        Name = "Видимый ввод в CMD"
        Run  = {
            if ($AllowSendKeys) {
                Start-Process -FilePath $env:ComSpec -ArgumentList '/k', 'title SimWork CMD'
                Wait-Safe 0.6

                [void](Focus-App @('cmd', 'WindowsTerminal', 'conhost') -WaitMs 400)
                Move-MouseForTextInput 'terminal'

                Send-TextSafe "echo simulated input $(Rnd 100 999)" -Enter
                Send-TextSafe "exit" -Enter

                WA "CMD: выполнен видимый ввод"
            } else {
                $null = Invoke-CmdSim -Arguments 'echo simulated input' -Description "CMD input"
                WA "CMD: ввод без SendKeys выполнен скрыто"
            }
        }
    },
    @{
        Name = "Переменная PATH"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'echo %PATH%' -Description "CMD PATH"
            WA "CMD: PATH выведен"
        }
    },
    @{
        Name = "Doskey macros"
        Run  = {
            $null = Invoke-CmdSim -Arguments 'doskey /macros' -Description "CMD doskey"
            WA "CMD: doskey macros запрошены"
        }
    }
)

# ============ Сценарии PowerShell ============
$script:PowerShellScenarios = @(
    @{
        Name = "Сводка процессов"
        Run  = {
            $code = @'
Get-Process |
    Sort-Object CPU -Descending |
    Select-Object -First 5 Name, Id, CPU |
    Format-Table -AutoSize |
    Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell process summary"
            WA "PowerShell: сводка процессов получена"
        }
    },
    @{
        Name = "Математика"
        Run  = {
            $a = Rnd 10 99
            $b = Rnd 10 99

            $code = @(
                '$a = ' + $a,
                '$b = ' + $b,
                'Write-Host ("a+b=$($a+$b)")',
                'Write-Host ("a*b=$($a*$b)")'
            ) -join "`r`n"

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell math"
            WA "PowerShell: математика выполнена"
        }
    },
    @{
        Name = "Модуль помощник"
        Run  = {
            $psm = Join-Path $script:WorkDir "Helpers.psm1"

            @'
function Convert-ToUpper {
    param([string]$Text)
    return $Text.ToUpper()
}

function Get-Timestamp {
    return (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    Write-Host "[$(Get-Timestamp)] [$Level] $Message"
}

Export-ModuleMember -Function Convert-ToUpper, Get-Timestamp, Write-Log
'@ | Set-Content -Path $psm -Encoding UTF8

            $code = "Import-Module '$psm' -Force; Write-Log 'PowerShell scenario test' 'DEBUG'; Convert-ToUpper 'hello'"

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell module"
            WA "PowerShell: модуль протестирован"
        }
    },
    @{
        Name = "Диски и свободное место"
        Run  = {
            $code = @'
Get-PSDrive -PSProvider FileSystem |
    Select-Object Name, Used, Free |
    Format-Table -AutoSize |
    Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell disks"
            WA "PowerShell: информация по дискам получена"
        }
    },
    @{
        Name = "Сводка служб"
        Run  = {
            $code = @'
Get-Service |
    Group-Object Status |
    Select-Object Name, Count |
    Format-Table -AutoSize |
    Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell services"
            WA "PowerShell: сводка служб получена"
        }
    },
    @{
        Name = "Переменные окружения"
        Run  = {
            $code = @'
Get-ChildItem Env: |
    Select-Object -First 10 |
    Format-Table -AutoSize |
    Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell env"
            WA "PowerShell: переменные окружения получены"
        }
    },
    @{
        Name = "Ping localhost"
        Run  = {
            $code = @'
Test-Connection -ComputerName 127.0.0.1 -Count 2 | Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell ping"
            WA "PowerShell: ping localhost выполнен"
        }
    },
    @{
        Name = "Региональные настройки"
        Run  = {
            $code = @'
Get-Culture | Format-List | Out-String
'@

            $null = Invoke-PowerShellScriptSim -ScriptContent $code -Description "PowerShell culture"
            WA "PowerShell: региональные настройки получены"
        }
    }
)

# ============ Сценарии Browser ============
$script:BrowserScenarios = @(
    @{
        Name = "HTML отчёт"
        Run  = {
            $body = @"
<table>
<tr><th>Менеджер</th><th>Продажи</th></tr>
<tr><td>Иванов</td><td>$((Rnd 100000 250000))</td></tr>
<tr><td>Петрова</td><td>$((Rnd 100000 250000))</td></tr>
<tr><td>Сидоров</td><td>$((Rnd 100000 250000))</td></tr>
</table>
"@

            $path = New-SimHtmlFile -Title "Отчёт $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -BodyHtml $body
            Open-BrowserFile $path
            WA "HTML отчёт открыт в браузере"
        }
    },
    @{
        Name = "Страница времени"
        Run  = {
            $body = @"
<p>Текущее время: <b>$(Get-Date -Format 'HH:mm:ss')</b></p>
<p>Случайное значение: <b>$((Rnd 1 1000))</b></p>
"@

            $path = New-SimHtmlFile -Title "Timestamp demo" -BodyHtml $body
            Open-BrowserFile $path
            WA "Открыта страница с временем"
        }
    },
    @{
        Name = "Список задач"
        Run  = {
            $items = @(
                "Проверить почту",
                "Обновить отчёт",
                "Позвонить клиенту",
                "Проверить задачи",
                "Подготовить статус"
            )

            $body = "<ul>"
            foreach ($i in $items) {
                $body += "<li>$i</li>"
            }
            $body += "</ul>"

            $path = New-SimHtmlFile -Title "План работы" -BodyHtml $body
            Open-BrowserFile $path
            WA "Открыт список задач в браузере"
        }
    },
    @{
        Name = "Форма"
        Run  = {
            $body = @"
<form>
  <p><label>Имя</label><br><input type="text" placeholder="Введите имя"></p>
  <p><label>Email</label><br><input type="email" placeholder="user@example.com"></p>
  <p><label>Комментарий</label><br><textarea rows="4" cols="40"></textarea></p>
  <p><button type="button">Отправить</button></p>
</form>
"@

            $path = New-SimHtmlFile -Title "Форма" -BodyHtml $body
            Open-BrowserFile $path
            Move-MouseForTextInput 'browser'

            WA "Браузер: открыта локальная форма"
        }
    },
    @{
        Name = "CSS карточки"
        Run  = {
            $body = @"
<style>
.cards { display: flex; gap: 12px; flex-wrap: wrap; }
.card { border: 1px solid #d0d7e2; border-radius: 8px; padding: 16px; width: 180px; background: white; }
.card b { display: block; margin-bottom: 6px; }
</style>
<div class="cards">
  <div class="card"><b>Отчёт</b><span>$((Rnd 100 999))</span></div>
  <div class="card"><b>Задачи</b><span>$((Rnd 1 20))</span></div>
  <div class="card"><b>Письма</b><span>$((Rnd 1 50))</span></div>
</div>
"@

            $path = New-SimHtmlFile -Title "CSS карточки" -BodyHtml $body
            Open-BrowserFile $path
            Move-MouseForTextInput 'browser'

            WA "Браузер: открыты CSS карточки"
        }
    },
    @{
        Name = "JSON просмотр"
        Run  = {
            $body = @"
<pre>
{
  "time": "$(Get-Date -Format 's')",
  "value": $((Rnd 1 1000)),
  "status": "$(Pick-Random @('ok','pending','error'))"
}
</pre>
"@

            $path = New-SimHtmlFile -Title "JSON" -BodyHtml $body
            Open-BrowserFile $path
            Move-MouseForTextInput 'browser'

            WA "Браузер: открыт JSON"
        }
    },
    @{
        Name = "Несколько вкладок"
        Run  = {
            $file1 = New-SimHtmlFile -Title "Вкладка 1" -BodyHtml "<p>Первая тестовая страница.</p>"
            $file2 = New-SimHtmlFile -Title "Вкладка 2" -BodyHtml "<p>Вторая тестовая страница.</p>"

            $uris = @($file1, $file2) | ForEach-Object {
                "file:///" + ($_ -replace '\\', '/')
            }

            if ($script:BrowserExe) {
                Start-Process -FilePath $script:BrowserExe -ArgumentList $uris
            } else {
                Invoke-Item $file1
                Invoke-Item $file2
            }

            Wait-Safe 1.0
            [void](Focus-App @('msedge', 'chrome', 'firefox', 'brave') -WaitMs 700)
            Move-MouseForTextInput 'browser'

            WA "Браузер: открыто несколько страниц"
        }
    }
)

# ============ Сценарии Explorer ============
$script:ExplorerScenarios = @(
    @{
        Name = "Открыть рабочую папку"
        Run  = {
            Open-ExplorerTarget $script:WorkDir
            WA "Explorer: рабочая папка открыта"
        }
    },
    @{
        Name = "Открыть Этот компьютер"
        Run  = {
            Open-ExplorerTarget "shell:MyComputerFolder"
            WA "Explorer: открыт 'Этот компьютер'"
        }
    },
    @{
        Name = "Открыть загрузки"
        Run  = {
            Open-ExplorerTarget "shell:DownloadsFolder"
            WA "Explorer: открыта папка загрузок"
        }
    },
    @{
        Name = "Создать папку"
        Run  = {
            $dir = Join-Path $script:WorkDir ("Folder_" + (Rnd 1000 9999))
            New-Item -ItemType Directory -Path $dir -Force | Out-Null

            Open-ExplorerTarget $dir
            Move-MouseForTextInput 'browser'

            WA "Explorer: папка создана и открыта"
        }
    },
    @{
        Name = "Создать текстовый файл"
        Run  = {
            $file = Join-Path $script:WorkDir ("file_" + (Rnd 1000 9999) + ".txt")
            Set-Content -Path $file -Value "Создано симулятором: $(Get-Date)" -Encoding UTF8

            Open-ExplorerTarget (Split-Path $file)
            Move-MouseForTextInput 'browser'

            WA "Explorer: текстовый файл создан"
        }
    },
    @{
        Name = "Открыть шрифты"
        Run  = {
            Open-ExplorerTarget 'shell:FontsFolder'
            Move-MouseForTextInput 'browser'

            WA "Explorer: открыта папка шрифтов"
        }
    },
    @{
        Name = "Поиск в папке"
        Run  = {
            $query = [uri]::EscapeDataString('txt')
            $location = [uri]::EscapeDataString($script:WorkDir)

            $uri = "search-ms:query=$query&crumb=location:$location"

            Start-Process explorer.exe -ArgumentList "`"$uri`""

            Wait-Safe 0.8
            [void](Focus-App @('explorer') -WaitMs 400)
            Move-MouseForTextInput 'browser'

            WA "Explorer: открыт поиск в рабочей папке"
        }
    },
    @{
        Name = "Копирование файла"
        Run  = {
            $src = Join-Path $script:WorkDir "copy_source.txt"
            $dst = Join-Path $script:WorkDir ("copy_" + (Get-Date -Format 'HHmmssfff') + ".txt")

            Set-Content -Path $src -Value "Исходный файл" -Encoding UTF8
            Copy-Item -Path $src -Destination $dst -Force

            Open-ExplorerTarget (Split-Path $dst)
            Move-MouseForTextInput 'browser'

            WA "Explorer: файл скопирован"
        }
    },
    @{
        Name = "Структура папок"
        Run  = {
            $root = Join-Path $script:WorkDir ("DemoStructure_" + (Get-Date -Format 'HHmmssfff'))

            New-Item -ItemType Directory -Path (Join-Path $root 'A\B\C') -Force | Out-Null
            New-Item -ItemType File -Path (Join-Path $root 'A\B\C\file.txt') -Force | Out-Null

            Open-ExplorerTarget $root
            Move-MouseForTextInput 'browser'

            WA "Explorer: создана структура папок"
        }
    }
)

# ============ Сценарии Outlook ============
$script:OutlookScenarios = @(
    @{
        Name = "Черновик письма"
        Run  = {
            Move-MouseForTextInput 'text'

            $path = Invoke-OutlookItemAction -Extension '.msg' -SaveAsFormat 4 -Action {
                param($ol)

                $mail = $ol.CreateItem(0)
                $mail.Subject = "Симулятор: тестовое письмо $(Get-Date -Format 'HH:mm:ss')"
                $mail.Body = "Это тестовый черновик, созданный симулятором.`r`nПисьмо не отправляется."

                $mail
            }

            WA "Outlook: черновик письма сохранён: $path"
        }
    },
    @{
        Name = "Встреча"
        Run  = {
            Move-MouseForTextInput 'text'

            $path = Invoke-OutlookItemAction -Extension '.ics' -SaveAsFormat 8 -Action {
                param($ol)

                $appt = $ol.CreateItem(1)
                $appt.Subject = "Симулятор: встреча"
                $appt.Start = (Get-Date).AddHours(1)
                $appt.Duration = 30
                $appt.Location = "Переговорная"
                $appt.Body = "Встреча создана симулятором."

                $appt
            }

            WA "Outlook: встреча сохранена: $path"
        }
    },
    @{
        Name = "Задача"
        Run  = {
            Move-MouseForTextInput 'text'

            $path = Invoke-OutlookItemAction -Extension '.msg' -SaveAsFormat 4 -Action {
                param($ol)

                $task = $ol.CreateItem(3)
                $task.Subject = "Симулятор: задача"
                $task.DueDate = (Get-Date).AddDays(1)
                $task.Body = "Задача создана симулятором."

                $task
            }

            WA "Outlook: задача сохранена: $path"
        }
    },
    @{
        Name = "Контакт"
        Run  = {
            Move-MouseForTextInput 'text'

            $path = Invoke-OutlookItemAction -Extension '.vcf' -SaveAsFormat 3 -Action {
                param($ol)

                $contact = $ol.CreateItem(2)
                $contact.FullName = "Симулятор Тестовый"
                $contact.Email1Address = "simwork@example.com"
                $contact.MobileTelephoneNumber = "+7 900 000-00-00"

                $contact
            }

            WA "Outlook: контакт сохранён: $path"
        }
    }
)

# ============ Сценарии PowerPoint ============
$script:PowerPointScenarios = @(
    @{
        Name = "Титульный слайд"
        Run  = {
            Move-MouseForTextInput 'ribbon'

            $path = Invoke-PowerPointAction -Description "PowerPoint title" -Action {
                param($app, $pres)

                $slide = $pres.Slides.Add(1, 1)

                try {
                    $slide.Shapes.Title.TextFrame.TextRange.Text = "Отчёт $(Get-Date -Format 'dd.MM.yyyy')"
                } catch {}

                $box = $slide.Shapes.AddTextbox(1, 60, 180, 600, 100)
                $box.TextFrame.TextRange.Text = "Создано симулятором рабочего дня."
            }

            WA "PowerPoint: титульный слайд создан: $path"
        }
    },
    @{
        Name = "Несколько слайдов"
        Run  = {
            Move-MouseForTextInput 'ribbon'

            $path = Invoke-PowerPointAction -Description "PowerPoint slides" -Action {
                param($app, $pres)

                for ($i = 1; $i -le 3; $i++) {
                    $slide = $pres.Slides.Add($i, 12)

                    $titleBox = $slide.Shapes.AddTextbox(1, 40, 30, 700, 60)
                    $titleBox.TextFrame.TextRange.Text = "Слайд $i"

                    $bodyBox = $slide.Shapes.AddTextbox(1, 60, 120, 650, 200)
                    $bodyBox.TextFrame.TextRange.Text = "Содержимое слайда $i.`r`nСлучайное значение: $((Rnd 100 999))"
                }
            }

            WA "PowerPoint: создано 3 слайда: $path"
        }
    },
    @{
        Name = "Слайд с заметкой"
        Run  = {
            Move-MouseForTextInput 'ribbon'

            $path = Invoke-PowerPointAction -Description "PowerPoint notes" -Action {
                param($app, $pres)

                $slide = $pres.Slides.Add(1, 12)

                $box = $slide.Shapes.AddTextbox(1, 60, 100, 600, 100)
                $box.TextFrame.TextRange.Text = "Слайд с заметкой."

                try {
                    $slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = "Заметка для докладчика."
                } catch {}
            }

            WA "PowerPoint: слайд с заметкой создан: $path"
        }
    }
)

# ============ Сценарии Windows Terminal ============
$script:TerminalScenarios = @(
    @{
        Name = "Открыть Windows Terminal"
        Run  = {
            if (-not $script:TerminalCommand) {
                throw "Windows Terminal не найден."
            }

            Start-Process -FilePath $script:TerminalCommand.Source

            Wait-Safe 0.7
            [void](Focus-App @('WindowsTerminal', 'wt') -WaitMs 500)
            Move-MouseForTextInput 'terminal'

            WA "Windows Terminal открыт"
        }
    },
    @{
        Name = "Терминал с командой"
        Run  = {
            if (-not $script:TerminalCommand) {
                throw "Windows Terminal не найден."
            }

            Start-Process -FilePath $script:TerminalCommand.Source -ArgumentList 'cmd', '/c', 'echo SimWork terminal && timeout /t 2'

            Wait-Safe 0.7
            [void](Focus-App @('WindowsTerminal', 'wt') -WaitMs 500)
            Move-MouseForTextInput 'terminal'

            WA "Windows Terminal выполнен с командой"
        }
    },
    @{
        Name = "PowerShell в терминале"
        Run  = {
            if (-not $script:TerminalCommand) {
                throw "Windows Terminal не найден."
            }

            Start-Process -FilePath $script:TerminalCommand.Source -ArgumentList 'powershell', '-NoProfile', '-Command', 'Write-Host "SimWork PowerShell terminal"'

            Wait-Safe 0.7
            [void](Focus-App @('WindowsTerminal', 'wt') -WaitMs 500)
            Move-MouseForTextInput 'terminal'

            WA "Windows Terminal открыл PowerShell"
        }
    }
)

# ============ Сценарии Git ============
$script:GitScenarios = @(
    @{
        Name = "Git status"
        Run  = {
            Ensure-GitRepo
            $null = Invoke-GitSim -Arguments @('status', '--short') -Description "Git status"
            WA "Git: status выполнен"
        }
    },
    @{
        Name = "Git commit"
        Run  = {
            Ensure-GitRepo

            $file = Join-Path $script:GitRepoDir ("sim_" + (Get-Date -Format 'HHmmssfff') + ".txt")
            Set-Content -Path $file -Value "SimWork git demo" -Encoding UTF8

            $null = Invoke-GitSim -Arguments @('add', '.') -Description "Git add"
            $null = Invoke-GitSim -Arguments @('commit', '-m', "Sim commit $(Get-Date -Format 'HH:mm:ss')") -Description "Git commit"

            WA "Git: коммит создан"
        }
    },
    @{
        Name = "Git branch"
        Run  = {
            Ensure-GitRepo

            $branch = "feature-" + (Rnd 100 999)

            $null = Invoke-GitSim -Arguments @('branch', $branch) -Description "Git branch"
            $null = Invoke-GitSim -Arguments @('checkout', $branch) -Description "Git checkout"

            WA "Git: создана ветка $branch"
        }
    },
    @{
        Name = "Git log"
        Run  = {
            Ensure-GitRepo
            $null = Invoke-GitSim -Arguments @('log', '--oneline', '--decorate', '--max-count=5') -Description "Git log"
            WA "Git: log показан"
        }
    }
)

# ============ Сценарии 7-Zip ============
$script:SevenZipScenarios = @(
    @{
        Name = "Создать архив"
        Run  = {
            if (-not $script:SevenZipExe) {
                throw "7-Zip не найден."
            }

            $src = Join-Path $script:WorkDir "archive_demo.txt"
            Set-Content -Path $src -Value "SimWork 7-Zip demo" -Encoding UTF8

            $zip = Join-Path $script:WorkDir ("archive_" + (Get-Date -Format 'yyyyMMddHHmmssfff') + ".zip")

            $null = Invoke-SevenZipSim -Arguments @('a', $zip, $src) -Description "7-Zip create"

            WA "7-Zip: архив создан"
        }
    },
    @{
        Name = "Список файлов архива"
        Run  = {
            if (-not $script:SevenZipExe) {
                throw "7-Zip не найден."
            }

            $zip = Get-OrCreateTestZip
            $null = Invoke-SevenZipSim -Arguments @('l', $zip) -Description "7-Zip list"

            WA "7-Zip: список файлов архива получен"
        }
    },
    @{
        Name = "Тест архива"
        Run  = {
            if (-not $script:SevenZipExe) {
                throw "7-Zip не найден."
            }

            $zip = Get-OrCreateTestZip
            $null = Invoke-SevenZipSim -Arguments @('t', $zip) -Description "7-Zip test"

            WA "7-Zip: архив протестирован"
        }
    }
)

# ============ Сценарии Calculator ============
$script:CalculatorScenarios = @(
    @{
        Name = "Открыть калькулятор"
        Run  = {
            Open-Calculator
            WA "Калькулятор открыт"
        }
    },
    @{
        Name = "Простое вычисление"
        Run  = {
            Open-Calculator

            if ($AllowSendKeys) {
                Send-KeysRaw "123"
                Send-KeysRaw "{+}"
                Send-KeysRaw "456"
                Send-KeysRaw "="

                Wait-Safe 0.4
                WA "Калькулятор: выполнено 123+456"
            } else {
                WA "Калькулятор: для ввода включите -AllowSendKeys"
            }
        }
    },
    @{
        Name = "Случайное умножение"
        Run  = {
            Open-Calculator

            if ($AllowSendKeys) {
                $a = Rnd 10 99
                $b = Rnd 10 99

                Send-KeysRaw "$a"
                Send-KeysRaw "*"
                Send-KeysRaw "$b"
                Send-KeysRaw "="

                Wait-Safe 0.4
                WA "Калькулятор: выполнено $a*$b"
            } else {
                WA "Калькулятор: для ввода включите -AllowSendKeys"
            }
        }
    },
    @{
        Name = "Очистка калькулятора"
        Run  = {
            Open-Calculator

            if ($AllowSendKeys) {
                Send-KeysRaw "{ESC}"
                Wait-Safe 0.3
                WA "Калькулятор: очищен"
            } else {
                WA "Калькулятор: для очистки включите -AllowSendKeys"
            }
        }
    }
)

# ============ Сценарии Task Manager ============
$script:TaskManagerScenarios = @(
    @{
        Name = "Открыть диспетчер задач"
        Run  = {
            Start-Process taskmgr.exe

            Wait-Safe 0.8
            [void](Focus-AppByTitle @('Диспетчер задач', 'Task Manager') -WaitMs 500)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.25 0.75) -YRatio (RndDouble 0.25 0.75) -Jitter 30

            WA "Task Manager открыт"
        }
    },
    @{
        Name = "Движение по диспетчеру задач"
        Run  = {
            Start-Process taskmgr.exe

            Wait-Safe 0.8
            [void](Focus-AppByTitle @('Диспетчер задач', 'Task Manager') -WaitMs 500)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.15 0.85) -YRatio (RndDouble 0.15 0.85) -Jitter 40
            Wait-Safe 0.3
            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.15 0.85) -YRatio (RndDouble 0.15 0.85) -Jitter 40

            WA "Task Manager: курсор перемещён по окну"
        }
    }
)

# ============ Сценарии Event Viewer ============
$script:EventViewerScenarios = @(
    @{
        Name = "Открыть просмотр событий"
        Run  = {
            Start-Process eventvwr.msc

            Wait-Safe 1.0
            [void](Focus-AppByTitle @('Просмотр событий', 'Event Viewer') -WaitMs 600)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 35

            WA "Event Viewer открыт"
        }
    },
    @{
        Name = "Движение по просмотру событий"
        Run  = {
            Start-Process eventvwr.msc

            Wait-Safe 1.0
            [void](Focus-AppByTitle @('Просмотр событий', 'Event Viewer') -WaitMs 600)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.15 0.50) -YRatio (RndDouble 0.20 0.70) -Jitter 30
            Wait-Safe 0.3
            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.55 0.85) -YRatio (RndDouble 0.20 0.70) -Jitter 30

            WA "Event Viewer: курсор перемещён по панелям"
        }
    }
)

# ============ Сценарии System Tools ============
$script:SystemToolsScenarios = @(
    @{
        Name = "Панель управления"
        Run  = {
            Start-Process control.exe

            Wait-Safe 0.8
            [void](Focus-AppByTitle @('Панель управления', 'Control Panel') -WaitMs 500)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 30

            WA "Открыта панель управления"
        }
    },
    @{
        Name = "Параметры Windows"
        Run  = {
            Start-Process "ms-settings:"

            Wait-Safe 0.9
            [void](Focus-AppByTitle @('Параметры', 'Settings') -WaitMs 500)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 30

            WA "Открыты параметры Windows"
        }
    },
    @{
        Name = "Сведения о системе"
        Run  = {
            Start-Process msinfo32.exe

            Wait-Safe 1.2
            [void](Focus-AppByTitle @('Сведения о системе', 'System Information') -WaitMs 600)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 30

            WA "Открыты сведения о системе"
        }
    },
    @{
        Name = "Диспетчер устройств"
        Run  = {
            Start-Process devmgmt.msc

            Wait-Safe 1.0
            [void](Focus-AppByTitle @('Диспетчер устройств', 'Device Manager') -WaitMs 600)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 30

            WA "Открыт диспетчер устройств"
        }
    },
    @{
        Name = "Службы"
        Run  = {
            Start-Process services.msc

            Wait-Safe 1.0
            [void](Focus-AppByTitle @('Службы', 'Services') -WaitMs 600)

            Move-MouseToActiveWindowPoint -XRatio (RndDouble 0.20 0.80) -YRatio (RndDouble 0.20 0.80) -Jitter 30

            WA "Открыты службы Windows"
        }
    }
)

# ============ Пул приложений ============
$appPools = @{
    Excel       = $script:ExcelScenarios
    Word        = $script:WordScenarios
    VSCode      = $script:VSCodeScenarios
    NotepadPlus = $script:NotepadPlusScenarios
    Cmd         = $script:CmdScenarios
    PowerShell  = $script:PowerShellScenarios
    Browser     = $script:BrowserScenarios
    Explorer    = $script:ExplorerScenarios

    Outlook     = $script:OutlookScenarios
    PowerPoint  = $script:PowerPointScenarios
    Terminal    = $script:TerminalScenarios
    Git         = $script:GitScenarios
    SevenZip    = $script:SevenZipScenarios
    Calculator  = $script:CalculatorScenarios
    TaskManager = $script:TaskManagerScenarios
    EventViewer = $script:EventViewerScenarios
    SystemTools = $script:SystemToolsScenarios
}

# ============ Главный цикл ============
$lastApp = $null
$lastSc = $null
$iter = 0

Write-LogLine -Message ("=" * 60) -Color DarkGray
Write-LogLine -Message " Симулятор рабочего дня (полный)" -Color Green
Write-LogLine -Message (" Старт: {0:HH:mm:ss} | Дедлайн: {1:HH:mm:ss} ({2} сек.)" -f $script:StartTime, $script:Deadline, $script:TotalSeconds) -Color Green
Write-LogLine -Message (" Скорость: x{0}" -f $script:Speed) -Color Green
Write-LogLine -Message (" Лог: {0}" -f $script:LogFile) -Color Green
Write-LogLine -Message ("=" * 60) -Color DarkGray

try {
    while ($true) {
        Assert-TimeLeft -Reserve 5
        $iter++

        $availableApps = @($appPools.Keys | Where-Object { $script:AppEnabled[$_] })

        if ($availableApps.Count -eq 0) {
            throw "Нет доступных приложений для симуляции."
        }

        $cands = @($availableApps | Where-Object { $_ -ne $lastApp })
        if ($cands.Count -eq 0) { $cands = $availableApps }

        $app = Pick-Random $cands
        $pool = $appPools[$app]

        $scCands = @($pool | Where-Object { $_.Name -ne $lastSc })
        if ($scCands.Count -eq 0) { $scCands = $pool }

        $sc = Pick-Random $scCands

        Write-Host ""
        Write-LogLine -Message ("-" * 60) -Color DarkGray
        WS "Итерация #$iter | $app | '$($sc.Name)' | осталось $(LeftSec) сек."
        Write-LogLine -Message ("-" * 60) -Color DarkGray

        [void](Focus-App (Get-FocusNames $app) -WaitMs 350)

        try {
            & $sc.Run
            $lastApp = $app
            $lastSc = $sc.Name
        } catch {
            $msg = $_.Exception.Message

            if ($msg -match '^TIMEOUT|^STOPPED') {
                throw
            }

            Write-LogLine "Сценарий '$($sc.Name)' для $app завершился ошибкой: $msg" -Color Yellow -Indent 4

            if ($msg -match 'Class not registered|Cannot load COM type|не найден|not found|CommandNotFoundException|New-Object') {
                $script:AppEnabled[$app] = $false
                Write-LogLine "Приложение $app отключено из-за ошибки доступности." -Color Yellow -Indent 4
            }

            Wait-Safe 0.5
            continue
        }

        Wait-Safe 0.8
    }
}
catch {
    Write-Host ""
    Write-LogLine -Message ("!" * 60) -Color Yellow
    Write-LogLine -Message " Сценарий прерван: $($_.Exception.Message)" -Color Yellow
    Write-LogLine -Message " Выполнено итераций: $iter" -Color Yellow
    Write-LogLine -Message ("!" * 60) -Color Yellow
}
finally {
    Write-Host ""
    WS "Сохранение и уборка..."

    if ($script:Ctx.ExcelWb -and $script:Ctx.Excel) {
        try {
            Start-Sleep -Milliseconds (ScaleMs 1200)
            $rp = Join-Path $script:WorkDir "Workbook.xlsx"

            if (Test-Path $rp) {
                Remove-Item $rp -Force -ErrorAction SilentlyContinue
            }

            Invoke-WithRetry -Context "Excel.SaveAs" -Action {
                $path = [string]$rp
                $fmt = [int]51
                $script:Ctx.ExcelWb.SaveAs($path, $fmt)
            }

            WA "Excel сохранён: $rp"
        } catch {
            Write-Warning "Excel не сохранён: $_"
        }
    }

    if ($script:Ctx.WordDoc -and $script:Ctx.Word) {
        try {
            Start-Sleep -Milliseconds (ScaleMs 1200)
            $dp = Join-Path $script:WorkDir "Document.docx"

            if (Test-Path $dp) {
                Remove-Item $dp -Force -ErrorAction SilentlyContinue
            }

            Invoke-WithRetry -Context "Word.SaveAs" -MaxRetries 30 -DelayMs 500 -Action {
                $path = [string]$dp
                $fmt = [int]16
                $script:Ctx.WordDoc.SaveAs([ref]$path, [ref]$fmt)
            }

            WA "Word сохранён: $dp"
        } catch {
            Write-Warning "Word не сохранён: $_"
        }
    }

    foreach ($p in @(
        @{ O = $script:Ctx.ExcelWb; C = { param($o) $o.Close($false) } },
        @{ O = $script:Ctx.WordDoc; C = { param($o) $o.Close($false) } },
        @{ O = $script:Ctx.Excel;   C = { param($o) $o.Quit() } },
        @{ O = $script:Ctx.Word;    C = { param($o) $o.Quit() } }
    )) {
        if ($p.O) {
            try { & $p.C $p.O } catch {}
            try { [Runtime.InteropServices.Marshal]::ReleaseComObject($p.O) | Out-Null } catch {}
        }
    }

    if ($script:Ctx.ExcelChart) {
        try { [Runtime.InteropServices.Marshal]::ReleaseComObject($script:Ctx.ExcelChart) | Out-Null } catch {}
    }

    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    $el = (Get-Date) - $script:StartTime

    Write-Host ""
    Write-LogLine -Message ("=" * 60) -Color DarkGray
    Write-LogLine -Message (" Готово. Прошло: {0:hh\:mm\:ss}, итераций: {1}" -f $el, $iter) -Color Green
    Write-LogLine -Message (" Лимит: {0} сек." -f $script:TotalSeconds) -Color Green
    Write-LogLine -Message (" Скорость: x{0}" -f $script:Speed) -Color Green
    Write-LogLine -Message (" Лог: {0}" -f $script:LogFile) -Color Green
    Write-LogLine -Message ("=" * 60) -Color DarkGray
}
