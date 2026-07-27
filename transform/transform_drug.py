import pandas as pd
from typing import List, Dict, Any


def transform_drug(results: List[Dict[str, Any]]) -> pd.DataFrame:

    rows = []

    for report in results:

        patient = report.get("patient", {})
        drugs = patient.get("drug", [])

        for drug in drugs:

            openfda = drug.get("openfda", {})

            row = {
                "medicinal_product": drug.get("medicinalproduct"),

                "brand_name": ", ".join(openfda.get("brand_name", [])),
                "generic_name": ", ".join(openfda.get("generic_name", [])),
                "manufacturer_name": ", ".join(openfda.get("manufacturer_name", [])),

                "drug_characterization": drug.get("drugcharacterization"),
                "authorization_number": drug.get("drugauthorizationnumb"),
                "dosage_text": drug.get("drugdosagetext")
            }

            rows.append(row)

    drug_df = pd.DataFrame(rows)

    drug_df = drug_df.drop_duplicates().reset_index(drop=True)

    return drug_df