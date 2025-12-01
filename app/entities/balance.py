from dataclasses import dataclass, field


@dataclass
class Balance:
    amount: float = field(default=0.0)

    def __str__(self) -> str:
        return f"Balance(amount={self.amount:.2f})"
