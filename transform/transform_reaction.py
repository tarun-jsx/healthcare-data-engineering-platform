import pandas as pd
from typing import List, Dict, Any


def transform_reaction(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform OpenFDA reaction data into the dim_reaction DataFrame.
    """

    rows = []

    for report in results:

        patient = report.get("patient", {})

        reactions = patient.get("reaction", [])

        for reaction in reactions:

            row = {
                "reaction_name": reaction.get("reactionmeddrapt"),
                "reaction_outcome": reaction.get("reactionoutcome"),
                "reaction_version": reaction.get("reactionmeddraversionpt")
            }

            rows.append(row)

    reaction_df = pd.DataFrame(rows)

    reaction_df = reaction_df.drop_duplicates().reset_index(drop=True)

    return reaction_df