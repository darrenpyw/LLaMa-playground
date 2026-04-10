#Requires -Version 5.0

# LLM Models available for llama-server
$llmModels = @(
    @{ Name = "unsloth Qwen3.5-4B-GGUF"; Path = "unsloth/Qwen3.5-4B-GGUF"; Port = 8000; Context = 65535 },
    @{ Name = "Unsloth gemma-4-E4B-it-GGUF"; Path = "unsloth/gemma-4-E4B-it-GGUF"; Port = 8000; Config = "-c 65535 --temperature 0.5 --top-p 0.5" }
)

# Display menu
Write-Host "`nAvailable LLM Models:" -ForegroundColor Cyan
Write-Host "`n"
for ($i = 0; $i -lt $llmModels.Count; $i++) {
    Write-Host "$($i + 1). $($llmModels[$i].Name)" -ForegroundColor Yellow
}
Write-Host "$($llmModels.Count + 1). Exit" -ForegroundColor Yellow

# Get user selection
$selection = Read-Host "`nSelect a model (1-$($llmModels.Count + 1))"

if ($selection -eq ($llmModels.Count + 1)) {
    Write-Host "Exiting..." -ForegroundColor Green
    exit
}

# Get WSL ethernet IP address
$wslIp =  Get-NetIPAddress |  Where-Object { $_.InterfaceAlias -eq "vEthernet (WSL (Hyper-V firewall))" -and $_.AddressFamily -eq "IPv4" } | Select-Object -ExpandProperty IPAddress

if ($selection -ge 1 -and $selection -le $llmModels.Count) {
    $selectedIndex = $selection - 1
    $selectedModel = $llmModels[$selectedIndex]
    
    Write-Host "`nStarting llama-server with $($selectedModel.Name)..." -ForegroundColor Green
    Write-Host "Model: $($selectedModel.Path)" -ForegroundColor Gray
    Write-Host "Port: $($selectedModel.Port)" -ForegroundColor Gray
    Write-Host "Context: $($selectedModel.Config)" -ForegroundColor Gray
    Write-Host "`n"
    
    # Start llama-server (adjust path as needed)
    #& "llama-server.exe" -hf $selectedModel.Path --host 0.0.0.0 --port $selectedModel.Port -c $selectedModel.Context
    & "llama-server.exe" --models-dir "C:\Users\Pre-Installed User\.cache\huggingface\hub" --host 0.0.0.0 --port 8000
    
} else {
    Write-Host "Invalid selection. Please run the script again." -ForegroundColor Red
}
