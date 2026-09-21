# Airport Security Queue Model

## Project Overview

This project investigates passenger congestion and waiting behaviour in an airport security screening system.

Passengers arrive at the security area, join a queue, wait for an available checkpoint, undergo security screening, and then leave the system.

The aim of this project is to investigate how different system parameters affect queue length, passenger waiting time, throughput, and overall system stability.

---

## Research Question

**How do passenger demand, queue capacity, processing time, and the number of security checkpoints affect passenger waiting time and congestion in an airport security screening system?**

More specifically, we investigate four main parameters:

1. Passenger arrival rate
2. Queue capacity
3. Passenger processing time variation
4. Number of security checkpoints

---

## Modelling Approach

The system will be implemented as a discrete-time agent-based simulation.

Each passenger is represented as an individual agent.

A passenger may have attributes such as:

- arrival time
- queue entry time
- service start time
- processing time
- waiting time
- completion time

Security checkpoints act as service resources that process passengers.

At every simulation time step:

1. New passengers may arrive.
2. Passengers join the queue if queue capacity is available.
3. If a security checkpoint is free, the next passenger enters screening.
4. Each passenger requires a certain amount of processing time.
5. After screening is completed, the passenger leaves the system.
6. Queue length, waiting time, throughput, and rejected passengers are recorded.

---

## Main Parameters

### 1. Passenger Arrival Rate

The passenger arrival rate represents how frequently new passengers enter the security system.

Different arrival rates will be tested to investigate how increasing passenger demand affects:

- queue length
- waiting time
- throughput
- system congestion

Example values may include:

- low arrival rate
- medium arrival rate
- high arrival rate

or numerical probabilities such as:

- 0.2 passengers per time step
- 0.4 passengers per time step
- 0.6 passengers per time step
- 0.8 passengers per time step

---

### 2. Queue Capacity

Queue capacity represents the maximum number of passengers that can wait in the security queue.

Different queue capacities will be tested to investigate how limited waiting space affects the system.

If the queue reaches maximum capacity, newly arriving passengers may be unable to enter the queue.

Possible measurements include:

- number of passengers rejected
- maximum queue length
- average waiting time
- system throughput

---

### 3. Passenger Processing Time Variation

Passenger processing time represents how long each passenger requires at a security checkpoint.

Instead of assuming that every passenger takes exactly the same amount of time, processing time may vary between passengers.

For example:

- Fixed processing time:
  - every passenger requires 3 time steps

- Low variation:
  - processing time randomly varies between 2–4 time steps

- High variation:
  - processing time randomly varies between 1–6 time steps

This experiment will investigate whether greater variation in passenger processing time increases queue length and waiting time.

---

### 4. Number of Security Checkpoints

The number of active security checkpoints determines the processing capacity of the airport security system.

Experiments may compare:

- 1 checkpoint
- 2 checkpoints
- 3 checkpoints
- 4 checkpoints

The aim is to investigate how increasing the number of checkpoints affects:

- passenger waiting time
- queue length
- throughput

This parameter may also be investigated together with processing time variation.

---

## Experimental Design

The project will investigate the four main parameters through controlled experiments.

Where possible, one parameter will be varied while the other parameters are held constant.

### Experiment A — Passenger Arrival Rate

Vary passenger arrival rate while keeping:

- queue capacity constant
- number of checkpoints constant
- processing time constant

Measure:

- average waiting time
- average queue length
- maximum queue length
- throughput

---

### Experiment B — Queue Capacity

Vary maximum queue capacity while keeping other parameters constant.

Measure:

- number of passengers rejected
- average waiting time
- throughput
- queue utilisation

---

### Experiment C — Passenger Processing Time Variation

Compare different levels of passenger processing time variation while keeping:

- arrival rate constant
- queue capacity constant
- number of checkpoints constant

Measure:

- average waiting time
- maximum waiting time
- average queue length
- throughput

---

### Experiment D — Number of Security Checkpoints

Vary the number of checkpoints while keeping other parameters constant.

Measure:

- average waiting time
- average queue length
- throughput

---

## Combined Parameter Analysis

After analysing individual parameters, selected parameter combinations may also be investigated.

For example:

### Processing Time Variation × Number of Checkpoints

This experiment will investigate whether increasing the number of checkpoints can compensate for unpredictable passenger processing times.

### Arrival Rate × Queue Capacity

This experiment will investigate how queue capacity affects system performance under different passenger demand levels.

---

## Output Measures

The main quantitative measurements will include:

- Average passenger waiting time
- Maximum passenger waiting time
- Average queue length
- Maximum queue length
- Passenger throughput
- Number of passengers successfully processed
- Number of passengers unable to join the queue

Simulation results will be visualised using graphs and summary statistics.

---

## Project Structure

```text
project-root/
|
+-- src/                  # Main simulation code, models, classes, functions
|
+-- utils/                # Helper and utility functions
|
+-- data/                 # Generated datasets or sample simulation results
|
+-- notebooks/            # Jupyter Notebooks for experiments, analysis and demonstrations
|
+-- requirements.txt      # Python dependencies
|
+-- README.md             # Project overview, setup instructions and usage guide