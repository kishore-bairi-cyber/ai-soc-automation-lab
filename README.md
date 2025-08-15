
# 🔐 LSASS Memory Access via Procdump Detection

## 📌 Summary
This detection identifies unauthorized access to `lsass.exe` (Local Security Authority Subsystem Service) memory using tools like `procdump.exe` or `mimikatz.exe`. This behavior is consistent with credential dumping (T1003.001) and is a high-severity threat.

## 📊 Detection Logic

### ▶️ Splunk SPL
```spl
index=windows sourcetype=XmlWinEventLog:Microsoft-Windows-Sysmon/Operational 
EventCode=10 TargetImage="*\lsass.exe"
(Image="*\procdump.exe" OR Image="*\mimikatz.exe" OR Image="*\taskmgr.exe")
| stats count by _time, host, User, Image, TargetImage, SourceProcessGUID
```

### ▶️ Sentinel KQL
```kql
DeviceProcessEvents
| where ActionType == "ProcessAccessed"
| where TargetProcessName =~ "lsass.exe"
| where FileName in~ ("procdump.exe", "mimikatz.exe", "taskmgr.exe")
| project Timestamp, DeviceName, InitiatingProcessAccountName, FileName
```

## 🔎 Triage Checklist (SOC Analyst)

| Step | Action |
|------|--------|
| ✅ | Identify source user and device (`attackeruser`, `WIN-ENDPOINT-001`) |
| ✅ | Check if procdump/mimikatz was executed manually |
| ✅ | Look for associated memory dump files |
| ✅ | Review lateral movement post-execution |
| ✅ | Check Defender/Splunk logs for LSASS crashes |
| ✅ | Correlate with VPN, RDP, or unusual logon |

## 🎯 MITRE & Kill Chain Mapping

| MITRE ID     | T1003.001 – Credential Dumping via LSASS |
|--------------|------------------------------------------|
| Kill Chain   | Credential Access → Lateral Movement     |
| Detection Tag| `attack.credential_access`, `Sysmon`, `EDR` |

## 🚨 Alert Example

```json
{
  "alert_name": "Unauthorized LSASS Memory Access via Procdump",
  "host": "WIN-ENDPOINT-001",
  "user": "DOMAIN\\attackeruser",
  "process": "C:\\tools\\procdump.exe",
  "target_process": "C:\\Windows\\System32\\lsass.exe",
  "event_type": "process_access",
  "event_id": "Sysmon EventCode 10"
}
```

## 🛡️ Recommended Response Actions

- [ ] Isolate host immediately (auto via SentinelOne / Defender API)
- [ ] Notify IR Team and open investigation
- [ ] Check for dumped credential artifacts (*.dmp)
- [ ] Rotate local/domain credentials if confirmed
- [ ] Hunt for additional LSASS access across org

## 🤖 Automation Script (Python)
→ See `automation.py` for host isolation via SentinelOne API

## 🧠 LLM Prompt (Auto-Triage)
```text
"Summarize this alert: Procdump.exe accessed lsass.exe on WIN-ENDPOINT-001 by DOMAIN\attackeruser. What are the risks, evidence, and next actions?"
```

## 📂 Files in This Folder
```
📁 week1-lsass-memory/
├── README.md
├── detection_spl.txt
├── detection_kql.txt
├── automation.py
├── sample_alert.json
├── LLM_prompt.txt
```

## ✍️ Authored by:
**Kishore Bairi – SOC/DFIR/Threat Hunter | Detection SME | AI-SOC Innovator**
