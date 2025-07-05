import random
import matplotlib.pyplot as plt
import numpy as np

# === MILLIKAN OIL DROP SIMULATION ===
# This simulates the famous experiment that proved charge quantization
# Each "box" represents an oil drop that has picked up electrons

# Physical parameters (in arbitrary units)
ELECTRON_CHARGE = 1.2  # Fundamental unit we're trying to "discover"
BASE_MASS = 6.5  # Minimum mass of oil drop
NUM_DROPS = 50  # More drops for better statistics

print("=== MILLIKAN OIL DROP SIMULATION ===")
print(f"True electron charge (unknown to 'experimenter'): {ELECTRON_CHARGE}")
print(f"Analyzing {NUM_DROPS} oil drops...\n")

# Generate oil drop masses (each picks up random number of electrons)
drop_masses = []
electrons_picked = []  # Track actual number for verification

for i in range(NUM_DROPS):
    # Each drop picks up 1-20 electrons (realistic range)
    n_electrons = random.randint(1, 20)
    mass = BASE_MASS + n_electrons * ELECTRON_CHARGE

    drop_masses.append(mass)
    electrons_picked.append(n_electrons)

# Sort for analysis (what Millikan would do)
sorted_masses = sorted(drop_masses)
min_mass = min(sorted_masses)

# Calculate mass differences from lightest drop
mass_differences = [mass - min_mass for mass in sorted_masses]

# Find step sizes between consecutive drops
step_sizes = []
for i in range(len(sorted_masses) - 1):
    step = sorted_masses[i + 1] - sorted_masses[i]
    if step > 0.1:  # Ignore tiny differences
        step_sizes.append(step)

# === THE "DISCOVERY" PROCESS ===
print("EXPERIMENTAL DATA:")
print(f"Lightest drop mass: {min_mass:.2f}")
print(f"Step sizes between drops: {[f'{s:.2f}' for s in step_sizes[:10]]}...")


# Find the greatest common divisor (Millikan's key insight!)
def find_charge_unit(differences):
    """Find the fundamental unit by looking for common factors"""
    # Remove zero differences and round to avoid floating point issues
    non_zero_diffs = [round(d, 1) for d in differences if d > 0.1]

    # Try different possible charge values
    best_unit = 0
    min_error = float("inf")

    for test_unit in np.arange(0.5, 3.0, 0.1):
        error = 0
        for diff in non_zero_diffs:
            # How close is this difference to an integer multiple?
            ratio = diff / test_unit
            closest_int = round(ratio)
            error += abs(ratio - closest_int)

        if error < min_error:
            min_error = error
            best_unit = test_unit

    return round(best_unit, 1)


discovered_charge = find_charge_unit(mass_differences)
accuracy = abs(discovered_charge - ELECTRON_CHARGE) / ELECTRON_CHARGE * 100

print(f"\nDISCOVERED fundamental unit: {discovered_charge}")
print(f"Actual fundamental unit: {ELECTRON_CHARGE}")
print(f"Accuracy: {100 - accuracy:.1f}%")

# === VISUALIZATION ===
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# 1. Raw drop masses
ax1.scatter(range(len(drop_masses)), drop_masses, alpha=0.7, color="blue")
ax1.set_xlabel("Drop Number")
ax1.set_ylabel("Total Mass")
ax1.set_title("Raw Oil Drop Masses")
ax1.grid(True, alpha=0.3)

# 2. Mass differences with theoretical lines
ax2.bar(range(len(mass_differences)), mass_differences, alpha=0.7, color="green")
# Add theoretical quantization lines
for i in range(1, 21):
    ax2.axhline(
        y=i * ELECTRON_CHARGE, color="red", linestyle="--", alpha=0.5, linewidth=1
    )
ax2.set_xlabel("Drop Number (sorted by mass)")
ax2.set_ylabel("Mass Above Minimum")
ax2.set_title("Mass Differences (Green=Data, Red=Theory)")
ax2.grid(True, alpha=0.3)

# 3. Step size histogram
ax3.hist(step_sizes, bins=20, alpha=0.7, color="orange", edgecolor="black")
ax3.axvline(
    x=ELECTRON_CHARGE,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"True value ({ELECTRON_CHARGE})",
)
ax3.axvline(
    x=discovered_charge,
    color="blue",
    linestyle="-",
    linewidth=2,
    label=f"Discovered ({discovered_charge})",
)
ax3.set_xlabel("Step Size")
ax3.set_ylabel("Frequency")
ax3.set_title("Distribution of Step Sizes")
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Verification plot - show electron count vs mass
actual_electrons = sorted(electrons_picked)
theoretical_masses = [BASE_MASS + n * ELECTRON_CHARGE for n in actual_electrons]
ax4.scatter(actual_electrons, sorted_masses, alpha=0.7, color="blue", label="Measured")
ax4.plot(actual_electrons, theoretical_masses, "r--", label="Theory")
ax4.set_xlabel("Number of Electrons")
ax4.set_ylabel("Total Mass")
ax4.set_title("Mass vs Electron Count (Verification)")
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle(
    "Millikan Oil Drop Experiment Simulation", y=1.02, fontsize=14, fontweight="bold"
)
plt.show()

# === STUDENT QUESTIONS ===
print("\n=== DISCUSSION QUESTIONS ===")
print("1. Why do the step sizes cluster around certain values?")
print("2. What would happen if charge wasn't quantized?")
print("3. How does increasing the number of drops improve accuracy?")
print("4. What sources of experimental error might Millikan have faced?")
