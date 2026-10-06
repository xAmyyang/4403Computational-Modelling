"""Passenger records used by the shared security-queue model."""


class Passenger:
    """Store one passenger's identity, service duration, and event times.

    Event times and duration remain None until assigned. waiting_time measures
    arrival to service start, including both external and internal waiting.
    """

    def __init__(self, passenger_id, arrival_time):
        """Create a newly arrived passenger with no queue or service assignment."""
        self.id = passenger_id
        self.arrival_time = arrival_time
        self.queue_entry_time = None
        self.service_start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.processing_time = None
