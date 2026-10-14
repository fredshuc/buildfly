SPLIT REVIEW ZIP

Both numbered parts are required. Each is strictly below 25,000,000 bytes.
These are byte segments, not independent ZIP archives. Do not rename them or extract a single part.

WINDOWS REASSEMBLY
Save both numbered parts, SHA256.json and JOIN.ps1 in the same folder.
Open PowerShell in that folder and run:
  powershell -NoProfile -ExecutionPolicy Bypass -File .\JOIN.ps1
The script verifies each part, joins them in order, and verifies the reconstructed ZIP.
It does not overwrite an existing ZIP. Extract the reconstructed ZIP normally, then open 00_START_HERE.html.

7-Zip can also open the .zip.001 file when both parts are together.

The reconstructed ZIP is byte-identical to the original English review package.
Original SHA256:
0e931351b87aeabf54ee12f92433c28dfd499534a339a304bea17c69134647af
