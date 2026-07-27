import pandas as pd
from typing import List, Dict, Any

from utils.surrogate_key_lookup import lookup_surrogate_key


def transform_report_drug(results: List[Dict[str, Any]], conn) -> pd.DataFrame:

    rows = []

    for report in results:

        safety_report_id = report.get("safetyreportid")

        report_key = lookup_surrogate_key(
            conn=conn,
            table_name="fact_safety_report",
            key_column="report_key",
            lookup_columns=["safety_report_id"],
            lookup_values=[safety_report_id]
        )

        patient = report.get("patient", {})
        drugs = patient.get("drug", [])

        for drug in drugs:

            medicinal_product = drug.get("medicinalproduct")

            drug_key = lookup_surrogate_key(
                conn=conn,
                table_name="dim_drug",
                key_column="drug_key",
                lookup_columns=["medicinal_product"],
                lookup_values=[medicinal_product]
            )

            rows.append({
                "report_key": int(report_key),
                "drug_key": int(drug_key)
             })

    return pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)