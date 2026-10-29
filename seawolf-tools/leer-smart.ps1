# Lee el SMART de TODOS los discos y guarda los datos para Seawolf Tools.
# Se ejecuta en modo administrador (lo lanza LEER-SMART-ADMIN.bat).
# NO toca datos: solo LEE el estado de los discos. Lo unico que "enciende" es el
# registro SMART en los discos que lo tuvieran apagado (es un interruptor, no borra nada).

$ErrorActionPreference = "SilentlyContinue"
$OutputEncoding = [System.Text.Encoding]::UTF8

$sc = "C:\Program Files\smartmontools\bin\smartctl.exe"
if (-not (Test-Path $sc)) {
    Write-Host ""
    Write-Host "  *** NO se encontro smartctl en:" -ForegroundColor Red
    Write-Host "      $sc" -ForegroundColor Red
    Write-Host "  Instalalo con:  winget install smartmontools.smartmontools" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

$destino = Join-Path $PSScriptRoot "seawolf-smart.json"
Write-Host "  Leyendo los discos... (esto NO modifica nada, solo lee)" -ForegroundColor Cyan
Write-Host ""

$discos = @{}
$ok = 0
$scan = & $sc --scan
foreach ($linea in $scan) {
    if ($linea -match '^(/dev/\S+)\s+-d\s+(\S+)') {
        $dev = $Matches[1]
        $tipo = $Matches[2]

        # Enciende el registro SMART si estaba apagado (interruptor, no borra nada)
        & $sc -s on -d $tipo $dev 2>&1 | Out-Null

        $j = (& $sc -j -a -d $tipo $dev 2>$null | Out-String)
        if ($j -and $j.Trim().StartsWith("{")) {
            $discos[$dev] = $j
            $ok++
            $modelo = ""
            try { $modelo = ($j | ConvertFrom-Json).model_name } catch { }
            if (-not $modelo) { $modelo = "$dev ($tipo)" }
            Write-Host ("   [OK]  {0,-10} {1}" -f $dev, $modelo) -ForegroundColor Green
        } else {
            Write-Host ("   [--]  {0,-10} no se pudo leer" -f $dev) -ForegroundColor DarkGray
        }
    }
}

# Guardar para que el aplicativo lo lea (el aplicativo corre como usuario normal)
$paquete = @{
    fecha        = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    equipo       = $env:COMPUTERNAME
    smartctl     = (& $sc --version | Select-Object -First 1)
    dispositivos = $discos
}
$paquete | ConvertTo-Json -Depth 8 | Set-Content -Path $destino -Encoding UTF8

Write-Host ""
Write-Host ("  Discos leidos: {0}" -f $ok) -ForegroundColor Cyan
Write-Host "  Datos guardados en:" -ForegroundColor Cyan
Write-Host "    $destino" -ForegroundColor White
Write-Host ""
Write-Host "  Ya puedes volver a Seawolf Tools y pulsar Analizar." -ForegroundColor Yellow
Write-Host ""
