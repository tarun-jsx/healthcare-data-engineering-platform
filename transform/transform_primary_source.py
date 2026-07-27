import pandas as pd
from typing import List,Dict, Any

def transform_primary_source(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform OpenFDA primary source data into the dim_primary_source DataFrame.
    """
    rows = []

    for report in results:

        primary_source = report.get('primarysource',{})

        row = {
            "safety_report_id": report.get("safetyreportid"),
            "reporter_country": primary_source.get("reportercountry"),
            "qualification": primary_source.get("qualification")
        }

        rows.append(row)

    primary_source_df = pd.DataFrame(rows)
    return primary_source_df
    
