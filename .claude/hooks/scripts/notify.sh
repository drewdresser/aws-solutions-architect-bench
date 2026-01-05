#!/bin/bash
# notify.sh
# Sends notifications for important events

EVENT="$1"

# Notification function - customize based on your system
send_notification() {
    local title="$1"
    local message="$2"

    # macOS notification
    if command -v osascript &> /dev/null; then
        osascript -e "display notification \"$message\" with title \"$title\""
    # Linux notification (requires notify-send)
    elif command -v notify-send &> /dev/null; then
        notify-send "$title" "$message"
    # Windows notification (requires powershell)
    elif command -v powershell.exe &> /dev/null; then
        powershell.exe -Command "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null; \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); \$template.GetElementsByTagName('text')[0].AppendChild(\$template.CreateTextNode('$title')); \$template.GetElementsByTagName('text')[1].AppendChild(\$template.CreateTextNode('$message'))"
    fi
}

# Parse event type and send appropriate notification
case "$EVENT" in
    *"error"*)
        send_notification "Claude Code Error" "An error occurred during execution"
        ;;
    *"complete"*)
        send_notification "Claude Code" "Task completed successfully"
        ;;
    *"warning"*)
        send_notification "Claude Code Warning" "A warning was generated"
        ;;
esac

exit 0
