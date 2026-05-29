import contextvars

# Context variable to hold logs for the current request
logs_var = contextvars.ContextVar("logs", default=None)

def add_log(agent_from, agent_to, message, status="info"):
    logs = logs_var.get()
    if logs is not None:
        logs.append({
            "from": agent_from,
            "to": agent_to,
            "message": message,
            "status": status
        })
