import json, os
from datetime import datetime

LOG_PATH = 'data/chat_logs.json'

def log_search(user_input, response, success):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    log_data = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            log_data = json.load(f)
    log_data.append({
        'timestamp': str(datetime.now()),
        'query': user_input,
        'response': response,
        'success': success
    })
    with open(LOG_PATH, 'w') as f:
        json.dump(log_data, f, indent=4)

def get_analytics():
    if not os.path.exists(LOG_PATH):
        return {"total": 0, "success": 0, "failure": 0}
    with open(LOG_PATH) as f:
        logs = json.load(f)
    total = len(logs)
    success = sum(1 for log in logs if log['success'])
    failure = total - success
    return {"total": total, "success": success, "failure": failure}