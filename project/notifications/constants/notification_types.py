
# the notification type that is sent to all 
# users when the type of technical work changed
CHANGE_MAINTENANCE_NOTIFICATION_TYPE: str = "change_maintenance"


# ======================= SERVICE MESSAGES =================================
# such messages are not shown to the user and are not stored in the database.
# They are only needed to update data on the client side of the application in real time.


# SERVICE MESSAGE that is sent to the user when he deletes his notifications
NOTIFICATIONS_BULK_DELETE_NOTIFICATION_TYPE: str = "bulk_notifications_delete"

# SERVICE MESSAGE that is sent to the user when he reads his notifications
NOTIFICATIONS_BULK_READ_NOTIFICATION_TYPE: str = "bulk_notifications_read"

# SERVICE MESSAGE that is sent to the user when he deletes all his notifications
ALL_USER_NOTIFICATIONS_DELETED_NOTIFICATION_TYPE: str = "all_user_notifications_deleted"

# SERVICE MESSAGE that is sent to the user when he reads all his notifications
ALL_USER_NOTIFICATIONS_READED_NOTIFICATION_TYPE: str = "all_user_notifications_readed"

# ================================================================================