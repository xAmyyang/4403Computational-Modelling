# Airport Security Queue Model

## Project Overview

This project investigates passenger congestion and waiting behaviour in an airport security screening system.

Instead of modelling traffic flow, we model passengers as individual agents who arrive at an airport security area, join a queue, wait for an available checkpoint, undergo security screening, and then leave the system.

The aim of the project is to investigate how passenger demand and security service capacity affect queue formation and waiting time.

---

## Research Question

**How do passenger arrival rate and the number of security checkpoints affect queue length and passenger waiting time in an airport security screening system?**

Possible extension:

**How do random additional screening delays affect the stability and efficiency of the queue?**

---

## Modelling Approach

We plan to use an **agent-based / discrete-time simulation**.

Each passenger is represented as an individual agent.

Each passenger may have attributes such as:

- arrival time
- queue entry time
- service start time
- service duration
- waiting time
- whether additional screening is required

Security checkpoints act as service resources that process passengers.

The simulation will evolve over discrete time steps.

---

## Model Rules

At each time step:

1. New passengers may arrive according to a defined arrival probability or arrival rate.
2. Newly arrived passengers join the security queue.
3. If a security checkpoint is available, the next passenger in the queue begins screening.
4. Each checkpoint can process one passenger at a time.
5. Screening requires a defined amount of service time.
6. Some passengers may require additional screening, creating a random delay.
7. After screening is completed, the passenger leaves the system.
8. Queue length, waiting time, and throughput are recorded.

---

## Main Parameters

The main parameters we plan to investigate are:

- **Passenger arrival rate**
- **Number of security checkpoints**

Additional parameters may include:

- service time
- probability of additional screening
- additional screening duration

To keep the project manageable, the initial experiments will focus mainly on passenger arrival rate and number of checkpoints.

---

## Output Measures

We plan to measure:

- average passenger waiting time
- maximum passenger waiting time
- average queue length
- maximum queue length
- passenger throughput
- number of passengers processed

These measurements will allow us to compare system performance under different conditions.

---

## Experimental Plan

We will systematically vary the passenger arrival rate and number of available checkpoints.

For example:

### Passenger arrival rate

- Low
- Medium
- High

or numerical values such as:

- 0.2 passengers per time step
- 0.4 passengers per time step
- 0.6 passengers per time step
- 0.8 passengers per time step

### Number of checkpoints

- 1 checkpoint
- 2 checkpoints
- 3 checkpoints
- 4 checkpoints

For each combination of parameters, the simulation will be repeated multiple times because passenger arrivals and delays may be stochastic.

We will compare the average results across repeated simulations.

---

## Expected Investigation

We expect that increasing passenger arrival rate will increase queue length and waiting time.

Increasing the number of checkpoints should increase service capacity and reduce congestion.

However, we are particularly interested in whether there is a point where passenger arrival demand becomes greater than the processing capacity of the system, causing the queue to continuously grow.

This may reveal a transition between:

- a stable queueing system, where passengers are processed fast enough, and
- an overloaded system, where the queue continues to increase.

---

## Originality and Contribution

Airport security queueing is not being modelled as a traffic-flow cellular automaton.

Our model focuses on:

- stochastic passenger arrivals,
- individual passenger waiting times,
- service capacity,
- multiple security checkpoints,
- random additional screening delays.

Our contribution is to investigate how these factors interact and how changes in passenger demand and checkpoint capacity affect the stability and efficiency of the airport security queue.

We may further extend the model by comparing different queue-management strategies, such as:

- one shared queue for all checkpoints, and
- separate queues for individual checkpoints.

---

## Project Structure

```text
airport-security-queue/
│
├── README.md
├── src/
│   └── model.py
│
├── experiments/
│   └── experiments.ipynb
│
├── results/
│   ├── figures/
│   └── data/
│
└── report/