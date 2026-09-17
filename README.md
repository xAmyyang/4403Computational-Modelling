# 4403Computational-Modelling
We are planning to model traffic congestion using a one-dimensional cellular automaton.

The road will consist of a fixed number of cells. Each cell can either be empty, represented by 0, or occupied by a car, represented by 1.

We have decided four parameters and four local rules.

## Parameters
1.Traffic density
2.Maximum speed
3.Random slowdown probability
4.Number of traffic lights

## Local Rules
1.Accelerate if possible
2.Brake if another car is too close
3.Randomly slow down
4.Stop at red traffic light, then move


## System
Traffic congestion on a single-lane circular road.
 
## Research Question
How does vehicle density affect traffic flow and the emergence of congestion?
 
## Modelling Approach
We will use a one-dimensional cellular automaton.
 
Each road cell is either:
- empty
- occupied by one vehicle
 
Vehicles move according to local rules based on the space in front of them.
 
 
## Measurements
- average vehicle speed
- traffic flow
- Percentage of stopped cars

## Planned Experiments
Run simulations across a range of vehicle densities and compare system behaviour. For each vehicle density, we will randomly distribute vehicles on the road and run the simulation for multiple time steps. We will repeat the simulation several times using different random initial conditions and calculate the average results.

## Expected Outcomes
We expect average vehicle speed to decrease as vehicle density increases. Traffic flow may initially increase as more vehicles are added, but may decrease once congestion becomes severe. We aim to identify whether there is a transition point where congestion begins to emerge.
 
