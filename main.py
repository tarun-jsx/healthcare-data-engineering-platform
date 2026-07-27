from extract.openfda_api import fetch_openfda_data

from transform.transform_patient import transform_patient
from transform.transform_drug import transform_drug
from transform.transform_reaction import transform_reaction
from transform.transform_sender import transform_sender
from transform.transform_primary_source import transform_primary_source
from transform.transform_fact import transform_fact_safety_report
from transform.transform_report_drug import transform_report_drug
from transform.transform_report_reaction import transform_report_reaction
from load.postgres_loader import load_dataframe
from database.db_connection import get_connection


def main():

    # -------------------------
    # Database Connection
    # -------------------------
    conn = get_connection()

    # -------------------------
    # Extract
    # -------------------------
    results = fetch_openfda_data()

    # -------------------------
    # Transform Dimensions
    # -------------------------
    patient_df = transform_patient(results)
    drug_df = transform_drug(results)
    reaction_df = transform_reaction(results)
    sender_df = transform_sender(results)
    primary_source_df = transform_primary_source(results)
    

    # -------------------------
    # Load Dimensions
    # -------------------------
    load_dataframe(patient_df, "dim_patient", conn)
    load_dataframe(drug_df, "dim_drug", conn)
    load_dataframe(reaction_df, "dim_reaction", conn)
    load_dataframe(sender_df, "dim_sender", conn)
    load_dataframe(primary_source_df, "dim_primary_source", conn)
    

    # -------------------------
    # Transform Fact
    # -------------------------
    fact_df = transform_fact_safety_report(results, conn)

    # -------------------------
    # Load Fact
    # -------------------------
    load_dataframe(fact_df, "fact_safety_report", conn)
    # -------------------------
    # Transform Bridge Tables
    # -------------------------
    report_drug_df = transform_report_drug(results, conn)
    report_reaction_df = transform_report_reaction(results, conn)

    # -------------------------
    # Load Bridge Tables
    # -------------------------
    load_dataframe(report_drug_df, "report_drug", conn)
    load_dataframe(report_reaction_df, "report_reaction", conn)
    # -------------------------
    # Close Connection
    # -------------------------
    conn.close()


if __name__ == "__main__":
    main()