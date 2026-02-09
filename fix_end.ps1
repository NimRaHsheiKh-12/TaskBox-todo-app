# Get the content of the file except the last line
$content = Get-Content -Path 'C:\fullstack TODO\todo_fullstack_app\deploy_k8s_fixed.ps1' -Raw
$contentWithoutLastLine = $content -replace '(?s)(.*)\r?\n.*?$', '$1'
$newContent = $contentWithoutLastLine + "`r`n`r`nWrite-Host ""`n🎉 Your Todo application is now deployed on Kubernetes!"" -ForegroundColor Green`r`n"
[System.IO.File]::WriteAllText('C:\fullstack TODO\todo_fullstack_app\deploy_k8s_fixed.ps1', $newContent, [System.Text.Encoding]::UTF8)