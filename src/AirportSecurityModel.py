from .passenger import Passenger

class Model:

    def __init__(
        self,
        arrival_rate=0.4,
        queue_capacity=10,
        num_checkpoints=2,
        processing_time=3,
        simulation_steps=500
    ):

        self.arrival_rate = arrival_rate
        self.queue_capacity = queue_capacity

        self.num_checkpoints = num_checkpoints
        self.processing_time = processing_time
        self.simulation_steps = simulation_steps

        self.queues = [
            [] for _ in range(num_checkpoints)
        ]

        self.in_service = [
            None for _ in range(num_checkpoints)
        ]

        self.remaining_service_time = [
            0 for _ in range(num_checkpoints)
        ]

        self.external_waiting = []

        self.completed_passengers = []
        self.all_passengers = []

        self.next_passenger_id = 0

        self.queue_length_history = []
        self.external_waiting_history = []
