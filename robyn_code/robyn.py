# robyn_code/robyn.py
class Robyn:
    def __init__(self, csv_input, alpha=0.5):
        self.csv_input = csv_input
        self.alpha = alpha

    def run(self):
        return f"Running Robyn model with {self.csv_input} and alpha={self.alpha}"

    def get_plot_data(self):
        return "Dummy ROAS Plot"

    def get_media_mix_plot(self):
        return "Dummy Media Mix Plot"

