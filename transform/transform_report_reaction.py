import pandas as pd
from typing import List, Dict, Any

from utils.surrogate_key_lookup import lookup_surrogate_key


def transform_report_reaction(results: List[Dict[str, Any]], conn) -> pd.DataFrame:

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
        reactions = patient.get("reaction", [])

        for reaction in reactions:

            reaction_term = reaction.get("reactionmeddrapt")

            reaction_key = lookup_surrogate_key(
                conn=conn,
                table_name="dim_reaction",
                key_column="reaction_key",
                lookup_columns=["reaction_name"],
                lookup_values=[reaction_term]
            )

            rows.append({
                "report_key": int(report_key),
                "reaction_key": int(reaction_key)
            })

    return pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)