param(
  [string]$Host = "127.0.0.1",
  [int]$Port = 8000
)

$env:PYTHONPATH = "$PSScriptRoot"
uvicorn app.main:app --host $Host --port $Port --reload
