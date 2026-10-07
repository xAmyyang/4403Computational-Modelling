"""Boundary and behavioural checks for the airport security model."""

import unittest
import warnings

import numpy as np

from src.model import AirportSecurityModel
from src.passenger import Passenger


class ModelTests(unittest.TestCase):
    def test_invalid_arrival_probabilities(self):
        for value in [-0.1, 1.1, np.nan, np.inf, -np.inf, True, np.bool_(False), "0.4", None]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "arrival_rate"):
                    AirportSecurityModel(arrival_rate=value)

    def test_positive_integer_parameters(self):
        for name in ["queue_capacity", "num_checkpoints", "processing_time", "simulation_steps"]:
            for value in [0, -1, 1.5, True, np.bool_(True), "2", None]:
                with self.subTest(parameter=name, value=value):
                    with self.assertRaisesRegex(ValueError, name):
                        AirportSecurityModel(**{name: value})
        model = AirportSecurityModel(queue_capacity=np.int64(2), simulation_steps=np.int64(10))
        self.assertEqual(model.queue_capacity, 2)
        self.assertEqual(model.simulation_steps, 10)

    def test_invalid_variation(self):
        for value in [-1, 4, 5, 1.5, True, np.bool_(False), "1", None]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "processing_time_variation"):
                    AirportSecurityModel(processing_time=4, processing_time_variation=value)

    def test_empty_observation_and_no_arrivals(self):
        model = AirportSecurityModel(arrival_rate=0, simulation_steps=10, seed=42)
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            before = model.get_results()
            self.assertTrue(np.isnan(before["average_queue_length"]))
            self.assertTrue(np.isnan(before["maximum_queue_length"]))
            model.run()
            after = model.get_results()
        self.assertEqual(len(model.all_passengers), 0)
        self.assertEqual(after["throughput"], 0)
        self.assertEqual(after["average_queue_length"], 0)
        self.assertEqual(after["maximum_queue_length"], 0)
        self.assertTrue(np.isnan(after["average_waiting_time"]))
        self.assertTrue(np.isnan(after["maximum_waiting_time"]))

    def test_no_completions_is_not_zero_waiting(self):
        model = AirportSecurityModel(arrival_rate=1, simulation_steps=2, num_checkpoints=1)
        model.run()
        self.assertEqual(len(model.all_passengers), 2)
        self.assertEqual(len(model.completed_passengers), 0)
        self.assertEqual(len(model.queues[0]), 1)
        self.assertTrue(np.isnan(model.get_results()["average_waiting_time"]))

    def test_known_fixed_service_timing(self):
        model = AirportSecurityModel(arrival_rate=1, num_checkpoints=1, processing_time=4,
                                     simulation_steps=10, seed=42)
        model.run()
        self.assertEqual(
            [(p.id, p.service_start_time, p.completion_time, p.waiting_time)
             for p in model.completed_passengers],
            [(0, 0, 4, 0), (1, 4, 8, 3)],
        )
        self.assertEqual(model.in_service[0].id, 2)
        self.assertEqual(model.in_service[0].service_start_time, 8)

    def test_conservation_capacity_and_timing_at_every_step(self):
        test = self

        class CheckedModel(AirportSecurityModel):
            def record_statistics(self):
                super().record_statistics()
                members = (
                    self.completed_passengers + self.external_waiting
                    + [p for queue in self.queues for p in queue]
                    + [p for p in self.in_service if p is not None]
                )
                test.assertEqual(len(members), len(self.all_passengers))
                test.assertEqual(len({p.id for p in members}), len(self.all_passengers))
                test.assertTrue(all(len(q) <= self.queue_capacity for q in self.queues))
                for p in self.completed_passengers:
                    test.assertLessEqual(p.arrival_time, p.queue_entry_time)
                    test.assertLessEqual(p.queue_entry_time, p.service_start_time)
                    test.assertEqual(p.completion_time - p.service_start_time, p.processing_time)
                    test.assertEqual(p.waiting_time, p.service_start_time - p.arrival_time)
                    test.assertGreaterEqual(p.processing_time, 1)
                    test.assertLessEqual(p.processing_time, 7)

        for capacity in [1, 4]:
            with self.subTest(capacity=capacity):
                model = CheckedModel(arrival_rate=1, queue_capacity=capacity, num_checkpoints=2,
                                     processing_time_variation=3, simulation_steps=200, seed=42)
                model.run()
                self.assertGreater(len(model.external_waiting), 0)

    def test_external_admission_preserves_fifo(self):
        model = AirportSecurityModel(num_checkpoints=1, queue_capacity=1, processing_time=2)
        for passenger_id in range(3):
            model.assign_queue(Passenger(passenger_id, 0), 0)
        model.assign_queue(Passenger(3, 1), 1)
        self.assertEqual([p.id for p in model.external_waiting], [2, 3])
        model.process_checkpoints(1)
        model.move_external_passengers(1)
        model.process_checkpoints(2)
        model.move_external_passengers(2)
        self.assertEqual(model.in_service[0].id, 1)
        self.assertEqual([p.id for p in model.queues[0]], [2])
        self.assertEqual([p.id for p in model.external_waiting], [3])

    def test_repeat_run_is_rejected_without_changing_state(self):
        model = AirportSecurityModel(simulation_steps=10, seed=42)
        model.run()
        before = (len(model.all_passengers), list(model.queue_length_history))
        with self.assertRaisesRegex(RuntimeError, "already been run"):
            model.run()
        self.assertEqual(before, (len(model.all_passengers), model.queue_length_history))

    def test_seed_reproduces_passenger_records_and_histories(self):
        models = [AirportSecurityModel(arrival_rate=0.7, simulation_steps=200,
                                       processing_time_variation=3, seed=42) for _ in range(2)]
        for model in models:
            model.run()
        self.assertEqual([vars(p) for p in models[0].all_passengers],
                         [vars(p) for p in models[1].all_passengers])
        self.assertEqual(models[0].queue_length_history, models[1].queue_length_history)
        self.assertEqual(models[0].external_waiting_history, models[1].external_waiting_history)

    def test_explicit_duration_overrides_default(self):
        self.assertEqual(AirportSecurityModel().processing_time, 4)
        model = AirportSecurityModel(processing_time=3, arrival_rate=1, simulation_steps=10)
        model.run()
        durations = [p.processing_time for p in model.all_passengers
                     if p.processing_time is not None]
        self.assertTrue(durations)
        self.assertTrue(all(duration == 3 for duration in durations))


if __name__ == "__main__":
    unittest.main()
