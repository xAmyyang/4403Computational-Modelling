# 4403Computational-Modelling
We are planning to model traffic congestion using a one-dimensional cellular automaton.

The road will consist of a fixed number of cells. Each cell can either be empty, represented by 0, or occupied by a car, represented by 1.

We will define a local rule for vehicle movement. For example, if the cell in front of a car is empty, the car can move forward; otherwise, it has to stop.

Our main research question is: **How does vehicle density affect traffic flow and congestion?**

We will start with cars randomly distributed on the road at different densities, for example 10%, 30%, 50%, 70%, and 90%.

For each density, we will run the simulation over multiple time steps and measure things such as the average speed of vehicles and traffic flow. We want to see whether there is a critical density where congestion starts to emerge.

If the basic model works well, we may extend it by adding random braking behaviour.

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
 
## Main Parameter
Vehicle density
 
## Measurements
- average vehicle speed
- traffic flow
 
## Planned Experiments
Run simulations across a range of vehicle densities and compare system behaviour. For each vehicle density, we will randomly distribute vehicles on the road and run the simulation for multiple time steps. We will repeat the simulation several times using different random initial conditions and calculate the average results.

## Expected Outcomes
We expect average vehicle speed to decrease as vehicle density increases. Traffic flow may initially increase as more vehicles are added, but may decrease once congestion becomes severe. We aim to identify whether there is a transition point where congestion begins to emerge.
 
## Possible Extension
Introduce random braking and investigate whether it changes the onset of congestion.
In the extended model, a vehicle may randomly stop even when the cell in front is empty. We may compare different braking probabilities, such as 0, 0.1, 0.2, and 0.3.
