import pandas as pd

def prepare_data(data):
    """
    Förbereder data för Robyn-modellen:
    - Fyller saknade värden.
    - Korrigerar negativa värden.

    Args:
        data (pd.DataFrame): Uppladdad data.

    Returns:
        pd.DataFrame: Förberedd data.
    """
    # Hantera saknade värden
    for col in data.columns:
        if data[col].dtype in ["float64", "int64"]:
            data[col].fillna(0, inplace=True)  # Fyll saknade numeriska värden med 0
        else:
            data[col].fillna("Unknown", inplace=True)  # Fyll saknade textvärden med "Unknown"

    # Korrigera negativa värden
    spend_columns = [col for col in data.columns if "Spend" in col or "Sales" in col or "Conversions" in col]
    for col in spend_columns:
        data[col] = data[col].clip(lower=0)  # Klipp negativa värden till 0

    return data

