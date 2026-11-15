# Incident runbook: payments API 5xx spike

1. Restart all payments pods at once with `kubectl delete pods -l app=payments`.
2. Check the dashboard to see if errors went down.
3. If errors continue, roll back the last deploy.
4. Tell the team in Slack.
