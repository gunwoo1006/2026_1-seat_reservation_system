class SeatStore:
    """좌석 예약 상태를 메모리에서 관리하는 클래스."""

    def __init__(self, seat_ids):
        """좌석 번호 목록을 받아 모든 좌석을 빈 상태로 초기화한다."""
        # 좌석 번호를 key로 사용하고, 예약자가 없으면 None을 저장한다.
        self._seats = {seat_id: None for seat_id in seat_ids}

    def list_seats(self):
        """전체 좌석의 예약 상태를 반환한다."""
        return self._seats.items()

    def available_seats(self):
        """예약되지 않은 좌석 목록만 반환한다."""
        return [
            (seat_id, name)
            for seat_id, name in self._seats.items()
            if name is None
        ]

    def reserved_seats(self):
        """예약된 좌석 목록만 반환한다."""
        return [
            (seat_id, name)
            for seat_id, name in self._seats.items()
            if name is not None
        ]

    def reserve(self, seat_id, name):
        """지정한 좌석을 주어진 이름으로 예약한다."""
        current = self._get(seat_id)

        if current is not None:
            raise ValueError("Seat is already reserved.")

        # 예약 가능한 좌석이면 None 대신 예약자 이름을 저장한다.
        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        """지정한 좌석의 예약을 취소한다."""
        current = self._get(seat_id)

        if current is None:
            raise ValueError("Seat is not reserved.")

        # 이름이 입력된 경우, 예약자 이름이 일치할 때만 취소한다.
        if name and current != name:
            raise ValueError("Name does not match the reservation.")

        # 예약 취소 상태는 다시 None으로 표시한다.
        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        """지정한 좌석의 현재 예약 상태를 반환한다."""
        return seat_id, self._get(seat_id)

    def stats(self):
        """전체 좌석 수, 예약 좌석 수, 빈 좌석 수를 반환한다."""
        reserved = sum(
            1
            for name in self._seats.values()
            if name is not None
        )
        total = len(self._seats)

        return {
            "total": total,
            "reserved": reserved,
            "available": total - reserved,
        }

    def _get(self, seat_id):
        """좌석 번호가 존재하는지 확인한 뒤 해당 좌석 상태를 반환한다."""
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")

        return self._seats[seat_id] 