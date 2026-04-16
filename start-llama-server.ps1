#Requires -Version 5.0

# Huggingface Models available for llama-server
$llmModels = @(
    @{ Name = "unsloth Qwen3.5-4B-GGUF";
        Path = "unsloth/Qwen3.5-4B-GGUF";
        Port = 8000;
        Params = @("-c", 65355, "--temperature", 0.5,"--top-p", 0.75)
    },
    @{ Name = "Unsloth gemma-4-E4B-it-GGUF Q4_K_M";
        Path = "unsloth/gemma-4-E4B-it-GGUF:Q4_K_M";
        Port = 8000;
        Params = @("-c", 32768, "--temperature", 0.75,"--top-p", 0.75, "--fit", "off", "-nkvo", "-np", 4, "--jinja")
    },
    @{ Name = "unsloth gemma-4-E2B-it-GGUF";
        Path = "unsloth/gemma-4-E2B-it-GGUF";
        Port = 8000;
        Params = @("-c", 32768, "--temperature", 0.75,"--top-p", 0.25, "--fit", "off", "-nkvo", "-np", 4, "--jinja", "-ctk", "q4_0", "-ctv", "q4_0")
    },
    @{ Name = "unsloth gemma-4-E2B-it-GGUF Tuning";
        Path = "unsloth/gemma-4-E2B-it-GGUF";
        Port = 8000;
        Params = @("-c", 32768, "--temperature", 0.75,"--top-p", 0.25, "--fit", "off", "-nkvo", "-np", 4, "--jinja", "-ctk", "q4_0", "-ctv", "q4_0")
    },
    @{ Name = "unsloth gemma-4-E4B-it-GGUF UD-Q4_K_XL";
        Path = "unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL";
        Port = 8000;
        Params = @("-nkvo", "-np", 4, "--jinja", "-ctk", "q4_0", "-ctv", "q4_0")
    }
    
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
# $wslIp =  Get-NetIPAddress |  Where-Object { $_.InterfaceAlias -eq "vEthernet (WSL (Hyper-V firewall))" -and $_.AddressFamily -eq "IPv4" } | Select-Object -ExpandProperty IPAddress

if ($selection -ge 1 -and $selection -le $llmModels.Count) {
    $selectedIndex = $selection - 1
    $selectedModel = $llmModels[$selectedIndex]
    
    Write-Host "`nStarting llama-server with $($selectedModel.Name)..." -ForegroundColor Green
    Write-Host "Model: $($selectedModel.Path)" -ForegroundColor Gray
    Write-Host "Port: $($selectedModel.Port)" -ForegroundColor Gray
    Write-Host "Params: $($selectedModel.Params)" -ForegroundColor Gray
    Write-Host "`n"
    
    # Start llama-server
    & llama-server -hf $selectedModel.Path --host 0.0.0.0 --port $selectedModel.Port $selectedMode.Params
    #& "llama-server.exe" --models-dir "C:\Users\Pre-Installed User\.cache\huggingface\hub" --host 0.0.0.0 --port 8000
    
} else {
    Write-Host "Invalid selection. Please run the script again." -ForegroundColor Red
}
