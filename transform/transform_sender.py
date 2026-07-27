import pandas as pd
from typing import List, Dict, Any


def transform_sender(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform OpenFDA sender data into the dim_sender DataFrame.
    """

    rows = []

    for report in results:

        sender = report.get("sender", {})

        row = {
            "safety_report_id": report.get("safetyreportid"),
            "sender_organization": sender.get("senderorganization")
        }

        rows.append(row)

    sender_df = pd.DataFrame(rows)

    return sender_df

