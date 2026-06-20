import matplotlib.pyplot as plt

labels = ["Simulator (Ideal)", "IBM Quantum Real Hardware"]
success_prob = [1.0, 0.93]

plt.bar(labels, success_prob)
plt.ylim(0, 1)
plt.ylabel("Success Probability")
plt.title("Bernstein–Vazirani Algorithm: Simulator vs Real Hardware")

for i, v in enumerate(success_prob):
    plt.text(i, v + 0.02, f"{v:.2f}", ha="center")

plt.show()
