from django.db import models

class ReceiptBookDeposit(models.Model):
    MONTH_CHOICES = [
        ("April", "APRIL"),
        ("May", "MAY"),
        ("June", "JUNE"),
        ("July", "JULY"),
        ("August", "AUGUST"),
        ("September", "SEPTEMBER"),
        ("October", "OCTOBER"),
        ("November", "NOVEMBER"),
        ("December", "DECEMBER"),
        ("January", "JANUARY"),
        ("February", "FEBRUARY"),
        ("March", "MARCH"),
    ]

    YEAR_CHOICES = [
        ("23-24", "23-24"),
        ("24-25", "24-25"),
        ("25-26", "25-26"),
    ]

    def get_next_code():
        last = ReceiptBookDeposit.objects.order_by('-id').first()
        if last and last.code.startswith('LN'):
            try:
                last_num = int(last.code[2:])
            except ValueError:
                last_num = 0
        else:
            last_num = 0
        return f'LN{last_num + 1:04d}'

    code = models.CharField(max_length=20, unique=True, blank=True)
    member_name = models.CharField(max_length=100)
    member_mobile = models.CharField(max_length=20)
    date = models.DateField()
    month = models.CharField(max_length=20, choices=MONTH_CHOICES, default="April")
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default="24-25")
    debit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    narration = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)  # <--- Added field for soft delete (1=active, -1=removed)

    def save(self, *args, **kwargs):
        # Auto-generate code if not set
        if not self.code:
            self.code = ReceiptBookDeposit.get_next_code()
        self.total_amount = self.debit_amount + self.credit_amount
        self.pending_amount = self.credit_amount - self.debit_amount
        self.closing_balance = self.total_amount - self.pending_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.member_name}"