
from fastapi import FastAPI, HTTPException, Query

from src.database.database_manager import (
    get_all_policies,
    get_policy_count,
)

app = FastAPI(
    title="Insurance AI Pipeline API",
    description="REST API for standardized insurance policy data.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Insurance AI Pipeline API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/policies/count")
def policy_count():
    return {"total_policies": get_policy_count()}


@app.get("/policies")
def list_policies(
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    policies = get_all_policies()

    # Convert missing values into JSON-compatible nulls.
    records = policies.to_dict(orient="records")

    return {
        "total": len(records),
        "limit": limit,
        "offset": offset,
        "policies": records[offset:offset + limit],
    }


@app.get("/policies/{policy_number}")
def get_policy(policy_number: str):
    policies = get_all_policies()

    matching = policies[
        policies["policy_number"] == policy_number
    ]

    if matching.empty:
        raise HTTPException(
            status_code=404,
            detail="Policy not found",
        )

    return matching.iloc[0].to_dict()
