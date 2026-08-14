import json
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import BadRequestException
from app.models.payment_event import PaymentEvent


class PaymentEventService:
    @staticmethod
    def process(db: Session, data):
        existing = db.query(PaymentEvent).filter(PaymentEvent.event_id == data.event_id).first()
        if existing:
            return existing, False
        event = PaymentEvent(
            provider=data.provider,
            event_id=data.event_id,
            event_type=data.event_type,
            payload=json.dumps(data.payload) if data.payload else None,
            processed_at=datetime.utcnow(),
        )
        try:
            db.add(event)
            db.commit()
            db.refresh(event)
            return event, True
        except IntegrityError:
            db.rollback()
            existing = db.query(PaymentEvent).filter(PaymentEvent.event_id == data.event_id).first()
            if existing:
                return existing, False
            raise BadRequestException("Payment webhook could not be processed safely.")
