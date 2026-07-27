import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import logging

from utils.surrogate_key_lookup import lookup_surrogate_key

logger = logging.getLogger(__name__)


def format_date(date_str):
    """
    Convert OpenFDA date format (YYYYMMDD)
    to PostgreSQL date format (YYYY-MM-DD).
    """

    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        return None


def format_boolean(value):
    """
    Convert OpenFDA Yes/No codes to Python booleans.

    1 -> True
    2 -> False
    None -> None
    Anything else -> None (with warning)
    """

    if value is None:
        return None

    if value == "1":
        return True

    if value == "2":
        return False

    logger.warning(f"Unexpected boolean value: {value}")
    return None


def transform_fact_safety_report(
    results: List[Dict[str, Any]],
    conn
) -> pd.DataFrame:
    """
    Transform OpenFDA safety reports into the Fact_Safety_Report DataFrame.
    """

    rows = []

    for report in results:

        safety_report_id = report.get("safetyreportid")

        # -----------------------------
        # Surrogate Key Lookups
        # -----------------------------

        patient_key = lookup_surrogate_key(
            conn=conn,
            table_name="dim_patient",
            key_column="patient_key",
            lookup_columns=["safety_report_id"],
            lookup_values=[safety_report_id]
        )

        sender_key = lookup_surrogate_key(
            conn=conn,
            table_name="dim_sender",
            key_column="sender_key",
            lookup_columns=["safety_report_id"],
            lookup_values=[safety_report_id]
        )

        primary_source_key = lookup_surrogate_key(
            conn=conn,
            table_name="dim_primary_source",
            key_column="primary_source_key",
            lookup_columns=["safety_report_id"],
            lookup_values=[safety_report_id]
        )

        # -----------------------------
        # Fact Row
        # -----------------------------

        row = {

            "safety_report_id": safety_report_id,

            "patient_key": patient_key,
            "sender_key": sender_key,
            "primary_source_key": primary_source_key,

            "transmission_date": format_date(report.get("transmissiondate")),
            "received_date": format_date(report.get("receivedate")),
            "receipt_date": format_date(report.get("receiptdate")),

            "serious": format_boolean(report.get("serious")),
            "seriousness_death": format_boolean(report.get("seriousnessdeath")),
            "fulfil_expedite_criteria": format_boolean(
                report.get("fulfillexpeditecriteria")
            ),

            "company_number": report.get("companynumb")
        }

        rows.append(row)

    return pd.DataFrame(rows)