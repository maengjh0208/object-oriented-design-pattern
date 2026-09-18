class LegacyGateway:
    """서드파티 결제 라이브러리. 코드 수정 불가하다고 가정한다."""

    def make_payment(self, amount_in_cents: int, currency: str):
        if amount_in_cents <= 0:
            return {
                "success": False,
                "error": "invalid amount",
            }

        return {
            "success": True,
            "charged_cents": amount_in_cents,
            "currency": currency,
        }
