from django.core.management.base import BaseCommand
from books.models import WishList
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Check wish list and notify users when a wish-listed book becomes available'

    def handle(self, *args, **kwargs):
        wish_list_items = WishList.objects.all()

        for item in wish_list_items:
            if item.book.stock_quantity > 0:
                message = (
                    f"Dear {item.user.username},\n\n"
                    f"The book '{item.book.title}' you added to your wish list is now available for borrowing.\n\n"
                    f"Visit our website to reserve the book now!\n\n"
                    f"Thank you for using our library service."
                )

                send_mail(
                    subject='Your wish-listed book is now available!',
                    message=message,
                    from_email='library@gmail.com',
                    recipient_list=[item.user.email]
                )

                item.delete()

                self.stdout.write(
                    self.style.SUCCESS(f"Notified {item.user.email} about the availability of {item.book.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"{item.book.title} is still not available"))
