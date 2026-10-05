# Airport Security Queue Model

A discrete-time, agent-based simulation of passengers arriving at airport security, waiting in queues, and being screened by parallel checkpoints. The project investigates how demand, waiting-space limits, and service capacity affect congestion and passenger waiting time.

## Research Question

**How do passenger arrival probability, queue capacity, service-time variation, and the number of security checkpoints affect waiting time, queue lengths, and throughput?**

Time is measured in abstract simulation steps, not seconds or minutes. The model is a simplified computational experiment, not a calibrated forecast for a specific airport.

## Current Experiments

| Notebook | Purpose | Current coverage |
| --- | --- | --- |
| [airport_security_model.ipynb](notebooks/airport_security_model.ipynb) | Model demonstration and validation | Baseline, low/high arrival examples, reproducibility and service-duration checks |
| [processing_time_analysis.ipynb](notebooks/processing_time_analysis.ipynb) | Processing-time variation | Fixed, low, and high variation; 30 seeds per scenario; summaries and comparison figures |
| [checkpoint_analysis.ipynb](notebooks/checkpoint_analysis.ipynb) | Number of checkpoints | 1–4 checkpoints; 30 seeds per scenario; summaries and comparison figures |
| [passenger_arrival_rate_analysis.ipynb](notebooks/passenger_arrival_rate_analysis.ipynb) | Passenger arrival rate | 0.2, 0.3, 0.4 and 0.5 arrival probabilities; 30 seeds per scenario; summaries and comparison figures |
| [queue_capacity_analysis.ipynb](notebooks/queue_capacity_analysis.ipynb) | Queue capacity | 1–4 waiting passengers per checkpoint; 30 seeds per scenario; summaries and comparison figures |
| [arrival_variation_analysis.ipynb](notebooks/arrival_variation_analysis.ipynb) | Arrival probability × service-time variation | Full 3 × 3 design; 30 seeds per combination; interaction plots, congestion measures, and CSV exports |

Four single-factor parameter studies are complete: service-time variation, checkpoint count, arrival probability, and queue capacity. They contain 450 simulation runs in total (90, 120, 120, and 120 respectively), with some baseline settings shared across studies. The low/high arrival examples in the demonstration notebook are separate from the completed repeated-run arrival study. One combined-parameter study is also complete: arrival probability × service-time variation, with 270 runs. The five parameter-study notebooks therefore contain 720 runs in total, including repeated baseline settings across studies; these are not 720 distinct parameter combinations or independent pieces of evidence. Observation-length sensitivity and additional combined-parameter studies remain planned work.

## How the Model Works

Each passenger has an arrival time, queue-entry time, service-start time, assigned service duration, completion time, and waiting time. Each checkpoint serves one passenger at a time and has its own FIFO internal queue. An unbounded external FIFO waiting area holds passengers when all internal queues are full.

At each time step, the model:

1. Advances existing service and records completed passengers. Freed checkpoints start serving their internal queues first.
2. Admits existing external waiters to available internal queues.
3. Generates at most one new passenger with the configured arrival probability. The new passenger enters the same admission process, behind existing external waiters.
4. Records internal queue length and external waiting-area occupancy.

Allocation prefers an idle checkpoint, then the shortest available internal queue; checkpoint index breaks ties. Service begins immediately when possible. A service started at time `t` is first advanced at `t + 1`. Passengers already assigned to an internal queue do not switch queues.

The current model does not reject passengers or implement a separate additional-screening event. Service-duration variation represents different screening durations directly. External admission is FIFO, but service order across separate checkpoint queues is not globally FIFO.

## Parameters

| Parameter | Meaning | Model default |
| --- | --- | ---: |
| `arrival_rate` | Probability of one arrival per step, between 0 and 1; also expected arrivals per step | 0.4 |
| `queue_capacity` | Maximum waiting passengers per internal queue, excluding the passenger in service | 10 |
| `num_checkpoints` | Number of parallel checkpoints and internal queues | 2 |
| `processing_time` | Central service duration, a positive integer | 4 |
| `processing_time_variation` | Integer half-range of service durations, from 0 to `processing_time - 1` | 0 |
| `simulation_steps` | Number of observation steps | 5000 |
| `seed` | Random seed; `None` leaves runs non-reproducible | `None` |

With central duration `m` and variation `v`, service duration is sampled uniformly from the integers `m-v` through `m+v`, inclusive. When `v=0`, duration is fixed. Use positive integers for queue capacity, checkpoint count, and simulation length; not all invalid parameter values are currently checked by the model.

All four repeated-run experiments use 5,000 steps and seeds 0–29. The shared baseline is arrival probability 0.4, queue capacity 10 per checkpoint, two checkpoints, and fixed service duration 4. Each study varies one factor while retaining the other baseline settings:

| Study | Values tested | Simulation runs |
| --- | --- | ---: |
| Service-time variation | `v=0,1,3`, with expected duration 4 in each case | 90 |
| Checkpoint count | 1, 2, 3, 4 | 120 |
| Arrival probability | 0.2, 0.3, 0.4, 0.5 | 120 |
| Queue capacity per checkpoint | 1, 2, 3, 4 waiting passengers | 120 |

The combined study crosses arrival probabilities `0.30, 0.40, 0.48` with service-time variations `0, 1, 3`: nine combinations × 30 seeds = 270 runs. It retains two checkpoints, queue capacity 10 per checkpoint, expected service duration 4, and 5,000 observation steps. Nominal load ratios are 0.60, 0.80, and 0.96; all are below capacity, with the highest close to the limit. It reruns all combinations independently of the other notebooks and preserves the shared model's random-number behaviour. Matching seed labels does not guarantee matched arrivals across service-variation settings.

In the saved combined-study results, the mean waiting gap between high-variation and fixed service increases from about 0.346 steps at arrival probability 0.30 to 0.943 at 0.40 and 4.656 at 0.48. This is a descriptive interaction on the additive waiting-time scale, not a claim of statistical significance or steady-state convergence. The notebook also reports queues, throughput, and unfinished passengers.

## Setup and Running

The current experiments and figures were checked with Python 3.13. The direct dependencies are pinned in `requirements.txt`; this is not a complete transitive dependency lockfile.

From the project root, create and activate an environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, create the environment with `python -m venv .venv`, then activate it in PowerShell with `.venv\Scripts\Activate.ps1` before installing the requirements.

Open the project folder in VS Code with its Python and Jupyter extensions installed. Open a notebook, select the `.venv` Python environment as its kernel, then choose **Restart Kernel** and **Run All**. `ipykernel` supplies the Python kernel; a standalone JupyterLab server is not included in these requirements.

Recommended reading order:

1. `airport_security_model.ipynb` for the baseline and validation checks.
2. `processing_time_analysis.ipynb` for service-duration variation.
3. `checkpoint_analysis.ipynb` for checkpoint capacity.
4. `passenger_arrival_rate_analysis.ipynb` for passenger arrival rate.
5. `queue_capacity_analysis.ipynb` for queue capacity.
6. `arrival_variation_analysis.ipynb` for the combined effect of demand and service-time variation.

The notebooks import the shared model from `src/` and can be run independently. Saved outputs include comparison figures; rerun all cells to regenerate them. Restart the kernel after editing the model. Use a new model instance for each simulation: calling `run()` twice on the same instance raises an error.

### Minimal Model Example

Run this example from the project root:

```python
from src.model import AirportSecurityModel

model = AirportSecurityModel(
    arrival_rate=0.4,
    queue_capacity=10,
    num_checkpoints=2,
    processing_time=4,
    processing_time_variation=1,
    simulation_steps=5000,
    seed=42,
)
model.run()
results = model.get_results()
print(results)
```

## Measures and Interpretation

| Measure | Definition |
| --- | --- |
| Completed-passenger mean waiting time | Arrival-to-service-start duration, averaged over passengers who complete screening within the observation period |
| Mean internal queue length | Time average of the total waiting across internal queues; excludes service and external waiting |
| Mean external queue length | Time average of external waiting-area occupancy |
| Throughput rate | Completed passengers divided by simulation steps |
| Unfinished passengers | Passengers still waiting internally, waiting externally, or in service when the simulation ends |

`model.get_results()["throughput"]` is a **completed count**, not a rate. Its `external_waiting` field is a **final external count**, not cumulative admissions or rejections. The analysis notebooks compute time averages, throughput rates, and unfinished counts explicitly. The checkpoint, service-variation, and combined arrival-variation notebooks treat waiting-time means with no completed passengers as undefined. The arrival and queue-capacity notebooks currently use the basic `get_results()` method, which returns zero in that case; those two notebooks therefore need an explicit undefined-value check before using scenarios with no completions. All runs in the current five parameter studies have completed passengers.

Scenario summaries give each run equal weight. Waiting-time error bars show one standard deviation **between run means**, not individual-passenger dispersion or confidence intervals. Other comparison panels show means or descriptive differences between scenario means only; the combined-study waiting-gap plot does not include uncertainty bars. Figures and numeric labels are generated from simulation results, not manually entered values.

### Nominal Capacity and Finite-Horizon Results

Nominal service capacity is `num_checkpoints / expected_service_duration` passengers per step. The nominal load ratio is expected arrival demand divided by this capacity. This comparison identifies spare capacity, critical load, or overload; it does not by itself establish steady-state behaviour from a finite simulation.

| Scenario | Expected arrivals / step | Nominal service capacity / step | Nominal load ratio | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Baseline: two checkpoints, fixed duration 4 | 0.4 | 0.5 | 0.8 | Demand below nominal capacity |
| Arrival study: two checkpoints, arrival probability 0.5 | 0.5 | 0.5 | 1.0 | Critical load: no spare nominal capacity |
| Checkpoint study: one checkpoint, arrival probability 0.4 | 0.4 | 0.25 | 1.6 | Overload: demand exceeds capacity |

At critical load, random arrival fluctuations can produce substantial queues even though expected demand equals nominal capacity. The saved arrival-study result of about 34.02 steps of completed-passenger waiting and 28.30 unfinished passengers describes a 5,000-step observation, not a stable long-run waiting-time estimate. The nominal capacity boundary is known from the model parameters; denser arrival settings would describe the response near that boundary rather than locate a previously unknown capacity.

In the overloaded one-checkpoint scenario, the saved mean wait of about 932.85 steps excludes the unfinished backlog (about 748.30 passengers at the end). Its value depends on the observation horizon. Longer runs or warm-up removal cannot turn this overloaded scenario into a stable system. Internal queue lengths can level off at their limits while the unbounded external queue continues to accumulate passengers.

## Assumptions and Limitations

- **Finite observation period:** simulations start empty, with no warm-up exclusion or drain-down. Results are not established steady-state estimates.
- **Unfinished passengers:** completed-only waiting statistics omit unfinished journeys and can understate congestion. Read them alongside external queues and unfinished counts, especially in overloaded scenarios.
- **Critical arrival demand:** arrival probability 0.5 with two fixed-duration, four-step checkpoints equals nominal service capacity. Random arrivals still create congestion; the 5,000-step results are not established steady-state estimates.
- **One-checkpoint overload:** with fixed four-step service, one checkpoint has nominal capacity 0.25 passengers per step versus demand 0.4. Its backlog grows and its reported waiting time depends on the observation horizon.
- **Capacity changes together:** adding checkpoints also adds internal queues of capacity 10. The checkpoint experiment represents adding checkpoints with associated waiting space, not changing service capacity at fixed total waiting space.
- **Arrival limit:** at most one passenger arrives per step. With four checkpoints and fixed four-step service, the model permits immediate service for every arrival. Zero waiting under these assumptions is not a general airport prediction.
- **Randomness:** one generator drives both arrival and service sampling. Matching seeds gives reproducible scenarios, but does not guarantee matched arrivals when service-time variation changes. With fixed service times, matched seeds yield the same arrivals across checkpoint counts.
- **Scope:** there is no abandonment, rejection, priority screening, queue switching, checkpoint breakdown, or explicit secondary screening.

Planned extensions include denser arrival-probability settings near nominal capacity and settings above it, additional combined-parameter studies such as service-variation × checkpoint-count comparisons, and sensitivity checks for simulation length and observation policy. Warm-up exclusion would be assessed for below-capacity scenarios. Stopping arrivals and draining the remaining passengers would measure waiting for a finite arrival cohort; it would not establish steady state under overload.

## Project Structure

```text
project-root/
├── src/
│   ├── __init__.py
│   ├── passenger.py                          # Passenger attributes
│   └── model.py                              # Shared simulation rules and basic metrics
├── utils/                                    # Reserved for reusable helper functions
├── data/
│   └── arrival_variation/                     # Runs, summaries, and descriptive contrasts (CSV)
├── notebooks/
│   ├── airport_security_model.ipynb          # Demonstration and validation
│   ├── processing_time_analysis.ipynb        # Service-duration variation
│   ├── checkpoint_analysis.ipynb             # Checkpoint-count comparison
│   ├── passenger_arrival_rate_analysis.ipynb # Passenger arrival rate analysis
│   ├── queue_capacity_analysis.ipynb         # Queue capacity analysis
│   └── arrival_variation_analysis.ipynb       # Combined demand and service-variation study
├── requirements.txt
└── README.md
```

Figures and summaries are embedded in the notebooks. The combined-study notebook additionally writes `data/arrival_variation/runs.csv` (270 rows), `summary.csv` (9 rows), and `contrasts.csv` (3 rows); rerunning its export cell replaces those files with the current results. No external dataset is required. Contributors should update the shared model in `src/` and import it into experiments rather than maintaining separate model copies.
