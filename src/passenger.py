
class Passenger:
    def __init__(self, passenger_id, arrival_time):
        self.id = passenger_id
        self.arrival_time = arrival_time

        self.queue_entry_time = None
        self.service_start_time = None
        self.completion_time = None

        self.waiting_time = None
        self.processing_time = None