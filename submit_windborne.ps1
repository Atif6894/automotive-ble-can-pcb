# Submit the WindBorne Electrical Engineer Intern application. Run manually: .\submit_windborne.ps1
$Name          = "Mohammed Atif"
$Email         = "REPLACE_WITH_EMAIL"
$ResumeUrl     = "REPLACE_WITH_PUBLIC_RESUME_URL"
$SubmissionUrl = "REPLACE_WITH_GITHUB_URL"
$Notes = "Designed a compact automotive BLE-to-CAN board (TCAN4550 + CC2340R5-Q1) with 9-36 V protection, CAN FD, backup-battery power path, SWD/test access and full fab outputs."

foreach ($v in @($Email, $ResumeUrl, $SubmissionUrl)) {
    if ($v -like "REPLACE_WITH*") { Write-Error "Fill in all REPLACE_WITH_* values first."; exit 1 }
}

$body = @{ career_application = @{
    name = $Name; email = $Email; role = "Electrical Engineer Intern"
    notes = $Notes; submission_url = $SubmissionUrl; resume_url = $ResumeUrl } } | ConvertTo-Json -Depth 3

try {
    $r = Invoke-WebRequest -Uri "https://windbornesystems.com/career_applications.json" -Method Post `
        -ContentType "application/json" -Body $body -UseBasicParsing
    $status = [int]$r.StatusCode; $content = $r.Content
} catch {
    $resp = $_.Exception.Response
    if ($null -eq $resp) { Write-Error $_; exit 1 }
    $status = [int]$resp.StatusCode
    $content = (New-Object System.IO.StreamReader($resp.GetResponseStream())).ReadToEnd()
}
Write-Host "HTTP status: $status"
Write-Host "Response body: $content"
if ($status -eq 200) { Write-Host "SUCCESS: application accepted (HTTP 200)." } else { Write-Host "FAILED: status was not 200."; exit 1 }
