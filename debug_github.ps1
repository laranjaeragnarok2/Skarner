# Script para Debug
$username = "laranjaeragnarok2"
$token = "SEU_TOKEN_AQUI"
$url = "https://api.github.com/users/$username/events"
$headers = @{ "Authorization" = "Bearer $token"; "Accept" = "application/vnd.github.v3+json" }

try {
    $events = Invoke-RestMethod -Uri $url -Method Get -Headers $headers
    $pushEvents = $events | Where-Object { $_.type -eq "PushEvent" }
    
    Write-Output "Total de eventos: $($events.Count)"
    Write-Output "Total de PushEvents: $($pushEvents.Count)"
    
    if ($pushEvents) {
        $first = $pushEvents | Select-Object -First 1
        Write-Output "Exemplo de evento:"
        Write-Output "Repo: $($first.repo.name)"
        Write-Output "Date: $($first.created_at)"
        Write-Output "Commits count: $($first.payload.commits.Count)"
        Write-Output "Message: $($first.payload.commits[0].message)"
    }
} catch {
    Write-Output "Erro: $($_.Exception.Message)"
}
