"""
Copyright 2021 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import pandas as pd
import io

def load_model(input_dir):
    return "dummy"


def score_unstructured(model, data, query, **kwargs):
    print("Incoming content type params: ", kwargs)
    print("Incoming data type: ", type(data))
    print("Incoming data: ", data)

    print("Incoming query params: ", query)
    if isinstance(data, bytes):
        data = data.decode("utf8")

    df = pd.read_csv(io.StringIO(data))
    print(df)

    ret = solve(df["c1"], df["c2"], df["c3"], df["c4"])

    list = []
    for x in ret["opt_values"].values():
        print(f"{x.name}: {x.value()}")
        list.append({x.name: x.value()})

    return str(list)

def solve(c1, c2, c3, c4):
    # Define the model
    model = LpProblem(name="production-planning-optimization", sense=LpMaximize)

    # Define the decision variables
    x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 5)}

    # Add constraints
    model += (lpSum(x.values()) <= c1, "energy_consumption")
    model += (2 * x[1] + x[2] + 2 * x[3] <= c2, "raw_material_a")
    model += (x[2] + 2 * x[3] + 2 * x[4] <= c3, "raw_material_b")
    model += (4 * x[1] + x[2] + 2 * x[3] + 3 * x[4] <= c4, "raw_material_c")

    # Set the objective
    model += 30 * x[1] + 20 * x[2] + 50 * x[3] + 35 * x[4]

    # Solve the optimization problem
    status = model.solve()

    # Get the results
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    return {"opt_values": x, "status": LpStatus[model.status]}
