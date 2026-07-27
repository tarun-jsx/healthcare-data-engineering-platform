import pandas as pd
from typing import List, Dict, Any

from transform.transform_fact import format_date


def transform_patient(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform OpenFDA patient data into the dim_patient DataFrame.

    Args:
        results: List of safety report dictionaries returned by the OpenFDA API.

    Returns:
        A pandas DataFrame matching the dim_patient table schema.
    """

    rows = []

    for report in results:

        patient = report.get("patient", {})
        patient_death = patient.get("patientdeath", {})

        # Get patient onset age
        age = patient.get("patientonsetage")

        # Debug invalid or very large values
        if age is not None:
            try:
                age = int(age)

                if age > 2147483647 or age < -2147483648:
                    print(
                        f"Large age value: {age} | "
                        f"Report: {report.get('safetyreportid')}"
                    )

            except (ValueError, TypeError):
                print(
                    f"Invalid age value: {age} | "
                    f"Report: {report.get('safetyreportid')}"
                )
                age = None

        row = {
            "safety_report_id": report.get("safetyreportid"),
            "patient_sex": patient.get("patientsex"),
            "patient_onset_age": age,
            "patient_death_date": format_date(
                patient_death.get("patientdeathdate")
            )
        }

        rows.append(row)

    patient_df = pd.DataFrame(rows)

    return patient_df