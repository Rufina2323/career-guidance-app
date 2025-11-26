from dataclasses import dataclass, field


@dataclass
class Balance:
    amount: float = field(default=0.0)

    def can_withdraw(self, amount: float) -> bool:
        return 0 <= amount <= self.amount

    def __str__(self) -> str:
        return f"Balance(amount={self.amount:.2f})"
