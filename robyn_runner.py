from facebook.robyn import Robyn
import pandas as pd

def run_robyn_model(data, alpha=0.5):
    """
    Kör Robyn-modellen med angiven data.

    Args:
        data (pd.DataFrame): Förberedd data.
        alpha (float): Regularisering för modellen.

    Returns:
        dict: Resultat inkluderar ROAS- och mediemix-plots.
    """
    # Spara data till en temporär CSV-fil
    temp_path = "uploads/temp.csv"
    data.to_csv(temp_path, index=False)

    # Initiera Robyn och kör modellen
    robyn_instance = Robyn(csv_input=temp_path, alpha=alpha)
    robyn_instance.run()

    # Hämta plots från Robyn
    return {
        "roas_plot": robyn_instance.get_plot_data(),
        "media_mix_plot": robyn_instance.get_media_mix_plot()
    }

def optimize_media_mix(goal, budget, priority_channels):
    """
    Optimerar mediemixen baserat på mål och budget.

    Args:
        goal (str): Optimeringsmål ("Maximera ROAS", "Maximera konverteringar").
        budget (int): Total budget.
        priority_channels (list): Lista över prioriterade kanaler.

    Returns:
        dict: Rekommenderad mediemix.
    """
    # Standardinställningar för kanaler
    channels = ["Facebook", "Google Ads", "Instagram", "TikTok"]
    initial_mix = {channel: budget / len(channels) for channel in channels}

    # Prioritera vissa kanaler
    if priority_channels:
        for channel in priority_channels:
            initial_mix[channel] *= 1.2  # Öka budgeten för prioriterade kanaler

        # Normalisera så att summan matchar budgeten
        total = sum(initial_mix.values())
        initial_mix = {k: v / total * budget for k, v in initial_mix.items()}

    # Kör Robyn med optimerad mix
    robyn_instance = Robyn(custom_media_mix=initial_mix, alpha=0.5)
    robyn_instance.run()

    # Returnera metrik från Robyn
    return robyn_instance.get_metrics()

