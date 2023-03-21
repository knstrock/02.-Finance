import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def calculate_dcf():
    cash_flows = [float(cf_entry.text()) for cf_entry in cash_flow_entries]
    discount_rate = float(discount_rate_entry.text()) / 100
    periods = len(cash_flows)

    dcf_value = sum(cf / (1 + discount_rate)**(i + 1) for i, cf in enumerate(cash_flows))

    result_label.setText(f"DCF Value: {dcf_value:.2f}")

    # Update the graph
    discounted_cash_flows = [cf / (1 + discount_rate)**(i + 1) for i, cf in enumerate(cash_flows)]
    ax.clear()
    bars = ax.bar(range(1, periods + 1), discounted_cash_flows)
    ax.set_xlabel("Period")
    ax.set_ylabel("Discounted Cash Flow")
    ax.set_title("Discounted Cash Flow Graph")

    # Add values inside the bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center", va="bottom")

    canvas.draw()

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

form_layout = QFormLayout()

cash_flow_entries = []
for i in range(1, 6):
    cf_label = QLabel(f"Cash Flow {i}")
    cf_entry = QLineEdit()
    cash_flow_entries.append(cf_entry)
    form_layout.addRow(cf_label, cf_entry)

discount_rate_label = QLabel("Discount Rate (%)")
discount_rate_entry = QLineEdit()
form_layout.addRow(discount_rate_label, discount_rate_entry)

layout.addLayout(form_layout)

calculate_button = QPushButton("Calculate DCF")
calculate_button.clicked.connect(calculate_dcf)
layout.addWidget(calculate_button)

result_label = QLabel("")
layout.addWidget(result_label)

# Create the graph
figure = Figure()
canvas = FigureCanvas(figure)
ax = figure.add_subplot(111)
layout.addWidget(canvas)

window.show()

sys.exit(app.exec_())