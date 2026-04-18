import requests
import subprocess
import json
from typing import Union, Dict

class RspamdHTTPClient:
    
    def __init__(self, host: str = "127.0.0.1", port: int = 11333, password: str = ""):
        self.base_url = f"http://{host}:{port}"
        self.password = password
    
    def ping(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/stat", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_status(self) -> Dict:
        try:
            response = requests.get(f"{self.base_url}/stat", timeout=5)
            if response.status_code == 200:
                return response.json()
            return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def learn(self, raw_message: Union[bytes, str], decision: str) -> Dict:
        if isinstance(raw_message, str):
            raw_message = raw_message.encode('utf-8')
        
        url = f"{self.base_url}/learn"
        headers = {"Content-Type": "message/rfc822"}
        params = {"spam": "1" if decision == "spam" else "0"}
        
        if self.password:
            params["password"] = self.password
        
        try:
            response = requests.post(
                url,
                data=raw_message,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"status": "success", "response": response.json()}
            else:
                return {
                    "status": "failed",
                    "http_status": response.status_code,
                    "response": response.text
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}

class RspamdRspamdcClient:
    
    def __init__(self):
        self.command = "rspamc"
    
    def ping(self) -> bool:
        try:
            result = subprocess.run(
                [self.command, "ping"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_status(self) -> Dict:
        try:
            result = subprocess.run(
                [self.command, "stat"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"status": "ok", "output": result.stdout}
            return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}
    
    def learn(self, raw_message: Union[bytes, str], decision: str) -> Dict:
        if isinstance(raw_message, str):
            raw_message_bytes = raw_message.encode('utf-8')
        else:
            raw_message_bytes = raw_message
        
        cmd_flag = "-S" if decision == "spam" else "-H"
        
        try:
            result = subprocess.run(
                [self.command, cmd_flag],
                input=raw_message_bytes,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "decision": decision,
                    "output": result.stdout.decode('utf-8', errors='ignore')
                }
            else:
                return {
                    "status": "failed",
                    "error": result.stderr.decode('utf-8', errors='ignore')
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}
