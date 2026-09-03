#!/bin/bash

cd /home/parthiv_setu/jijnasa
source .venv/bin/activate

NTFY_TOPIC="jijnasa-parthiv-8x7k29m4-daily"
NTFY_URL="https://ntfy.sh/$NTFY_TOPIC"

echo "=== JIJNASA DAILY NEWS ==="
date

# Run Jijnasa
python -u jijnasa.py news

# Check whether Jijnasa succeeded
if [ $? -eq 0 ]; then
    curl -s \
        -H "Title: 🕉️ Jijnasa Daily News" \
        -H "Priority: default" \
        -H "Tags: newspaper,robot" \
        -d "Your daily technology news analysis is complete. Check your Obsidian vault." \
        "$NTFY_URL"

    echo "📱 Notification sent successfully."
else
    curl -s \
        -H "Title: ⚠️ Jijnasa News Failed" \
        -H "Priority: high" \
        -H "Tags: warning" \
        -d "Jijnasa daily news pipeline failed. Check daily_news.log on the server." \
        "$NTFY_URL"

    echo "⚠️ Failure notification sent."
    exit 1
fi
