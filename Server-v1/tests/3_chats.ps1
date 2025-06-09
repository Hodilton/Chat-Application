[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Send-Message {
    param (
        [int]$chat_id,
        [int]$sender_id,
        [string]$content
    )

    $uri = "http://localhost:8000/messages"

    # Create request body with proper encoding
    $body = @{
        chat_id = $chat_id
        sender_id = $sender_id
        content = $content
    } | ConvertTo-Json -Compress

    try {
        Write-Host "Sending message..." -ForegroundColor Cyan
        Write-Host "Request body: $body" -ForegroundColor DarkGray

        # Using Invoke-RestMethod with proper encoding settings
        $response = Invoke-RestMethod -Uri $uri -Method Post `
            -ContentType "application/json; charset=utf-8" `
            -Body $body `
            -ErrorAction Stop

        $response | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errorResponse = $reader.ReadToEnd()
            $reader.Close()
            $errorResponse | Write-Host -ForegroundColor Red
        }
    }
}

function Get-Messages {
    param (
        [int]$chat_id
    )

    $uri = "http://localhost:8000/messages/$chat_id"

    try {
        Write-Host "Getting messages for chat $chat_id..." -ForegroundColor Cyan
        $response = Invoke-RestMethod -Uri $uri -Method Get
        $response | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Green
    }
    catch {
        Write-Host "Error getting messages: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "=== MESSAGES API TESTING ===" -ForegroundColor Yellow

# 1. Send message
#Send-Message -chat_id 6 -sender_id 1 -content "Hello, how are you?"
Send-Message -chat_id 6 -sender_id 1 -content "How about going to a cafe?"

# 2. Get messages
#Get-Messages -chat_id 1