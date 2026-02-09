
$subnet = "192.168.0"
$jobs = @()

Write-Host "Iniciando varredura na rede $subnet.0/24..." -ForegroundColor Cyan

1..254 | ForEach-Object {
    $ip = "$subnet.$_"
    $jobs += Test-Connection -ComputerName $ip -Count 1 -AsJob
}

$activeHosts = $jobs | Wait-Job | Receive-Job | Where-Object { $_.StatusCode -eq 0 }

$results = foreach ($hostObj in $activeHosts) {
    $ip = $hostObj.Address
    
    # Tentar resolver Hostname
    try {
        $hostname = [System.Net.Dns]::GetHostEntry($ip).HostName
    } catch {
        $hostname = "N/A"
    }

    # Pegar MAC via ARP
    $arp = arp -a $ip | Select-String "$ip\s+([0-9a-f-]+)"
    $mac = if ($arp -match "([0-9a-f-]{17})") { $matches[1] } else { "N/A" }

    # Identificar tipo baseado em portas comuns
    $ports = @(80, 443, 445, 22, 548, 5000)
    $openPorts = @()
    foreach ($port in $ports) {
        $connection = New-Object System.Net.Sockets.TcpClient
        $t = $connection.BeginConnect($ip, $port, $null, $null)
        $wait = $t.AsyncWaitHandle.WaitOne(100, $false)
        if ($wait -and $connection.Connected) {
            $openPorts += $port
        }
        $connection.Close()
    }

    $description = switch ($openPorts) {
        { $_ -contains 445 } { "Windows/Server/NAS (SMB)" }
        { $_ -contains 548 } { "Apple Device (AFP)" }
        { $_ -contains 22 } { "Linux/SSH Device" }
        { $_ -contains 5000 } { "Synology/Docker/UpnP" }
        { $_ -contains 80 -or $_ -contains 443 } { "Web Service/Router/IoT" }
        Default { "Dispositivo Genrico" }
    }

    if ($ip -eq "192.168.0.1") { $description = "Roteador/Gateway" }
    if ($hostname -like "*DESKTOP*") { $description = "PC Windows (Arthur?)" }

    [PSCustomObject]@{
        IP          = $ip
        MAC         = $mac
        Hostname    = $hostname
        Portas      = ($openPorts -join ",")
        Identificado= $description
    }
}

$results | Format-Table -AutoSize
