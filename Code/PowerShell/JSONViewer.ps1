Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- Цвета для типов данных ---
$ColorString  = [System.Drawing.Color]::DarkGreen
$ColorNumber  = [System.Drawing.Color]::Blue
$ColorBool    = [System.Drawing.Color]::Purple
$ColorNull    = [System.Drawing.Color]::Gray
$ColorObject  = [System.Drawing.Color]::FromArgb(0, 102, 204)
$ColorArray   = [System.Drawing.Color]::FromArgb(204, 102, 0)
$ColorDefault = [System.Drawing.Color]::Black

# --- Настройка формы ---
$form = New-Object System.Windows.Forms.Form
$form.Text = "JSON Viewer (PowerShell)"
$form.Size = New-Object System.Drawing.Size(1000, 750)
$form.MinimumSize = New-Object System.Drawing.Size(600, 400)
$form.StartPosition = "CenterScreen"

# --- 1. Верхняя панель (Кнопки) ---
$panelTop = New-Object System.Windows.Forms.Panel
$panelTop.Height = 60
$panelTop.Dock = "Top"
$panelTop.BackColor = [System.Drawing.Color]::FromArgb(240, 240, 240)

$btnOpen = New-Object System.Windows.Forms.Button
$btnOpen.Text = "Открыть JSON"
$btnOpen.Size = New-Object System.Drawing.Size(140, 35)
$btnOpen.Location = New-Object System.Drawing.Point(10, 12)
$btnOpen.FlatStyle = "Flat"
$btnOpen.FlatAppearance.BorderSize = 1
$panelTop.Controls.Add($btnOpen)

$btnExpandAll = New-Object System.Windows.Forms.Button
$btnExpandAll.Text = "Развернуть всё"
$btnExpandAll.Size = New-Object System.Drawing.Size(140, 35)
$btnExpandAll.Location = New-Object System.Drawing.Point(160, 12)
$btnExpandAll.FlatStyle = "Flat"
$btnExpandAll.FlatAppearance.BorderSize = 1
$btnExpandAll.Enabled = $false
$panelTop.Controls.Add($btnExpandAll)

$btnCollapseAll = New-Object System.Windows.Forms.Button
$btnCollapseAll.Text = "Свернуть всё"
$btnCollapseAll.Size = New-Object System.Drawing.Size(140, 35)
$btnCollapseAll.Location = New-Object System.Drawing.Point(310, 12)
$btnCollapseAll.FlatStyle = "Flat"
$btnCollapseAll.FlatAppearance.BorderSize = 1
$btnCollapseAll.Enabled = $false
$panelTop.Controls.Add($btnCollapseAll)

# --- 2. Дерево (Центральная часть) ---
$treeView = New-Object System.Windows.Forms.TreeView
$treeView.Dock = "Fill"
$treeView.Font = New-Object System.Drawing.Font("Consolas", 10, [System.Drawing.FontStyle]::Regular)
$treeView.Indent = 20
$treeView.ShowLines = $true
$treeView.ShowPlusMinus = $true
$treeView.BackColor = [System.Drawing.Color]::White

# --- 3. Нижняя панель (Значение) ---
$panelBottom = New-Object System.Windows.Forms.Panel
$panelBottom.Height = 250
$panelBottom.Dock = "Bottom"
$panelBottom.BackColor = [System.Drawing.Color]::FromArgb(245, 245, 245)
$panelBottom.Visible = $false

$lblValue = New-Object System.Windows.Forms.Label
$lblValue.Text = "Значение выбранного узла:"
$lblValue.Location = New-Object System.Drawing.Point(10, 5)
$lblValue.AutoSize = $true
$lblValue.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$lblValue.BackColor = [System.Drawing.Color]::Transparent
$panelBottom.Controls.Add($lblValue)

$textBoxValue = New-Object System.Windows.Forms.TextBox
$textBoxValue.Multiline = $true
$textBoxValue.ScrollBars = "Vertical"
$textBoxValue.ReadOnly = $true
$textBoxValue.Font = New-Object System.Drawing.Font("Consolas", 10)
$textBoxValue.BackColor = [System.Drawing.Color]::White
$textBoxValue.BorderStyle = "FixedSingle"
# ИСПРАВЛЕНИЕ: Dock = Fill + отступ через Margin. Location и Size удалены.
$textBoxValue.Dock = "Fill"
$textBoxValue.Margin = New-Object System.Windows.Forms.Padding(10, 30, 10, 10)
$panelBottom.Controls.Add($textBoxValue)

# --- Добавление элементов на форму ---
# Порядок критичен: Bottom -> Fill -> Top
$form.Controls.Add($panelBottom)
$form.Controls.Add($treeView)
$form.Controls.Add($panelTop)

# --- Логика ---

function Get-ValueColor {
    param([object]$Value)
    
    if ($null -eq $Value) { return $ColorNull }
    if ($Value -is [System.String]) { return $ColorString }
    if ($Value -is [System.Int32] -or $Value -is [System.Int64] -or $Value -is [System.Decimal] -or $Value -is [System.Double]) { return $ColorNumber }
    if ($Value -is [System.Boolean]) { return $ColorBool }
    if ($Value -is [PSCustomObject]) { return $ColorObject }
    if ($Value -is [System.Array]) { return $ColorArray }
    
    return $ColorDefault
}

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
                $node.ForeColor = $ColorArray
                $ParentNode.Nodes.Add($node)
                Build-JsonTree -JsonObject $item -ParentNode $node
            } else {
                $displayValue = if ($null -eq $item) { "null" } else { $item.ToString() }
                $node = New-Object System.Windows.Forms.TreeNode("$nodeName : $displayValue")
                $node.Tag = $item
                $node.ForeColor = Get-ValueColor $item
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
                $node.ForeColor = if ($value -is [System.Array]) { $ColorArray } else { $ColorObject }
                $ParentNode.Nodes.Add($node)
                Build-JsonTree -JsonObject $value -ParentNode $node
            } else {
                $displayValue = if ($null -eq $value) { "null" } else { $value.ToString() }
                if ($displayValue.Length -gt 80) {
                    $displayValue = $displayValue.Substring(0, 80) + "..."
                }
                $node = New-Object System.Windows.Forms.TreeNode("$nodeName : $displayValue")
                $node.Tag = $prop.Value
                $node.ForeColor = Get-ValueColor $prop.Value
                $ParentNode.Nodes.Add($node)
            }
        }
    }
}

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
            
            $rootNode = New-Object System.Windows.Forms.TreeNode("📄 Root (JSON)")
            $rootNode.Tag = $jsonObject
            $rootNode.ForeColor = $ColorDefault
            $treeView.Nodes.Add($rootNode)
            
            Build-JsonTree -JsonObject $jsonObject -ParentNode $rootNode
            
            $rootNode.Expand()
            
            $btnExpandAll.Enabled = $true
            $btnCollapseAll.Enabled = $true
            
            $form.Cursor = [System.Windows.Forms.Cursors]::Default
        }
        catch {
            $form.Cursor = [System.Windows.Forms.Cursors]::Default
            [System.Windows.Forms.MessageBox]::Show("Ошибка при чтении JSON: `n$($_.Exception.Message)", "Ошибка", "OK", "Error")
        }
    }
})

$btnExpandAll.Add_Click({
    if ($treeView.Nodes.Count -gt 0) {
        $treeView.BeginUpdate()
        $treeView.ExpandAll()
        $treeView.EndUpdate()
    }
})

$btnCollapseAll.Add_Click({
    if ($treeView.Nodes.Count -gt 0) {
        $treeView.BeginUpdate()
        $treeView.CollapseAll()
        foreach ($node in $treeView.Nodes) {
            $node.Expand()
        }
        $treeView.EndUpdate()
    }
})

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

$form.ShowDialog()