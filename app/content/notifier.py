import os
import requests


NTFY_TOPIC = os.getenv(
    "NTFY_TOPIC",
    "jijnasa-parthiv-8x7k29m4-daily",
)

NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"


def send_notification(
    title: str,
    message: str,
    tags: str = "newspaper",
):
    """Send a notification to the user's phone using ntfy."""

    try:
        # HTTP headers must use ASCII-safe text.
        safe_title = title.encode(
            "ascii",
            "ignore",
        ).decode()

        response = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title": safe_title,
                "Priority": "3",
                "Tags": tags,
            },
            timeout=10,
        )

        response.raise_for_status()

        print(
            "📱 Notification sent successfully.",
            flush=True,
        )

        return True

    except Exception as error:
        print(
            f"⚠️ Notification failed: {error}",
            flush=True,
        )

        return False
