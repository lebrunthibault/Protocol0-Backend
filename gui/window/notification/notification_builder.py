from gui.window.decorators.auto_close_window_decorator import AutoCloseNotificationDecorator
from gui.window.decorators.unique_window_decorator import UniqueWindowDecorator
from gui.window.notification.notification_error import NotificationError
from gui.window.notification.notification_info import NotificationInfo
from gui.window.notification.notification_warning import NotificationWarning
from gui.window.window import Window
from gui.window.window_builder import WindowBuilder
from lib.enum.NotificationEnum import NotificationEnum


class NotificationBuilder(WindowBuilder):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum) -> Window:
        if notification_enum == NotificationEnum.INFO:
            notification = NotificationInfo(message=message)
            notification = AutoCloseNotificationDecorator(notification)
        elif notification_enum == NotificationEnum.WARNING:
            notification = NotificationWarning(message=message)
            notification = AutoCloseNotificationDecorator(notification)
        elif notification_enum == NotificationEnum.ERROR:
            notification = NotificationError(message=message)
        else:
            raise NotImplementedError

        notification = UniqueWindowDecorator(notification)
        return notification