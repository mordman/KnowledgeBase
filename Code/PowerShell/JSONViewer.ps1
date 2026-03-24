Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Настройка формы ---
$form = New-Object System.Windows.Forms.Form
$form.Text = "JSON Viewer (PowerShell)"
$form.Size = New-Object System.Drawing.Size(900, 700)
$form.MinimumSize = New-Object System.Drawing.Size(600, 400)
$form.StartPosition = "CenterScreen"

# --- 1. Верхняя панель (Кнопка) ---
$panelTop = New-Object System.Windows.Forms.Panel
$panelTop.Height = 60
$panelTop.Dock = "Top"
$panelTop.BackColor = [System.Drawing.Color]::FromArgb(240, 240, 240)

$btnOpen = New-Object System.Windows.Forms.Button
$btnOpen.Text = "Открыть JSON файл"
$btnOpen.Size = New-Object System.Drawing.Size(160, 35)
$btnOpen.Location = New-Object System.Drawing.Point(15, 12)
$btnOpen.FlatStyle = "Flat"
$btnOpen.FlatAppearance.BorderSize = 1
$panelTop.Controls.Add($btnOpen)

# --- 2. Дерево (Центральная часть) ---
$treeView = New-Object System.Windows.Forms.TreeView
$treeView.Dock = "Fill"
#$treeView.Font = New-Object System.Drawing.Font("Consolas", 10)
$treeView.Indent = 20
$treeView.ShowLines = $true
$treeView.ShowPlusMinus = $true

# --- 3. Нижняя панель (Значение) ---
$panelBottom = New-Object System.Windows.Forms.Panel
$panelBottom.Height = 200
$panelBottom.Dock = "Bottom"
$panelBottom.BackColor = [System.Drawing.Color]::FromArgb(245, 245, 245)

$lblValue = New-Object System.Windows.Forms.Label
$lblValue.Text = "Значение выбранного узла:"
$lblValue.Location = New-Object System.Drawing.Point(10, 5)
$lblValue.AutoSize = $true
# ИСПРАВЛЕНИЕ 1: Используем правильный тип для стиля шрифта
#$lblValue.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$panelBottom.Controls.Add($lblValue)

$textBoxValue = New-Object System.Windows.Forms.TextBox
$textBoxValue.Multiline = $true
$textBoxValue.ScrollBars = "Vertical"
$textBoxValue.ReadOnly = $true
#$textBoxValue.Font = New-Object System.Drawing.Font("Consolas", 10)
$textBoxValue.BackColor = [System.Drawing.Color]::White
$textBoxValue.BorderStyle = "FixedSingle"
$textBoxValue.Location = New-Object System.Drawing.Point(10, 30)

# ИСПРАВЛЕНИЕ 2: Вычисляем размеры в отдельных переменных перед созданием объекта
$txtBoxWidth = $panelBottom.Width - 20
$txtBoxHeight = $panelBottom.Height - 40
$textBoxValue.Size = New-Object System.Drawing.Size($txtBoxWidth, $txtBoxHeight)

$textBoxValue.Anchor = "Top, Left, Right, Bottom"
$panelBottom.Controls.Add($textBoxValue)

# --- Добавление элементов на форму ---
# Порядок важен для корректной работы Dock
$form.Controls.Add($panelBottom)
$form.Controls.Add($treeView)
$form.Controls.Add($panelTop)

# --- Логика ---

# Рекурсивная функция для построения дерева
function Build-JsonTree {
    param (
        [object]$JsonObject,
        [System.Windows.Forms.TreeNode]$ParentNode
    )

    if ($null -eq $JsonObject) { return }

    if ($JsonObject -is [System.Array]) {
        for ($i = 0; $i -lt $JsonObject.Count; $i++) {
            $item = $JsonObject[$i]
            $nodeName = "[$i]"
            
            if ($item -is [PSCustomObject] -or $item -is [System.Array]) {
                $node = New-Object System.Windows.Forms.TreeNode($nodeName)
                $node.Tag = $item
                $node.ForeColor = [System.Drawing.Color]::FromArgb(0, 102, 204)
                $ParentNode.Nodes.Add($node)
                Build-JsonTree -JsonObject $item -ParentNode $node
            } else {
                $displayValue = if ($null -eq $item) { "null" } else { $item.ToString() }
                $node = New-Object System.Windows.Forms.TreeNode("$nodeName : $displayValue")
                $node.Tag = $item
                $node.ForeColor = [System.Drawing.Color]::DarkGreen
                $ParentNode.Nodes.Add($node)
            }
        }
    }
    elseif ($JsonObject -is [PSCustomObject]) {
        foreach ($prop in $JsonObject.PSObject.Properties) {
            $nodeName = $prop.Name
            $value = $prop.Value

            if ($value -is [PSCustomObject] -or $value -is [System.Array]) {
                $node = New-Object System.Windows.Forms.TreeNode($nodeName)
                $node.Tag = $value
                $node.ForeColor = [System.Drawing.Color]::FromArgb(0, 102, 204)
                $ParentNode.Nodes.Add($node)
                Build-JsonTree -JsonObject $value -ParentNode $node
            } else {
                $displayValue = if ($null -eq $value) { "null" } else { $value.ToString() }
                if ($displayValue.Length -gt 60) {
                    $displayValue = $displayValue.Substring(0, 60) + "..."
                }
                $node = New-Object System.Windows.Forms.TreeNode("$nodeName : $displayValue")
                $node.Tag = $prop.Value
                $node.ForeColor = [System.Drawing.Color]::DarkGreen
                $ParentNode.Nodes.Add($node)
            }
        }
    }
}

# Обработчик кнопки "Открыть"
$btnOpen.Add_Click({
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = "JSON Files (*.json)|*.json|All Files (*.*)|*.*"
    $dialog.Title = "Выберите JSON файл"
    
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        try {
            $form.Cursor = [System.Windows.Forms.Cursors]::WaitCursor
            $jsonContent = Get-Content -Path $dialog.FileName -Raw -Encoding UTF8
            $jsonObject = ConvertFrom-Json $jsonContent
            
            $treeView.Nodes.Clear()
            $textBoxValue.Clear()
            
            $rootNode = New-Object System.Windows.Forms.TreeNode("Root (JSON)")
            $rootNode.Tag = $jsonObject
            $rootNode.ForeColor = [System.Drawing.Color]::Black
            #$rootNode.Font = New-Object System.Drawing.Font("Consolas", 10, [System.Drawing.FontStyle]::Bold)
            $treeView.Nodes.Add($rootNode)
            
            Build-JsonTree -JsonObject $jsonObject -ParentNode $rootNode
            
            $rootNode.Expand()
            $form.Cursor = [System.Windows.Forms.Cursors]::Default
        }
        catch {
            $form.Cursor = [System.Windows.Forms.Cursors]::Default
            [System.Windows.Forms.MessageBox]::Show("Ошибка при чтении JSON: `n$($_.Exception.Message)", "Ошибка", "OK", "Error")
        }
    }
})

# Обработчик выбора узла
$treeView.Add_AfterSelect({
    $selectedNode = $treeView.SelectedNode
    if ($selectedNode -and $selectedNode.Tag) {
        $value = $selectedNode.Tag
        
        if ($value -is [PSCustomObject] -or $value -is [System.Array]) {
            try {
                $textBoxValue.Text = ($value | ConvertTo-Json -Depth 10 -Compress:$false)
            } catch {
                $textBoxValue.Text = $value.GetType().FullName
            }
        } else {
            $textBoxValue.Text = $value.ToString()
        }
    } else {
        $textBoxValue.Clear()
    }
})

# Обработчик изменения размера формы (динамическое изменение размера текстового поля)
$form.Add_Resize({
    if ($panelBottom.Width -gt 50) {
        $textBoxValue.Width = $panelBottom.Width - 20
        $textBoxValue.Height = $panelBottom.Height - 40
    }
})

# Запуск формы
$form.ShowDialog()