# ============================================================
#  Симулятор рабочего дня (retry для COM)
#  Приложения: Excel, Word, VS Code, Notepad++
#  Запуск:
#    .\Simulate-Workday.ps1 -DurationMinutes 5
#    .\Simulate-Workday.ps1 -DurationSeconds 60 -Seed 42
#    .\Simulate-Workday.ps1 -DurationMinutes 10 -SpeedMultiplier 2.0
# ============================================================
[CmdletBinding()]
param(
    [int]$DurationMinutes=0,
    [int]$DurationSeconds=30,
    [int]$Seed=0,
    [double]$SpeedMultiplier=1.0,
    [int]$ActionDelayMs=400,
    [int]$StartupDelayMs=1500
)

$script:TotalSeconds = if ($DurationSeconds -gt 0) { $DurationSeconds } else { $DurationMinutes*60 }
if ($script:TotalSeconds -le 0) { throw "Длительность > 0" }
if ($SpeedMultiplier -le 0) { throw "SpeedMultiplier > 0" }
$script:SpeedMul = $SpeedMultiplier
$script:ActionDelay = [int]($ActionDelayMs / $script:SpeedMul)
$script:StartupDelay = [int]($StartupDelayMs / $script:SpeedMul)
$script:Random = if ($Seed -ne 0) { [System.Random]::new($Seed) } else { [System.Random]::new() }
$script:StartTime = Get-Date
$script:Deadline  = $script:StartTime.AddSeconds($script:TotalSeconds)
$script:Stopped   = $false

Write-Host ("="*60) -ForegroundColor DarkGray
Write-Host " Симулятор работы (rand, no C#, расширенный)" -ForegroundColor Green
Write-Host (" Старт: {0:HH:mm:ss} | Дедлайн: {1:HH:mm:ss} ({2} сек.)" -f $script:StartTime,$script:Deadline,$script:TotalSeconds)
Write-Host (" Скорость: x{0} | Действие: {1} мс | Старт: {2} мс" -f $script:SpeedMul,$script:ActionDelay,$script:StartupDelay)
Write-Host ("="*60) -ForegroundColor DarkGray

# ============ Хелперы ============
function WS { param($t) Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $t" -ForegroundColor Cyan }
function WA { param($t) Write-Host "    -> $t" -ForegroundColor DarkYellow }
function LeftSec { [int]([math]::Round(($script:Deadline-(Get-Date)).TotalSeconds)) }

function Assert-TimeLeft {
    param([int]$Reserve=0)
    if ($script:Stopped) { throw "Остановлен пользователем." }
    if ((Get-Date) -ge $script:Deadline.AddSeconds(-$Reserve)) {
        throw ($(if($Reserve){"Мало времени (запас $Reserve сек.)"}else{"Истекло время ($($script:TotalSeconds) сек.)"}))
    }
}

function Wait-Safe {
    param([double]$Seconds)
    $scaled = $Seconds / $script:SpeedMul
    $target=(Get-Date).AddSeconds($scaled)
    while ((Get-Date) -lt $target) {
        Assert-TimeLeft
        $t=($target-(Get-Date)).TotalMilliseconds
        $d=($script:Deadline-(Get-Date)).TotalMilliseconds
        $s=[math]::Min(200,[math]::Min($t,$d))
        if ($s -gt 0) { Start-Sleep -Milliseconds $s }
    }
}
function Wait-Action { Wait-Safe -Seconds ($script:ActionDelay/1000.0) }

function Invoke-WithRetry {
    param([scriptblock]$Action,[int]$MaxRetries=20,[int]$DelayMs=400,[string]$Context="COM")
    $n=0
    while ($true) {
        $n++
        try { return & $Action }
        catch {
            $m=$_.Exception.Message
            if (-not ($m -match "RPC_E_CALL_REJECTED|0x80010001|Вызов был отклонен|Call was rejected") -or $n -ge $MaxRetries) { throw }
            Write-Host "    [retry $n/$MaxRetries] $Context занят, ждём ${DelayMs}мс..." -ForegroundColor DarkGray
            Start-Sleep -Milliseconds $DelayMs
        }
    }
}

function Assert-NotNull { param($Obj,[string]$Name) if($null -eq $Obj){throw "Внутренняя ошибка: $Name = `$null"}; return $Obj }
function Get-AppProc { param($Name) Get-Process -Name $Name -EA SilentlyContinue | ? {$_.MainWindowHandle -ne 0} | Sort StartTime | Select -Last 1 }
function Focus-App {
    param($Name,[int]$WaitMs=500)
    $p=Get-AppProc $Name; if(-not $p){return $null}
    try { (New-Object -ComObject WScript.Shell).AppActivate($p.Id) | Out-Null } catch {}
    Start-Sleep -Milliseconds ([int]($WaitMs / $script:SpeedMul))
    return $p
}
function Rnd { param([int]$Min,[int]$Max) $script:Random.Next($Min,$Max) }
function Pick-Random { param([array]$Items) if(-not $Items -or $Items.Count -eq 0){return $null}; $Items[$script:Random.Next(0,$Items.Count)] }

# ============ Контекст ============
$script:Ctx = @{
    Excel=$null;ExcelWb=$null;ExcelWs=$null;ExcelChart=$null
    Word=$null;WordDoc=$null
    VSCodeFile=$null
    NppFile=$null;NppExe=$null
}

function Ensure-Excel {
    if ($script:Ctx.Excel -and $script:Ctx.ExcelWb -and $script:Ctx.ExcelWs) { return }
    $script:Ctx.Excel = New-Object -ComObject Excel.Application
    $script:Ctx.Excel.Visible=$true; $script:Ctx.Excel.DisplayAlerts=$false
    Wait-Safe 1.5; [void](Focus-App EXCEL -WaitMs 800)
    $script:Ctx.ExcelWb = Invoke-WithRetry -Context "Excel.Workbooks.Add" -Action { $script:Ctx.Excel.Workbooks.Add() }
    if($null -eq $script:Ctx.ExcelWb){throw "Excel: не удалось создать книгу"}
    $script:Ctx.ExcelWs = Invoke-WithRetry -Context "Excel.Worksheet" -Action { $script:Ctx.ExcelWb.Worksheets.Item(1) }
    if($null -eq $script:Ctx.ExcelWs){throw "Excel: не удалось получить лист"}
    WA "Excel: книга и лист созданы"
}
function Ensure-Word {
    if ($script:Ctx.Word -and $script:Ctx.WordDoc) { return }
    $script:Ctx.Word = New-Object -ComObject Word.Application
    $script:Ctx.Word.Visible=$true
    Wait-Safe 2.5; [void](Focus-App WINWORD -WaitMs 1000)
    $script:Ctx.WordDoc = Invoke-WithRetry -Context "Word.Documents.Add" -MaxRetries 30 -DelayMs 500 -Action { $script:Ctx.Word.Documents.Add() }
    if($null -eq $script:Ctx.WordDoc){throw "Word: не удалось создать документ"}
    $null = Invoke-WithRetry -Context "Word warm-up" -MaxRetries 30 -DelayMs 500 -Action { $s=$script:Ctx.Word.Selection; $null=$s.Start; $s }
    WA "Word: документ создан (готов)"
}
function Ensure-VSCode {
    $dir="$env:TEMP\SimWork"; if(-not(Test-Path $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
    if (-not $script:Ctx.VSCodeFile -or -not (Test-Path $script:Ctx.VSCodeFile)) {
        $script:Ctx.VSCodeFile = Join-Path $dir "Scratch.ps1"
        if(-not(Test-Path $script:Ctx.VSCodeFile)){"# Scratch.ps1`r`n# Рабочий файл`r`n"|Set-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8}
        WA "VS Code: создан Scratch.ps1"
    }
    Start-Process "code" -ArgumentList "`"$($script:Ctx.VSCodeFile)`""; Wait-Safe 2
    [void](Focus-App "Code" -WaitMs 800)
}
function Find-NotepadPP {
    $cands=@(
        "$env:ProgramFiles\Notepad++\notepad++.exe",
        "${env:ProgramFiles(x86)}\Notepad++\notepad++.exe",
        "$env:LOCALAPPDATA\Programs\Notepad++\notepad++.exe"
    )
    foreach($c in $cands){ if(Test-Path $c){ return $c } }
    $cmd=Get-Command notepad++.exe -EA SilentlyContinue
    if($cmd){ return $cmd.Source }
    return $null
}
function Ensure-NotepadPP {
    if (-not $script:Ctx.NppExe) {
        $script:Ctx.NppExe = Find-NotepadPP
        if (-not $script:Ctx.NppExe) { throw "Notepad++ не найден" }
        WA "Notepad++: $($script:Ctx.NppExe)"
    }
    $dir="$env:TEMP\SimWork"; if(-not(Test-Path $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
    if (-not $script:Ctx.NppFile -or -not (Test-Path $script:Ctx.NppFile)) {
        $script:Ctx.NppFile = Join-Path $dir "Note.txt"
        if(-not(Test-Path $script:Ctx.NppFile)){"Заметка $(Get-Date -Format 'yyyy-MM-dd')`r`n"|Set-Content -Path $script:Ctx.NppFile -Encoding UTF8}
        WA "Notepad++: создан Note.txt"
    }
    Start-Process $script:Ctx.NppExe -ArgumentList "`"$($script:Ctx.NppFile)`""
    Wait-Safe 1.5
    [void](Focus-App "notepad++" -WaitMs 600)
}

# ============ Сценарии Excel (10) ============
$script:ExcelScenarios = @(
    @{ Name="Квартальный отчёт с диаграммой"; Run={
        Ensure-Excel
        $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel header" -Action {
            $ws.Cells.Item(1,1)="Квартальный отчёт"; $ws.Range("A1:E1").Merge()
            $ws.Cells.Item(1,1).Font.Bold=$true; $ws.Cells.Item(1,1).Font.Size=14; $ws.Cells.Item(1,1).HorizontalAlignment=-4108
        }
        Wait-Action; WA "Заголовок записан"
        Invoke-WithRetry -Context "Excel hdr" -Action {
            $h=@("Менеджер","Янв","Фев","Мар","Итого")
            for($c=0;$c-lt 5;$c++){$ws.Cells.Item(3,$c+1)=$h[$c];$ws.Cells.Item(3,$c+1).Font.Bold=$true;$ws.Cells.Item(3,$c+1).Interior.Color=15773696}
        }
        $names=@("Иванов","Петрова","Сидоров","Козлова","Морозов")
        Invoke-WithRetry -Context "Excel data" -Action {
            for($r=0;$r-lt $names.Count;$r++){
                $ws.Cells.Item($r+4,1)=$names[$r]
                for($c=2;$c-le 4;$c++){$ws.Cells.Item($r+4,$c)=(Rnd 80000 200000)}
                $ws.Cells.Item($r+4,5).Formula="=SUM(B$($r+4):D$($r+4))"
            }
        }
        WA "5 менеджеров + SUM"; Wait-Action
        $last=3+$names.Count+1
        Invoke-WithRetry -Context "Excel total" -Action {
            $ws.Cells.Item($last,1)="ИТОГО"
            for($c=2;$c-le 5;$c++){
                $col=[char](64+$c); $ws.Cells.Item($last,$c).Formula="=SUM($col`4:$col$($last-1))"
                $ws.Cells.Item($last,$c).Font.Bold=$true; $ws.Cells.Item($last,$c).Interior.Color=13551615
            }
            $ws.Columns.Item("A:E").AutoFit()|Out-Null
        }
        WA "Итоговая строка"; Wait-Action
        Invoke-WithRetry -Context "Excel chart" -Action {
            $rng=$ws.Range("A3:E$($last-1)")
            $ch=$ws.Shapes.AddChart2(240,201)
            if($null -ne $ch){$ch.Chart.SetSourceData($rng);$ch.Chart.HasTitle=$true;$ch.Chart.ChartTitle.Text="Продажи";$script:Ctx.ExcelChart=$ch}
        }
        WA "Диаграмма построена"
    }},
    @{ Name="Добавление и удаление строк"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        $sr=Invoke-WithRetry -Context "Excel UsedRange" -Action { ($ws.UsedRange.Rows.Count)+2 }; if($sr-lt 4){$sr=4}
        $names=@("Новиков","Фёдорова","Белов")
        for($i=0;$i-lt 3;$i++){
            Invoke-WithRetry -Context "Excel add" -Action { $ws.Cells.Item($sr+$i,1)=$names[$i];$ws.Cells.Item($sr+$i,2)=(Rnd 50000 180000);$ws.Cells.Item($sr+$i,3)=(Rnd 50000 180000) }
            WA "Строка $($names[$i])"; Wait-Action
        }
        Invoke-WithRetry -Context "Excel del" -Action { $ws.Rows.Item($sr+1).Delete()|Out-Null }
        WA "Средняя строка удалена"; Wait-Action
        Invoke-WithRetry -Context "Excel ins" -Action { $ws.Rows.Item($sr).Insert(-4162)|Out-Null;$ws.Cells.Item($sr,1)="Вставлен";$ws.Cells.Item($sr,2)=123456 }
        WA "Строка вставлена"
    }},
    @{ Name="Формулы и вычисления"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        $xl=Invoke-WithRetry -Context "Excel app" -Action { $script:Ctx.Excel }
        Invoke-WithRetry -Context "Excel f" -Action {
            $ws.Cells.Item(1,1)="Формулы"; $ws.Cells.Item(1,1).Font.Bold=$true
            $ws.Cells.Item(3,1)="A";$ws.Cells.Item(3,2)="B";$ws.Cells.Item(3,3)="Результат"
            $ws.Cells.Item(4,1)=(Rnd 10 100);$ws.Cells.Item(4,2)=(Rnd 10 100)
        }
        $fs=@(@{R=4;F="=A4+B4";D="Сумма"},@{R=5;F="=A4-B4";D="Разность"},@{R=6;F="=A4*B4";D="Произведение"},@{R=7;F="=A4/B4";D="Деление"},@{R=8;F="=POWER(A4,2)";D="Квадрат"})
        foreach($f in $fs){
            Invoke-WithRetry -Context "Excel f" -Action { $ws.Cells.Item($f.R,3).Formula=$f.F;$ws.Cells.Item($f.R,1)="$($f.D):" }
            WA "Формула '$($f.D)'"; Wait-Action
        }
        Invoke-WithRetry -Context "Excel calc" -Action { $xl.Calculate() }
        WA "Пересчёт: сумма=$($ws.Cells.Item(4,3).Value2)"
    }},
    @{ Name="Сводная таблица (SUMIF)"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        $xl=Invoke-WithRetry -Context "Excel app" -Action { $script:Ctx.Excel }
        Invoke-WithRetry -Context "Excel raw" -Action {
            $ws.Cells.Item(1,1)="Регион";$ws.Cells.Item(1,2)="Продажи";$ws.Cells.Item(1,3)="Квартал"
            $reg=@("Север","Юг","Запад","Восток");$qs=@("Q1","Q2","Q3","Q4")
            for($i=0;$i-lt 12;$i++){
                $ws.Cells.Item($i+2,1)=(Pick-Random $reg);$ws.Cells.Item($i+2,2)=(Rnd 50000 250000);$ws.Cells.Item($i+2,3)=(Pick-Random $qs)
            }
        }
        WA "12 сырых строк"; Wait-Action
        Invoke-WithRetry -Context "Excel sumif" -Action {
            $ws.Cells.Item(1,5)="Регион";$ws.Cells.Item(1,6)="Сумма"
            $reg=@("Север","Юг","Запад","Восток")
            for($i=0;$i-lt $reg.Count;$i++){
                $ws.Cells.Item($i+2,5)=$reg[$i];$ws.Cells.Item($i+2,6).Formula="=SUMIF(A2:A13,E$($i+2),B2:B13)"
            }
            $xl.Calculate(); $ws.Columns.Item("A:F").AutoFit()|Out-Null
        }
        WA "SUMIF по регионам готов"
    }},
    @{ Name="Условное форматирование"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel cf" -Action {
            $ws.Cells.Item(1,1)="Метрика";$ws.Cells.Item(1,2)="Значение"
            for($i=0;$i-lt 8;$i++){$ws.Cells.Item($i+2,1)="Метрика $($i+1)";$ws.Cells.Item($i+2,2)=(Rnd 10 100)}
            $rng=$ws.Range("B2:B9")
            $rng.FormatConditions.AddColorScale(3)|Out-Null
            $rng.FormatConditions.AddIconSetCondition()|Out-Null
            $ws.Columns.Item("A:B").AutoFit()|Out-Null
        }
        WA "ColorScale + IconSet добавлены"
    }},
    @{ Name="Поиск и замена"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel fill" -Action {
            for($i=0;$i-lt 10;$i++){$ws.Cells.Item($i+1,1)="Старое_значение_$i";$ws.Cells.Item($i+1,2)=(Rnd 100 1000)}
        }
        WA "10 строк заполнено"
        Invoke-WithRetry -Context "Excel replace" -Action { $ws.Cells.Replace("Старое_значение","Новое_значение",-4162,1,$false)|Out-Null }
        WA "Replace выполнен"; Wait-Action
        Invoke-WithRetry -Context "Excel overwrite" -Action { for($i=0;$i-lt 10;$i++){if($i%2-eq 0){$ws.Cells.Item($i+1,1)="Чётная_строка"}} }
        WA "Часть ячеек перезаписана"
    }},
    @{ Name="Сортировка и фильтр"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel sort-data" -Action {
            $ws.Cells.Item(1,1)="Товар";$ws.Cells.Item(1,2)="Цена";$ws.Cells.Item(1,3)="Кол-во"
            $goods=@("Ноутбук","Мышь","Клавиатура","Монитор","Наушники","Веб-камера","Микрофон","Коврик")
            for($i=0;$i-lt $goods.Count;$i++){
                $ws.Cells.Item($i+2,1)=$goods[$i];$ws.Cells.Item($i+2,2)=(Rnd 500 50000);$ws.Cells.Item($i+2,3)=(Rnd 1 50)
            }
        }
        WA "8 товаров добавлено"; Wait-Action
        Invoke-WithRetry -Context "Excel sort" -Action {
            $rng=$ws.Range("A1:C9")
            $rng.Sort($ws.Range("B2"),1)  # xlAscending по цене
        }
        WA "Сортировка по цене (возрастание)"; Wait-Action
        Invoke-WithRetry -Context "Excel autofilter" -Action {
            $ws.Range("A1:C9").AutoFilter()|Out-Null
        }
        WA "Автофильтр включён"
    }},
    @{ Name="Несколько листов"; Run={
        Ensure-Excel; $wb=Invoke-WithRetry -Context "Excel wb" -Action { $script:Ctx.ExcelWb }
        foreach($name in @("Январь","Февраль","Март")){
            Invoke-WithRetry -Context "Excel addsheet" -Action {
                $new=$wb.Worksheets.Add()
                $new.Name=$name
                $new.Cells.Item(1,1)="Отчёт: $name"
                $new.Cells.Item(1,1).Font.Bold=$true
                for($i=0;$i-lt 5;$i++){
                    $new.Cells.Item($i+3,1)="Строка $($i+1)"; $new.Cells.Item($i+3,2)=(Rnd 10000 100000)
                }
            }
            WA "Лист '$name' создан"; Wait-Action
        }
        Invoke-WithRetry -Context "Excel activate" -Action { $wb.Worksheets.Item("Февраль").Activate() }
        WA "Активирован лист 'Февраль'"
    }},
    @{ Name="Объединение ячеек и перенос"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel merge" -Action {
            $ws.Cells.Item(1,1)="Большой заголовок в несколько строк"
            $ws.Range("A1:D1").Merge()
            $ws.Range("A1").WrapText=$true
            $ws.Rows.Item(1).RowHeight=45
            $ws.Cells.Item(1,1).Font.Size=16; $ws.Cells.Item(1,1).Font.Bold=$true
            $ws.Cells.Item(1,1).HorizontalAlignment=-4108
            $ws.Cells.Item(1,1).VerticalAlignment=-4108
            $ws.Range("A1:D1").Interior.Color=13551615
        }
        WA "A1:D1 объединено, перенос текста, высота 45"
        Invoke-WithRetry -Context "Excel merge2" -Action {
            for($i=0;$i-lt 4;$i++){
                $ws.Cells.Item($i+3,1)="Группа $($i+1)"
                $ws.Cells.Item($i+3,2)=(Rnd 100 500)
                $ws.Cells.Item($i+3,3)=(Rnd 100 500)
            }
        }
        WA "Добавлено 4 группы данных"
    }},
    @{ Name="Диаграмма-круговая"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel pie-data" -Action {
            $ws.Cells.Item(1,1)="Категория";$ws.Cells.Item(1,2)="Доля"
            $cats=@("Электроника","Одежда","Продукты","Книги","Спорт")
            for($i=0;$i-lt $cats.Count;$i++){
                $ws.Cells.Item($i+2,1)=$cats[$i];$ws.Cells.Item($i+2,2)=(Rnd 10 100)
            }
            $ws.Columns.Item("A:B").AutoFit()|Out-Null
        }
        WA "5 категорий добавлено"; Wait-Action
        Invoke-WithRetry -Context "Excel pie" -Action {
            $rng=$ws.Range("A1:B6")
            $ch=$ws.Shapes.AddChart2(251,5)  # xlPie
            if($null -ne $ch){
                $ch.Chart.SetSourceData($rng)
                $ch.Chart.HasTitle=$true;$ch.Chart.ChartTitle.Text="Доли категорий"
                $script:Ctx.ExcelChart=$ch
            }
        }
        WA "Круговая диаграмма построена"
    }},
    @{ Name="Гистограмма по месяцам"; Run={
        Ensure-Excel; $ws=Invoke-WithRetry -Context "Excel ws" -Action { $script:Ctx.ExcelWs }
        Invoke-WithRetry -Context "Excel bar-data" -Action {
            $ws.Cells.Item(1,1)="Месяц";$ws.Cells.Item(1,2)="Продажи"
            $months=@("Янв","Фев","Мар","Апр","Май","Июн")
            for($i=0;$i-lt 6;$i++){
                $ws.Cells.Item($i+2,1)=$months[$i];$ws.Cells.Item($i+2,2)=(Rnd 50000 200000)
            }
            $ws.Columns.Item("A:B").AutoFit()|Out-Null
        }
        WA "6 месяцев добавлено"; Wait-Action
        Invoke-WithRetry -Context "Excel bar" -Action {
            $rng=$ws.Range("A1:B7")
            $ch=$ws.Shapes.AddChart2(286,201)  # xlColumnClustered
            if($null -ne $ch){
                $ch.Chart.SetSourceData($rng)
                $ch.Chart.HasTitle=$true;$ch.Chart.ChartTitle.Text="Продажи по месяцам"
                $script:Ctx.ExcelChart=$ch
            }
        }
        WA "Гистограмма построена"
    }}
)

# ============ Сценарии Word (10) ============
$script:WordScenarios = @(
    @{ Name="Служебная записка с таблицей"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word memo" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$doc=$script:Ctx.WordDoc
            $sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.Style="Заголовок 1";$sel.TypeText("Служебная записка от $(Get-Date -Format 'dd.MM.yyyy')");$sel.TypeParagraph()
            $sel.Style="Обычный";$sel.TypeText("Направляю сводку по продажам.");$sel.TypeParagraph()
            $tbl=$doc.Tables.Add($sel.Range,4,3)
            $tbl.Cell(1,1).Range.Text="Менеджер";$tbl.Cell(1,2).Range.Text="Сумма";$tbl.Cell(1,3).Range.Text="План"
            $nm=@("Иванов","Петрова","Сидоров")
            for($i=0;$i-lt 3;$i++){$tbl.Cell($i+2,1).Range.Text=$nm[$i];$tbl.Cell($i+2,2).Range.Text="$((Rnd 200000 500000))";$tbl.Cell($i+2,3).Range.Text="$((Rnd 80 130))%"}
            $tbl.Rows.Item(1).Range.Font.Bold=$true;$tbl.Rows.Item(1).Shading.BackgroundPatternColor=15773696
        }
        WA "Записка с таблицей создана"
    }},
    @{ Name="Список задач"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word list" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection
            $sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.Style="Заголовок 2";$sel.TypeText("План на день");$sel.TypeParagraph()
            $sel.Style="Список"
            foreach($t in @("Проверить отчёт","Ответить на письма","Обновить документацию","Созвон в 15:00","Подготовить презентацию")){
                $sel.TypeText($t);$sel.TypeParagraph()
            }
            $sel.Style="Обычный"
        }
        WA "Список из 5 задач"
    }},
    @{ Name="Вставка/удаление абзацев"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word add" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$sel.EndKey(6)|Out-Null
            for($i=0;$i-lt 5;$i++){$sel.TypeParagraph();$sel.TypeText("Временный абзац $($i+1).")}
        }
        WA "5 абзацев добавлено";Wait-Action
        Invoke-WithRetry -Context "Word del" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$sel.EndKey(6)|Out-Null
            $sel.HomeKey(5)|Out-Null;$sel.EndKey(5,$true)|Out-Null;$sel.Delete()|Out-Null
        }
        WA "Последний абзац удалён"
        Invoke-WithRetry -Context "Word del2" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection
            $sel.HomeKey(5)|Out-Null;$sel.EndKey(5,$true)|Out-Null;$sel.Delete()|Out-Null
        }
        WA "Ещё один абзац удалён"
    }},
    @{ Name="Поиск и замена"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word text" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.TypeText("Отчёт за первый квартал. Первый квартал был успешным. Первый квартал завершён.")
        }
        WA "Текст с 3 вхождениями";Wait-Action
        Invoke-WithRetry -Context "Word find1" -MaxRetries 30 -DelayMs 500 -Action {
            $script:Ctx.WordDoc.Content.Find.Execute("первый квартал",$false,$false,$false,$false,$false,$true,1,$false,"I квартал",2)|Out-Null
        }
        WA "первый квартал -> I квартал"
        Invoke-WithRetry -Context "Word find2" -MaxRetries 30 -DelayMs 500 -Action {
            $script:Ctx.WordDoc.Content.Find.Execute("успешным",$false,$false,$false,$false,$false,$true,1,$false,"очень успешным",2)|Out-Null
        }
        WA "успешным -> очень успешным"
    }},
    @{ Name="Форматирование"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word fmt" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.TypeText("ВАЖНОЕ ОБЪЯВЛЕНИЕ: совещание в 16:00.")
            $sel.HomeKey(5)|Out-Null;$sel.EndKey(5,$true)|Out-Null
            $sel.Font.Bold=$true;$sel.Font.Size=14;$sel.Font.Color=255
        }
        WA "Жирный, 14pt, красный";Wait-Action
        Invoke-WithRetry -Context "Word fmt2" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.TypeText("Подтвердите участие.");$sel.Font.Bold=$false;$sel.Font.Size=11;$sel.Font.Color=0
        }
        WA "Обычный абзац добавлен"
    }},
    @{ Name="Оглавление и разрывы"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word toc" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$doc=$script:Ctx.WordDoc
            $sel.EndKey(6)|Out-Null
            for($s=1;$s-le 3;$s++){
                $sel.Style="Заголовок 1";$sel.TypeText("Раздел $s");$sel.TypeParagraph()
                $sel.Style="Обычный";$sel.TypeText("Содержимое раздела $s.");$sel.TypeParagraph()
                if($s-lt 3){$sel.InsertBreak(7)|Out-Null}
            }
            $sel.HomeKey(6)|Out-Null
            $doc.TablesOfContents.Add($doc.Range(0,0),$true,1,3)|Out-Null
        }
        WA "3 раздела + оглавление"
    }},
    @{ Name="Многоуровневый список"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word multi-list" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection
            $sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.Style="Заголовок 1";$sel.TypeText("Структура проекта");$sel.TypeParagraph()
            $sel.Style="Обычный"
            $structure=@(
                @{Lvl=0;Text="Этап 1: Анализ"},
                @{Lvl=1;Text="Сбор требований"},
                @{Lvl=1;Text="Интервью с заказчиком"},
                @{Lvl=0;Text="Этап 2: Разработка"},
                @{Lvl=1;Text="Проектирование"},
                @{Lvl=1;Text="Реализация"},
                @{Lvl=2;Text="Модуль A"},
                @{Lvl=2;Text="Модуль B"},
                @{Lvl=0;Text="Этап 3: Тестирование"}
            )
            foreach($item in $structure){
                $sel.ParagraphFormat.LeftIndent = $item.Lvl * 18
                $prefix = if($item.Lvl -eq 0){"• "}elseif($item.Lvl -eq 1){"  ○ "}else{"    ▪ "}
                $sel.TypeText("$prefix$($item.Text)");$sel.TypeParagraph()
            }
            $sel.ParagraphFormat.LeftIndent = 0
        }
        WA "Многоуровневый список (3 уровня)"
    }},
    @{ Name="Вставка изображения (фигура)"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word shape" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection
            $sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.Style="Заголовок 2";$sel.TypeText("Диаграмма процесса");$sel.TypeParagraph()
            $sel.Style="Обычный"
            $doc=$script:Ctx.WordDoc
            $sh1=$doc.Shapes.AddShape(1,50,50,100,50)  # msoShapeRectangle
            $sh1.TextFrame.TextRange.Text="Начало"
            $sh2=$doc.Shapes.AddShape(1,200,50,100,50)
            $sh2.TextFrame.TextRange.Text="Процесс"
            $sh3=$doc.Shapes.AddShape(1,350,50,100,50)
            $sh3.TextFrame.TextRange.Text="Конец"
        }
        WA "3 фигуры с подписями добавлены"
    }},
    @{ Name="Таблица с итогами"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word sum-table" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection;$doc=$script:Ctx.WordDoc
            $sel.EndKey(6)|Out-Null;$sel.TypeParagraph()
            $sel.Style="Заголовок 2";$sel.TypeText("Смета расходов");$sel.TypeParagraph()
            $sel.Style="Обычный"
            $tbl=$doc.Tables.Add($sel.Range,6,3)
            $tbl.Cell(1,1).Range.Text="Статья";$tbl.Cell(1,2).Range.Text="Сумма";$tbl.Cell(1,3).Range.Text="Примечание"
            $items=@(
                @("Оборудование",150000,"Закупка"),
                @("ПО",80000,"Лицензии"),
                @("Обучение",45000,"Курсы"),
                @("Командировки",60000,"Поездки")
            )
            for($i=0;$i-lt 4;$i++){$tbl.Cell($i+2,1).Range.Text=$items[$i][0];$tbl.Cell($i+2,2).Range.Text="$($items[$i][1])";$tbl.Cell($i+2,3).Range.Text=$items[$i][2]}
            $tbl.Cell(6,1).Range.Text="ИТОГО"
            $tbl.Cell(6,2).Range.Text="335 000"
            $tbl.Cell(6,3).Range.Text="—"
            $tbl.Rows.Item(1).Range.Font.Bold=$true;$tbl.Rows.Item(6).Range.Font.Bold=$true
            $tbl.Rows.Item(1).Shading.BackgroundPatternColor=15773696
            $tbl.Rows.Item(6).Shading.BackgroundPatternColor=13551615
        }
        WA "Таблица сметы с итоговой строкой"
    }},
    @{ Name="Разные стили заголовков"; Run={
        Ensure-Word
        Invoke-WithRetry -Context "Word styles" -MaxRetries 30 -DelayMs 500 -Action {
            $sel=$script:Ctx.Word.Selection
            $sel.EndKey(6)|Out-Null
            $levels=@(@{S="Заголовок 1";T="Глава 1: Введение"},@{S="Заголовок 2";T="1.1 Цели"},@{S="Заголовок 3";T="1.1.1 Подцель"},@{S="Заголовок 1";T="Глава 2: Методы"},@{S="Заголовок 2";T="2.1 Обзор"})
            foreach($l in $levels){
                $sel.TypeParagraph()
                $sel.Style=$l.S
                $sel.TypeText($l.T)
            }
            $sel.TypeParagraph();$sel.Style="Обычный"
            $sel.TypeText("Документ со всеми уровнями заголовков.")
        }
        WA "5 заголовков разного уровня"
    }}
)

# ============ Сценарии VS Code (10) ============
$script:VSCodeScenarios = @(
    @{ Name="Функция обработки данных"; Run={
        Ensure-VSCode
        Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @'

function Process-SalesData {
    param([array]$Rows)
    $r=@(); foreach($row in $Rows){ $r += [PSCustomObject]@{ M=$row.Name; T=($row.Q1+$row.Q2+$row.Q3); A=[math]::Round(($row.Q1+$row.Q2+$row.Q3)/3,2) } }
    return $r
}
'@
        WA "Process-SalesData добавлена";Start-Process "code" -ArgumentList "`"$($script:Ctx.VSCodeFile)`"";Wait-Action;[void](Focus-App "Code" -WaitMs 500)
    }},
    @{ Name="Класс ReportBuilder"; Run={
        Ensure-VSCode
        Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @'

class ReportBuilder {
    [string]$Title; [array]$Items
    ReportBuilder([string]$t){$this.Title=$t;$this.Items=@()}
    [void]AddItem([string]$n,[int]$v){$this.Items += [PSCustomObject]@{Name=$n;Value=$v}}
    [int]GetTotal(){ $s=0; foreach($i in $this.Items){$s+=$i.Value}; return $s }
}
'@
        WA "Класс добавлен";Start-Process "code" -ArgumentList "`"$($script:Ctx.VSCodeFile)`"";Wait-Action;[void](Focus-App "Code" -WaitMs 500)
    }},
    @{ Name="Запуск скрипта"; Run={
        $dir="$env:TEMP\SimWork";if(-not(Test-Path $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
        $rf=Join-Path $dir "RunDemo.ps1";$n1=(Rnd 10 50);$n2=(Rnd 10 50)
        @"
`$a=$n1; `$b=$n2
Write-Host "a+b=`$(`$a+`$b)"
Write-Host "a*b=`$(`$a*`$b)"
Write-Host "a^2=`$([math]::Pow(`$a,2))"
"@ | Set-Content -Path $rf -Encoding UTF8
        WA "RunDemo.ps1 (a=$n1,b=$n2)";Start-Process "code" -ArgumentList "`"$rf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
        WA "Запуск скрипта...";$out=& powershell -NoProfile -ExecutionPolicy Bypass -File $rf 2>&1;foreach($l in $out){WA "output: $l"}
    }},
    @{ Name="TODO/FIXME комментарии"; Run={
        Ensure-VSCode
        Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @"

# TODO: добавить валидацию
# TODO: вынести константы
# FIXME: обработка пустого массива
"@
        WA "Комментарии добавлены";Start-Process "code" -ArgumentList "`"$($script:Ctx.VSCodeFile)`"";Wait-Action;[void](Focus-App "Code" -WaitMs 500)
    }},
    @{ Name="Модуль Helpers.psm1"; Run={
        $dir="$env:TEMP\SimWork";$mf=Join-Path $dir "Helpers.psm1"
        @'
function Convert-ToUpper { param([string]$Text) return $Text.ToUpper() }
function Get-Timestamp { return (Get-Date).ToString("yyyy-MM-dd HH:mm:ss") }
function Write-Log {
    param([string]$Message,[string]$Level="INFO")
    Write-Host "[$(Get-Timestamp)] [$Level] $Message"
}
Export-ModuleMember -Function Convert-ToUpper, Get-Timestamp, Write-Log
'@ | Set-Content -Path $mf -Encoding UTF8
        WA "Helpers.psm1 (3 функции)";Start-Process "code" -ArgumentList "`"$mf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
        WA "Импорт и тест...";$out=& powershell -NoProfile -Command "Import-Module '$mf' -Force; Write-Log 'test' 'DEBUG'; Convert-ToUpper 'hello'" 2>&1;foreach($l in $out){WA "output: $l"}
    }},
    @{ Name="HTML/CSS заготовка"; Run={
        $dir="$env:TEMP\SimWork";$hf=Join-Path $dir "index.html";$title="Отчёт $(Get-Date -Format 'yyyy-MM-dd')"
        @"
<!DOCTYPE html><html><head><meta charset="utf-8"><title>$title</title>
<style>body{font-family:Segoe UI,sans-serif;margin:40px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccc;padding:8px}th{background:#e0f0ff}</style>
</head><body><h1>$title</h1>
<table><tr><th>Менеджер</th><th>Продажи</th></tr>
<tr><td>Иванов</td><td>$((Rnd 100000 200000))</td></tr>
<tr><td>Петрова</td><td>$((Rnd 100000 200000))</td></tr></table></body></html>
"@ | Set-Content -Path $hf -Encoding UTF8
        WA "index.html создан";Start-Process "code" -ArgumentList "`"$hf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
    }},
    @{ Name="JSON-конфигурация"; Run={
        $dir="$env:TEMP\SimWork";$jf=Join-Path $dir "config.json"
        $obj=@{
            app=@{name="SimWorker";version="1.$(Rnd 0 9).$(Rnd 0 99)";debug=$false}
            server=@{host="localhost";port=(Rnd 8000 9000)}
            logging=@{level="INFO";file="app.log";rotate=$true}
        }
        $obj|ConvertTo-Json -Depth 5|Set-Content -Path $jf -Encoding UTF8
        WA "config.json создан";Start-Process "code" -ArgumentList "`"$jf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
    }},
    @{ Name="Юнит-тест (Pester-стиль)"; Run={
        $dir="$env:TEMP\SimWork";$tf=Join-Path $dir "Tests.ps1"
        @'
Describe "Calculator" {
    It "adds two numbers" {
        (2 + 3) | Should -Be 5
    }
    It "multiplies" {
        (4 * 5) | Should -Be 20
    }
    It "handles strings" {
        ("hello".ToUpper()) | Should -Be "HELLO"
    }
}
'@ | Set-Content -Path $tf -Encoding UTF8
        WA "Tests.ps1 с 3 тестами";Start-Process "code" -ArgumentList "`"$tf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
    }},
    @{ Name="Обработка ошибок (try/catch)"; Run={
        Ensure-VSCode
        Add-Content -Path $script:Ctx.VSCodeFile -Encoding UTF8 -Value @'

function Safe-Divide {
    param([int]$A, [int]$B)
    try {
        if ($B -eq 0) { throw "Division by zero" }
        return $A / $B
    } catch {
        Write-Warning "Ошибка: $($_.Exception.Message)"
        return $null
    } finally {
        Write-Host "Safe-Divide завершён"
    }
}
'@
        WA "Safe-Divide с try/catch/finally";Start-Process "code" -ArgumentList "`"$($script:Ctx.VSCodeFile)`"";Wait-Action;[void](Focus-App "Code" -WaitMs 500)
    }},
    @{ Name="CSV-парсер"; Run={
        $dir="$env:TEMP\SimWork";$cf=Join-Path $dir "Data.csv"
        "Имя,Возраст,Город"
        for($i=0;$i-lt 10;$i++){
            $names=@("Анна","Борис","Виктор","Галина","Дмитрий","Елена","Жанна","Игорь","Ксения","Леонид")
            $cities=@("Москва","СПб","Казань","Новосибирск","Екатеринбург")
            Add-Content -Path $cf -Value "$($names[$i]),$((Rnd 18 65)),$((Pick-Random $cities))" -Encoding UTF8
        }
        WA "Data.csv (10 записей)";Start-Process "code" -ArgumentList "`"$cf`"";Wait-Safe 1.5;[void](Focus-App "Code" -WaitMs 600)
    }}
)

# ============ Сценарии Notepad++ (8) ============
$script:NppScenarios = @(
    @{ Name="Быстрая заметка"; Run={
        Ensure-NotepadPP
        $txt=@"

=== Заметка от $(Get-Date -Format 'dd.MM.yyyy HH:mm') ===
- Проверить почту
- Ответить клиенту
- Подготовить отчёт
- Созвон с командой
"@
        Add-Content -Path $script:Ctx.NppFile -Value $txt -Encoding UTF8
        WA "Заметка добавлена в Note.txt";Wait-Action
        Start-Process $script:Ctx.NppExe -ArgumentList "`"$($script:Ctx.NppFile)`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="Конфигурационный файл"; Run={
        Ensure-NotepadPP
        $cfg=Join-Path "$env:TEMP\SimWork" "config_$(Rnd 1000 9999).ini"
        @"
[app]
name = SimWorker
version = 1.$(Rnd 0 20).$(Rnd 0 99)
debug = false

[server]
host = 127.0.0.1
port = $(Rnd 8000 9000)

[logging]
level = INFO
file = app.log
"@ | Set-Content -Path $cfg -Encoding UTF8
        WA "Создан $((Split-Path $cfg -Leaf))";Start-Process $script:Ctx.NppExe -ArgumentList "`"$cfg`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="Лог-файл"; Run={
        Ensure-NotepadPP
        $log=Join-Path "$env:TEMP\SimWork" "app.log"
        for($i=0;$i-lt 10;$i++){
            $lvl=Pick-Random @("INFO","WARN","ERROR","DEBUG")
            $ts=(Get-Date).AddSeconds(-($i*7)).ToString("yyyy-MM-dd HH:mm:ss")
            Add-Content -Path $log -Value "[$ts] [$lvl] Message $($i+1): operation completed" -Encoding UTF8
        }
        WA "Добавлено 10 строк лога";Start-Process $script:Ctx.NppExe -ArgumentList "`"$log`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="Поиск и замена"; Run={
        Ensure-NotepadPP
        $tf=Join-Path "$env:TEMP\SimWork" "replace_demo.txt"
        "Старое слово раз. Старое слово два. Старое слово три."|Set-Content -Path $tf -Encoding UTF8
        WA "Создан replace_demo.txt"
        Start-Process $script:Ctx.NppExe -ArgumentList "`"$tf`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
        $content=Get-Content -Path $tf -Raw
        $content=$content -replace "Старое слово","Новое слово"
        Set-Content -Path $tf -Value $content -Encoding UTF8 -NoNewline
        WA "Замена 'Старое слово' -> 'Новое слово'"
        Start-Process $script:Ctx.NppExe -ArgumentList "`"$tf`"";Wait-Action
    }},
    @{ Name="JSON-валидация"; Run={
        Ensure-NotepadPP
        $jf=Join-Path "$env:TEMP\SimWork" "data_$(Rnd 100 999).json"
        @"
{
    "id": $(Rnd 1000 9999),
    "name": "Sample Item",
    "tags": ["alpha", "beta", "gamma"],
    "active": true,
    "price": $((Rnd 100 9999))
}
"@ | Set-Content -Path $jf -Encoding UTF8
        WA "Создан $((Split-Path $jf -Leaf))"
        try {
            $null=Get-Content -Path $jf -Raw|ConvertFrom-Json
            WA "JSON валиден"
        } catch { WA "JSON невалиден" }
        Start-Process $script:Ctx.NppExe -ArgumentList "`"$jf`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="Markdown-документ"; Run={
        Ensure-NotepadPP
        $md=Join-Path "$env:TEMP\SimWork" "README.md"
        @"
# Проект SimWorker

## Описание
Автоматизация офисных задач.

## Установка
``````
git clone https://example.com/simworker.git
cd simworker
``````

## Использование
- Запустить `Simulate-Workday.ps1`
- Указать `-DurationMinutes`
- Наблюдать за работой

## Лицензия
MIT
"@ | Set-Content -Path $md -Encoding UTF8
        WA "README.md создан";Start-Process $script:Ctx.NppExe -ArgumentList "`"$md`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="CSV-таблица"; Run={
        Ensure-NotepadPP
        $cf=Join-Path "$env:TEMP\SimWork" "users.csv"
        "id,name,email,role"
        for($i=1;$i-le 8;$i++){
            $names=@("Анна","Борис","Виктор","Галина","Дмитрий","Елена","Жанна","Игорь")
            $roles=@("admin","user","editor","viewer")
            Add-Content -Path $cf -Value "$i,$($names[$i-1]),$($names[$i-1].ToLower())$i@example.com,$((Pick-Random $roles))" -Encoding UTF8
        }
        WA "users.csv (8 записей)";Start-Process $script:Ctx.NppExe -ArgumentList "`"$cf`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }},
    @{ Name="Python-скрипт"; Run={
        Ensure-NotepadPP
        $py=Join-Path "$env:TEMP\SimWork" "script_$(Rnd 100 999).py"
        @"
import sys
import os

def main():
    print("SimWorker Python script")
    args = sys.argv[1:]
    if not args:
        print("No arguments")
        return 1
    for i, arg in enumerate(args, 1):
        print(f"{i}: {arg}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
"@ | Set-Content -Path $py -Encoding UTF8
        WA "Создан script_$((Split-Path $py -Leaf))";Start-Process $script:Ctx.NppExe -ArgumentList "`"$py`"";Wait-Action
        [void](Focus-App "notepad++" -WaitMs 500)
    }}
)

# ============ Главный цикл ============
$appPools = @{
    Excel=$script:ExcelScenarios
    Word=$script:WordScenarios
    VSCode=$script:VSCodeScenarios
    NotepadPP=$script:NppScenarios
}
$appNames = @("Excel","Word","VSCode","NotepadPP")
$lastApp=$null;$lastSc=$null;$iter=0

try {
    while ($true) {
        Assert-TimeLeft -Reserve 5;$iter++
        $cands=$appNames|?{$_ -ne $lastApp};if($cands.Count -eq 0){$cands=$appNames}
        $app=Pick-Random $cands;$pool=$appPools[$app]
        $scCands=$pool|?{$_.Name -ne $lastSc};if($scCands.Count -eq 0){$scCands=$pool}
        $sc=Pick-Random $scCands

        Write-Host "";Write-Host ("-"*60) -ForegroundColor DarkGray
        WS "Итерация #$iter | $app | '$($sc.Name)' | осталось $(LeftSec) сек."
        Write-Host ("-"*60) -ForegroundColor DarkGray

        switch($app){
            "Excel"{[void](Focus-App EXCEL -WaitMs 400)}
            "Word"{[void](Focus-App WINWORD -WaitMs 400)}
            "VSCode"{[void](Focus-App "Code" -WaitMs 400)}
            "NotepadPP"{[void](Focus-App "notepad++" -WaitMs 400)}
        }

        try { & $sc.Run }
        catch {
            Write-Warning "  Ошибка в сценарии '$($sc.Name)': $($_.Exception.Message)"
            WA "Продолжаем со следующего сценария..."
        }

        $lastApp=$app;$lastSc=$sc.Name
        Wait-Action
    }
}
catch {
    Write-Host "";Write-Host ("!"*60) -ForegroundColor Yellow
    Write-Host " Сценарий прерван: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host " Выполнено итераций: $iter"
    Write-Host ("!"*60) -ForegroundColor Yellow
}
finally {
    Write-Host "";WS "Сохранение и уборка..."
    $saveDir="$env:TEMP\SimWork";if(-not(Test-Path $saveDir)){New-Item -ItemType Directory -Path $saveDir -Force|Out-Null}

    if ($script:Ctx.ExcelWb -and $script:Ctx.Excel) {
        try {
            Start-Sleep -Milliseconds 1500
            $rp=Join-Path $saveDir "Workbook.xlsx"
            if(Test-Path $rp){Remove-Item $rp -Force -EA SilentlyContinue}
            Invoke-WithRetry -Context "Excel.SaveAs" -Action {
                $path=[string]$rp;$fmt=[int]51
                $script:Ctx.ExcelWb.SaveAs($path,$fmt)
            }
            WA "Excel сохранён: $rp"
        } catch { Write-Warning "Excel не сохранён: $_" }
    }

    if ($script:Ctx.WordDoc -and $script:Ctx.Word) {
        try {
            Start-Sleep -Milliseconds 1500
            $dp=Join-Path $saveDir "Document.docx"
            if(Test-Path $dp){Remove-Item $dp -Force -EA SilentlyContinue}
            Invoke-WithRetry -Context "Word.SaveAs" -MaxRetries 30 -DelayMs 500 -Action {
                $path=[string]$dp;$fmt=[int]16
                $script:Ctx.WordDoc.SaveAs([ref]$path,[ref]$fmt)
            }
            WA "Word сохранён: $dp"
        } catch { Write-Warning "Word не сохранён: $_" }
    }

    foreach($p in @(
        @{O=$script:Ctx.ExcelWb;C={param($o)$o.Close($false)}},
        @{O=$script:Ctx.WordDoc;C={param($o)$o.Close($false)}},
        @{O=$script:Ctx.Excel;C={param($o)$o.Quit()}},
        @{O=$script:Ctx.Word;C={param($o)$o.Quit()}}
    )){
        if($p.O){
            try{& $p.C $p.O}catch{}
            try{[Runtime.InteropServices.Marshal]::ReleaseComObject($p.O)|Out-Null}catch{}
        }
    }
    if($script:Ctx.ExcelChart){try{[Runtime.InteropServices.Marshal]::ReleaseComObject($script:Ctx.ExcelChart)|Out-Null}catch{}}
    [GC]::Collect();[GC]::WaitForPendingFinalizers()

    $el=(Get-Date)-$script:StartTime
    Write-Host "";Write-Host ("="*60) -ForegroundColor DarkGray
    Write-Host (" Готово. Прошло: {0:hh\:mm\:ss}, итераций: {1}" -f $el,$iter) -ForegroundColor Green
    Write-Host (" Лимит: {0} сек. | Скорость: x{1}" -f $script:TotalSeconds,$script:SpeedMul)
    Write-Host ("="*60) -ForegroundColor DarkGray
}
