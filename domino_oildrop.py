import random
import matplotlib.pyplot as plt

# Mean mass (arbitrary units, e.g., corresponding to a single electron charge)
mass_mean = 6.5
# Minimum step size (simulating quantization, e.g., one electron's charge)
mass_step = 1.2

# Generate random "drop" masses, simulating oil drops picking up integer numbers of electrons
num_drops = 40
box_masses = []
for _ in range(num_drops):
    # Each drop gets a mass that's an integer multiple of the step size above the minimum
    n_steps = random.randint(1, int(4 * mass_mean))
    mass = mass_step + n_steps * mass_step
    box_masses.append(mass)

# Sort the masses to analyze quantization
box_sorted = sorted(box_masses)

# Calculate absolute increase relative to the smallest drop
smallest = box_sorted[0]
absolute_increase = [mass - smallest for mass in box_sorted]

# Calculate non-zero step sizes between consecutive drops (should cluster around mass_step)
step_sizes = [
    box_sorted[i + 1] - box_sorted[i]
    for i in range(len(box_sorted) - 1)
    if box_sorted[i + 1] - box_sorted[i] != 0
]

print("Sorted box masses:", box_sorted)
print("Non-zero step sizes (should be multiples of mass_step):", step_sizes)

# Plot both absolute and relative increases
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.bar(range(len(absolute_increase)), absolute_increase)
plt.xlabel("Drop # (sorted by mass)")
plt.ylabel("Absolute Increase to Lightest Box")
plt.title("Absolute Mass Increase (Oil Drop Analogy)")

plt.subplot(1, 2, 2)
plt.bar(range(len(step_sizes)), step_sizes)
plt.xlabel("Step #")
plt.ylabel("Step Size")
plt.title("Relative Mass Step Sizes (Quantization)")
# Annotate each bar with its step size value
for i, v in enumerate(step_sizes):
    plt.text(i, v + 0.05, f"{v:.2f}", ha="center", va="bottom", fontsize=8)

plt.tight_layout()
plt.show()
