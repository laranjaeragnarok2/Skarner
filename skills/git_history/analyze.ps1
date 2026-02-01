
param(
    [string]$path = "C:\Users\Horyu\Desktop\Projetos",
    [int]$hours = 24
)

$projects = Get-ChildItem -Path $path -Directory

$report = @()
$report += "# Relatório de Progresso (Últimas $hours horas)"
$report += ""

foreach ($proj in $projects) {
    if (Test-Path "$($proj.FullName)\.git") {
        # Check commits
        $commits = git -C $proj.FullName log --since="$hours.hours.ago" --oneline --author="Horyu" 2>$null
        
        if ($commits) {
            $report += "## 📂 $($proj.Name)"
            $report += $commits
            $report += ""
        }
        
        # Check status (uncommitted changes)
        $status = git -C $proj.FullName status --porcelain 2>$null
        if ($status) {
            $report += "⚠️  $($proj.Name) tem alterações não commitadas."
        }
    }
}

if ($report.Count -eq 2) {
    Write-Output "Nada commitado nas últimas $hours horas. 💤"
} else {
    Write-Output ($report -join "`n")
}
