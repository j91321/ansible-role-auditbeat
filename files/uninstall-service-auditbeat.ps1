# Delete and stop the service if it already exists.
if (Get-Service auditbeat -ErrorAction SilentlyContinue) {
  $service = Get-WmiObject -Class Win32_Service -Filter "name='auditbeat'"
  $service.StopService()
  Start-Sleep -s 1
  $service.delete()
}
