
filename = 'dist/2025-12-24T152325_Compromised_DEVICE01/C/Windows/System32/winevt/logs/Microsoft-Windows-Sysmon%4Operational.evtx'
offset = 1935717

with open(filename, 'rb') as f:
    f.seek(offset)
    data = f.read(500)
    
print(data.hex())
