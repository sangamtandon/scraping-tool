from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message):
        pass

class ConsoleNotifier(Notifier):
    def send_notification(self, message):
        print(message)

class EmailNotifier(Notifier):
    def send_notification(self, message):
        # Implementation for sending notification via email
        pass

class SMSNotifier(Notifier):
    def send_notification(self, message):
        # Implementation for sending notification via SMS
        pass