# ======================= SERVICE MESSAGES =================================
# such messages are not shown to the user and are not stored in the database.
# They are only needed to update data on the client side of the application in real time.


# SERVICE MESSAGE that is sent to the user when he changes his avatar
USER_UPDATED_AVATAR_NOTIFICATION_TYPE: str = "user_updated_avatar"

# SERVICE MESSAGE that is sent to the user when he becomes offline
USER_OFFLINE_NOTIFICATION_TYPE: str = "user_offline"

# SERVICE MESSAGE that is sent to the user when he becomes online
USER_ONLINE_NOTIFICATION_TYPE: str = "user_online"

# =================================================================================