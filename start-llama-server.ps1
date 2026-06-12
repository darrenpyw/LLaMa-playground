#Requires -Version 5.0
Set-StrictMode -Version Latest

# Huggingface Models available for llama-server
$llmModels = @(
    @{ Name = "models.ini";
        Path = "./models.ini";
    },
    @{ Name = "unsloth Qwen3.5-4B-MTP-GGUF";
        Path = "unsloth/Qwen3.5-4B-MTP-GGUF:UD-Q4_K_XL";
        Port = 8000;
        Params = @("--jinja", "--no-mmproj", "--temperature", 0.3, "-cmoe", "-np", 1, "-fa", "on")
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
        Params = @("-np", 4, "--jinja", "--no-mmproj", "-ctk", "q4_0", "-ctv", "q4_0", "-cmoe", "--mlock")
    },
    @{ Name = "nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF";
        Path = "nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M";
        Port = 8000;
        Params = @("-np", 4, "--jinja", "--no-mmproj", "-ctk", "q4_0", "-ctv", "q4_0", "--mlock", "-ngl", "-1", "-dev", "Vulkan1", "-fa", "on", "-kvo", "--mmap")
    },
     @{ Name = "unsloth gemma-4-26B-A4B-it-GGUF UD-Q4_K_M";
        Path = "unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_M";
        Port = 8000;
        Params = @("-np", 1, "--jinja", "--no-mmproj", "--mlock", "--temp", "1.0", "--top-p", "0.95", "--top-k", "64", "-ngl", "8", "-c", "65536", "-fa", "on", "--mmap", "--no-kv-offload", "--no-cache-idle-slots")
    },
     @{ Name = "unsloth gemma-4-12b-it-GGUF UD-Q4_K_XL";
        Path = "unsloth/gemma-4-12b-it-GGUF:UD-Q4_K_XL";
        Port = 8000;
        Params = @("-np", 1, "--jinja", "--no-mmproj", "--mlock", "--temp", "1.0", "--top-p", "0.95", "--top-k", "64", "-ngl", "auto", "-c", "65536", "-fa", "on", "--no-cache-idle-slots")
    },
     @{ Name = "unsloth gemma-4-12b-it-GGUF Q3_K_S";
        Path = "unsloth/gemma-4-12b-it-GGUF:Q3_K_S";
        Port = 8000;
        Params = @("-np", 1, "--jinja", "--no-mmproj", "--mlock", "--temp", "1.0", "--top-p", "0.95", "--top-k", "64", "-ngl", "auto", "-c", "65536", "-fa", "on", "--no-cache-idle-slots")
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
[int]$selection = Read-Host "`nSelect a model (1-$($llmModels.Count + 1))"
Write-Host "`n User entered $($selection)"
Write-Host "`n"

if ($selection -eq ($llmModels.Count + 1)) {
    Write-Host "Exiting..." -ForegroundColor Green
    exit
}

# Get WSL ethernet IP address
# $wslIp =  Get-NetIPAddress |  Where-Object { $_.InterfaceAlias -eq "vEthernet (WSL (Hyper-V firewall))" -and $_.AddressFamily -eq "IPv4" } | Select-Object -ExpandProperty IPAddress
if ($selection -eq 1) {
    $selectedModel = $llmModels[0]
    Write-Host "`nStarting llama-server with $($selectedModel.Path)" -ForegroundColor Green
    Write-Host "`n"
    # Start llama-server
    & llama-server --host 0.0.0.0 --port 8000 --models-preset $($selectedModel.Path)

} elseif ($selection -ge 2 ) {
    $selectedIndex = $selection - 1
    $selectedModel = $llmModels[$selectedIndex]
    
    Write-Host "`nStarting llama-server with $($selectedModel.Name)..." -ForegroundColor Green
    Write-Host "Model: $($selectedModel.Path)" -ForegroundColor Gray
    Write-Host "Port: $($selectedModel.Port)" -ForegroundColor Gray
    Write-Host "Params: $($selectedModel.Params)" -ForegroundColor Gray
    Write-Host "`n"
    
    # Start llama-server
    & llama-server -hf $selectedModel.Path --host 0.0.0.0 --port $selectedModel.Port $selectedModel.Params
    
} else {
    Write-Host "Invalid selection. Please run the script again." -ForegroundColor Red
}
