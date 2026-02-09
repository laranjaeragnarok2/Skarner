# Script para verificar atividade no GitHub (Público)
$username = "laranjaeragnarok2"
$url = "https://api.github.com/users/$username/events/public"

try {
    $events = Invoke-RestMethod -Uri $url -Method Get
    $recentCommits = $events | Where-Object { $_.type -eq "PushEvent" } | Select-Object -First 5
    
    if ($recentCommits) {
        Write-Output "Últimos Pushes do Arthur no GitHub:"
        foreach ($event in $recentCommits) {
            $repo = $event.repo.name
            $date = [DateTime]::Parse($event.created_at).ToString("dd/MM/yyyy HH:mm")
            $messages = $event.payload.commits.message -join "; "
            Write-Output " - [$date] Repo: $repo | Msg: $messages"
        }
    } else {
        Write-Output "Nenhuma atividade de push recente encontrada (pública)."
    }
} catch {
    Write-Output "Erro ao acessar o GitHub: $($_.Exception.Message)"
}
