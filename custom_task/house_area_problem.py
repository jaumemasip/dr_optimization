"""
Copyright 2021 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

def define_and_solve_linear_problem(c1, c2, c3):
    # Define the model
    model = LpProblem(name="house-area-optimization", sense=LpMaximize)

    # Define the decision variables
    x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 4)}

    # Add constraints
    model += (lpSum(x.values()) <= 13000, "total_area") # because of taxes
    model += (x[1] >= c1, "lot_area")
    model += (x[2] >= c2, "gr_liv_area")
    model += (x[3] >= c3, "garage_area")

    # Set the objective
    model += x[1] + x[2] + x[3] # increase profit for rental

    # Solve the optimization problem
    status = model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    for var in x.values():
        print(f"{var.name}: {var.value()}")

    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")

    return {"opt_values": x, "status": LpStatus[model.status]}
