"""Discrete-time airport security queues with bounded internal waiting areas."""

from numbers import Integral, Real

import numpy as np

from .passenger import Passenger


def _positive_integer(name, value):
    """Validate a positive integer, excluding Boolean values."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral) or value < 1:
        raise ValueError(f"{name} must be a positive integer.")
    return int(value)


class AirportSecurityModel:
    """Simulate Bernoulli arrivals, separate FIFO queues, and parallel screening.

    Queue capacity counts waiting passengers per checkpoint, excluding service.
    Excess demand waits in an unbounded external FIFO area. Time is measured in
    integer steps. Each instance supports one run; use a new instance to repeat.
    """

    def __init__(
        self,
        arrival_rate=0.4,
        queue_capacity=10,
        num_checkpoints=2,
        processing_time=4,
        simulation_steps=5000,
        seed=None,
        processing_time_variation=0,
    ):
        """Validate settings and initialise an empty system and seeded generator.

        arrival_rate must be a finite probability in [0, 1]. Queue capacity,
        checkpoint count, central service duration, and run length must be
        positive integers. Variation must be an integer from zero to one less
        than the central duration, so every sampled duration is positive.
        """
        if (
            isinstance(arrival_rate, (bool, np.bool_))
            or not isinstance(arrival_rate, Real)
            or not np.isfinite(arrival_rate)
            or not 0 <= arrival_rate <= 1
        ):
            raise ValueError("arrival_rate must be a finite number between 0 and 1.")

        self.arrival_rate = float(arrival_rate)
        self.queue_capacity = _positive_integer("queue_capacity", queue_capacity)
        self.num_checkpoints = _positive_integer("num_checkpoints", num_checkpoints)
        self.processing_time = _positive_integer("processing_time", processing_time)
        self.simulation_steps = _positive_integer("simulation_steps", simulation_steps)

        if (
            isinstance(processing_time_variation, (bool, np.bool_))
            or not isinstance(processing_time_variation, Integral)
            or not 0 <= processing_time_variation < self.processing_time
        ):
            raise ValueError(
                "processing_time_variation must be a non-negative integer "
                "smaller than processing_time."
            )
        self.processing_time_variation = int(processing_time_variation)
        self.rng = np.random.default_rng(seed)
        self._has_run = False

        self.queues = [[] for _ in range(self.num_checkpoints)]
        self.in_service = [None for _ in range(self.num_checkpoints)]
        self.remaining_service_time = [0 for _ in range(self.num_checkpoints)]
        self.external_waiting = []
        self.completed_passengers = []
        self.all_passengers = []
        self.next_passenger_id = 0
        self.queue_length_history = []
        self.external_waiting_history = []

    def create_passenger(self, current_time):
        """Generate at most one arrival and admit it behind existing outside waiters."""
        if self.rng.random() < self.arrival_rate:
            passenger = Passenger(self.next_passenger_id, current_time)
            self.next_passenger_id += 1
            self.all_passengers.append(passenger)
            self.assign_queue(passenger, current_time)

    def assign_queue(self, passenger, current_time):
        """Join the external admission FIFO and attempt immediate internal entry."""
        self.external_waiting.append(passenger)
        self.move_external_passengers(current_time)

    def move_external_passengers(self, current_time):
        """Admit outside waiters FIFO, preferring idle then shortest available queues.

        Checkpoint index breaks ties. Immediate service updates checkpoint state
        before the next allocation. Passengers do not switch internal queues.
        """
        while self.external_waiting:
            available_queues = [
                i for i, queue in enumerate(self.queues)
                if len(queue) < self.queue_capacity
            ]
            if not available_queues:
                break
            selected = min(
                available_queues,
                key=lambda i: (
                    self.in_service[i] is not None,
                    len(self.queues[i]),
                    i,
                ),
            )
            passenger = self.external_waiting.pop(0)
            passenger.queue_entry_time = current_time
            self.queues[selected].append(passenger)
            self.start_service(selected, current_time)

    def sample_processing_time(self):
        """Draw a uniform integer duration; fixed service consumes no random draw."""
        if self.processing_time_variation == 0:
            return self.processing_time
        lower = self.processing_time - self.processing_time_variation
        upper = self.processing_time + self.processing_time_variation
        return int(self.rng.integers(lower, upper + 1))

    def start_service(self, checkpoint_id, current_time):
        """Start the next internal FIFO passenger if the checkpoint is idle.

        Waiting time includes external and internal waiting. Service duration
        is sampled once and stored on the passenger for timing checks.
        """
        if self.in_service[checkpoint_id] is None and self.queues[checkpoint_id]:
            passenger = self.queues[checkpoint_id].pop(0)
            passenger.service_start_time = current_time
            passenger.waiting_time = current_time - passenger.arrival_time
            passenger.processing_time = self.sample_processing_time()
            self.in_service[checkpoint_id] = passenger
            self.remaining_service_time[checkpoint_id] = passenger.processing_time

    def process_checkpoints(self, current_time):
        """Advance existing service, record completions, then start internal waiters.

        Newly started service is first advanced on the following time step.
        Internal waiters are served before outside waiters are admitted.
        """
        for i in range(self.num_checkpoints):
            if self.in_service[i] is not None:
                self.remaining_service_time[i] -= 1
                if self.remaining_service_time[i] <= 0:
                    passenger = self.in_service[i]
                    passenger.completion_time = current_time
                    self.completed_passengers.append(passenger)
                    self.in_service[i] = None
            if self.in_service[i] is None:
                self.start_service(i, current_time)

    def record_statistics(self):
        """Record end-of-step waiting counts; exclude passengers in service."""
        self.queue_length_history.append(sum(len(queue) for queue in self.queues))
        self.external_waiting_history.append(len(self.external_waiting))

    def run(self):
        """Run once from time zero without warm-up removal or a drain-down period."""
        if self._has_run:
            raise RuntimeError(
                "This model has already been run. Create a new model instance "
                "to run another simulation."
            )
        self._has_run = True
        for t in range(self.simulation_steps):
            self.process_checkpoints(t)
            self.move_external_passengers(t)
            self.create_passenger(t)
            self.record_statistics()

    def get_results(self):
        """Return completed-passenger waiting and observed internal-queue metrics.

        Waiting statistics are NaN when no passengers have completed. Queue
        statistics are NaN before any steps have been recorded. throughput is
        a completed count, not a rate; external_waiting is a final snapshot.
        """
        waiting_times = [
            p.waiting_time for p in self.completed_passengers
            if p.waiting_time is not None
        ]
        return {
            "average_waiting_time": np.mean(waiting_times) if waiting_times else np.nan,
            "maximum_waiting_time": np.max(waiting_times) if waiting_times else np.nan,
            "average_queue_length": (
                np.mean(self.queue_length_history) if self.queue_length_history else np.nan
            ),
            "maximum_queue_length": (
                np.max(self.queue_length_history) if self.queue_length_history else np.nan
            ),
            "throughput": len(self.completed_passengers),
            "external_waiting": len(self.external_waiting),
        }
