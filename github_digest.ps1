# Script para Resumo de Commits
$username = "laranjaeragnarok2"
$token = "SEU_TOKEN_AQUI"
$url = "https://api.github.com/users/$username/events"
$since = (Get-Date).AddDays(-7)

$headers = @{
    "Authorization" = "Bearer $token"
    "Accept"        = "application/vnd.github.v3+json"
}

try {
    $events = Invoke-RestMethod -Uri $url -Method Get -Headers $headers
    
    $recentPushes = $events | Where-Object { 
        $_.type -eq "PushEvent" -and ([DateTime]::Parse($_.created_at) -gt $since.ToUniversalTime())
    }

    if ($recentPushes) {
        Write-Output "Resumo Semanal de Commits (Teste)"
        foreach ($event in $recentPushes) {
            $repo = $event.repo.name
            $date = [DateTime]::Parse($event.created_at).ToLocalTime().ToString("dd/MM HH:mm")
            
            if ($event.payload.commits.Count -gt 0) {
                foreach ($commit in $event.payload.commits) {
                    $msg = $commit.message.Split("`n")[0]
                    Write-Output "- [$date] [$repo] $msg"
                }
            } else {
                Write-Output "- [$date] [$repo] (Push detectado)"
            }
        }
    } else {
        Write-Output "Nenhum commit detectado nos ultimos 7 dias."
    }
} catch {
    Write-Output "Erro ao acessar API GitHub: $_"
}
