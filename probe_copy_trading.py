"""Public endpoint diagnostics. No credentials, no orders, no notifications."""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

BASE = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/"
def fetch(path, pid):
    req = urllib.request.Request(BASE + path + "?portfolioId=" + pid, headers={
        "User-Agent": "Mozilla/5.0", "Accept": "application/json",
        "clienttype": "web", "Referer": "https://www.binance.com/en/copy-trading"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            body = response.read()
            try:
                payload = json.loads(body)
            except ValueError:
                return {"ok": False, "http_status": response.status, "error": "Non-JSON response"}
            return {"ok": payload.get("code") == "000000" and payload.get("success") is not False and payload.get("data") is not None,
                    "http_status": response.status, "payload": payload}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": "HTTP access rejected"}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}

def main():
    targets = json.loads(Path("tracked_portfolios.json").read_text(encoding="utf-8"))
    output = Path("diagnostics")
    output.mkdir(exist_ok=True)
    passed = True
    for target in targets:
        pid = target["portfolio_id"]
        result = {"target": target, "checked_at": datetime.now(timezone.utc).isoformat()}
        result["detail"] = fetch("lead-portfolio/detail", pid)
        result["positions"] = fetch("lead-data/positions", pid)
        detail = result["detail"].get("payload", {}).get("data")
        name = detail.get("nickname") if isinstance(detail, dict) else None
        result["identity_verified"] = name == target["name"]
        result["ready_for_schema_review"] = result["identity_verified"] and result["positions"]["ok"]
        passed = passed and result["ready_for_schema_review"]
        (output / (pid + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"portfolio_id": pid, "detail_ok": result["detail"]["ok"],
                         "positions_ok": result["positions"]["ok"], "identity_verified": result["identity_verified"],
                         "ready_for_schema_review": result["ready_for_schema_review"]}, ensure_ascii=False))
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
