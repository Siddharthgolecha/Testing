"""Public Qiskit and Aer smoke tests; no cloud credentials required."""

import unittest

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


class TestQiskitSmoke(unittest.TestCase):
    @staticmethod
    def bell_circuit():
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit

    def test_statevector_bell_correlations(self):
        probabilities = Statevector.from_instruction(
            self.bell_circuit()
        ).probabilities_dict()
        self.assertAlmostEqual(probabilities.get("00", 0.0), 0.5, places=8)
        self.assertAlmostEqual(probabilities.get("11", 0.0), 0.5, places=8)
        self.assertAlmostEqual(sum(probabilities.values()), 1.0, places=8)

    def test_aer_compilation_and_measurement(self):
        circuit = self.bell_circuit()
        circuit.measure_all()
        simulator = AerSimulator(method="statevector")
        compiled = transpile(circuit, simulator, optimization_level=1)
        shots = 256
        counts = simulator.run(
            compiled, shots=shots, seed_simulator=12345
        ).result().get_counts()
        self.assertEqual(sum(counts.values()), shots)
        self.assertTrue(set(counts).issubset({"00", "11"}), counts)


if __name__ == "__main__":
    unittest.main()
