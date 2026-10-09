"""Public SCHI Qiskit exporter probe. No private repo code or secrets.

Tests mixed-polarity little-endian MCX control states, reversible computation
and uncomputation, and Aer-based 5-bit Grover amplification. A *small-scale*
interface test, NOT a full 94-qubit KRK experiment.
"""
import math
import unittest
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import MCXGate
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


def mcx(qc, ctl, pattern, target):
    state = sum(int(v) << i for i, v in enumerate(pattern))
    qc.append(MCXGate(len(ctl), ctrl_state=state), list(ctl) + [target])


def bad(code):
    a = [(code >> i) & 1 for i in range(5)]
    return int(bool(a[4] and a[3] and not a[1] and (a[0] ^ a[2])))


def compute_bad(qc):
    # Five action bits, parity-work bit 5, XOR target bit 6.
    qc.cx(0, 5)
    qc.cx(2, 5)
    mcx(qc, (1, 3, 4, 5), (0, 1, 1, 1), 6)
    qc.cx(2, 5)
    qc.cx(0, 5)


def phase_oracle(qc):
    compute_bad(qc)
    qc.z(6)
    compute_bad(qc)


def diffuser(qc):
    qc.h(range(5))
    qc.x(range(5))
    qc.h(4)
    mcx(qc, (0, 1, 2, 3), (1, 1, 1, 1), 4)
    qc.h(4)
    qc.x(range(5))
    qc.h(range(5))


def grover(iterations, measure=False):
    qc = QuantumCircuit(7, 5 if measure else 0)
    qc.h(range(5))
    for _ in range(iterations):
        phase_oracle(qc)
        diffuser(qc)
    if measure:
        qc.measure(range(5), range(5))
    return qc


class SCHIExporterTest(unittest.TestCase):
    def test_mixed_control_states(self):
        for code in range(16):
            for output in (0, 1):
                qc = QuantumCircuit(5)
                for i in range(4):
                    if (code >> i) & 1:
                        qc.x(i)
                if output:
                    qc.x(4)
                mcx(qc, (0, 1, 2, 3), (0, 1, 0, 1), 4)
                toggle = code == 10
                basis = code | ((output ^ toggle) << 4)
                result = Statevector.from_instruction(qc).probabilities_dict()
                self.assertAlmostEqual(result.get(format(basis, "05b"), 0), 1)

    def test_computed_xor_and_clean_work(self):
        for code in range(32):
            for old_flag in (0, 1):
                qc = QuantumCircuit(7)
                for i in range(5):
                    if (code >> i) & 1:
                        qc.x(i)
                if old_flag:
                    qc.x(6)
                compute_bad(qc)
                expected = code | ((old_flag ^ bad(code)) << 6)
                result = Statevector.from_instruction(qc).probabilities_dict()
                self.assertAlmostEqual(result.get(format(expected, "07b"), 0), 1)

    def test_phase_oracle_basis_states(self):
        for code in range(32):
            qc = QuantumCircuit(7)
            for i in range(5):
                if (code >> i) & 1:
                    qc.x(i)
            phase_oracle(qc)
            amplitudes = Statevector.from_instruction(qc).data
            self.assertAlmostEqual(float(amplitudes[code].real), (-1) ** bad(code))
            self.assertAlmostEqual(float(amplitudes[code].imag), 0)
            self.assertAlmostEqual(abs(amplitudes[code]), 1)

    def test_grover_ideal_and_aer_shots(self):
        winning = {j for j in range(32) if bad(j)}
        self.assertEqual(len(winning), 2)
        theta = math.asin(math.sqrt(len(winning) / 32))
        for k in (0, 1, 2):
            sv = Statevector.from_instruction(grover(k))
            probability = sum(abs(sv.data[j]) ** 2 for j in winning)
            self.assertAlmostEqual(probability, math.sin((2*k+1)*theta)**2, places=8)
            # All paths clean flags and parity scratch.
            self.assertLess(sum(abs(sv.data[j])**2 for j in range(32,128)), 1e-10)
        simulator = AerSimulator(method="matrix_product_state")
        compiled = transpile(grover(2, measure=True), simulator, optimization_level=0)
        self.assertFalse(any(op.name == "mcx" for op in compiled.data))
        result = simulator.run(
            compiled, shots=4096, seed_simulator=101
        ).result()
        counts = result.get_counts()
        actual = sum(n for state, n in counts.items() if int(state, 2) in winning)/4096
        theoretical = math.sin(5*theta)**2
        self.assertLess(abs(actual-theoretical), 0.04)
        print(f"SCHI_PUBLIC_PROBE: winners={sorted(winning)}, "
              f"Aer_success={actual:.6f}, ideal={theoretical:.6f}")


if __name__ == "__main__":
    unittest.main()
