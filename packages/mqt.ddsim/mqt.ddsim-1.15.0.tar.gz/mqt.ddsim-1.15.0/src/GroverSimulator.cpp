#include "GroverSimulator.hpp"

#include "QuantumComputation.hpp"
#include "dd/FunctionalityConstruction.hpp"

#include <chrono>

template<class Config>
std::map<std::string, std::size_t> GroverSimulator<Config>::Simulate(std::size_t shots) {
    // Setup X on the last, Hadamard on all qubits
    qc::QuantumComputation qc_setup(n_qubits + n_anciallae);
    qc_setup.x(n_qubits);
    for (qc::Qubit i = 0; i < n_qubits; ++i) {
        qc_setup.h(i);
    }

    dd::Edge setup_op{dd::buildFunctionality(&qc_setup, Simulator<Config>::dd)};

    // Build the oracle
    qc::QuantumComputation qc_oracle(n_qubits + n_anciallae);
    qc::Controls           controls{};
    for (qc::Qubit i = 0; i < n_qubits; i++) {
        controls.emplace(qc::Control{i, oracle.at(i) == '1' ? qc::Control::Type::Pos : qc::Control::Type::Neg});
    }
    qc_oracle.z(n_qubits, controls);

    dd::Edge oracle_op{dd::buildFunctionality(&qc_oracle, Simulator<Config>::dd)};

    // Build the diffusion stage.
    qc::QuantumComputation qc_diffusion(n_qubits + n_anciallae);

    for (qc::Qubit i = 0; i < n_qubits; ++i) {
        qc_diffusion.h(i);
    }
    for (qc::Qubit i = 0; i < n_qubits; ++i) {
        qc_diffusion.x(i);
    }

    qc_diffusion.h(n_qubits - 1);

    qc::Controls diff_controls{};
    for (qc::Qubit j = 0; j < n_qubits - 1; ++j) {
        diff_controls.emplace(qc::Control{j});
    }
    qc_diffusion.x(n_qubits - 1, diff_controls);

    qc_diffusion.h(n_qubits - 1);

    for (qc::Qubit i = 0; i < n_qubits; ++i) {
        qc_diffusion.x(i);
    }
    for (qc::Qubit i = 0; i < n_qubits; ++i) {
        qc_diffusion.h(i);
    }

    dd::Edge diffusion_op{dd::buildFunctionality(&qc_diffusion, Simulator<Config>::dd)};

    dd::Edge full_iteration{Simulator<Config>::dd->multiply(oracle_op, diffusion_op)};
    Simulator<Config>::dd->incRef(full_iteration);

    assert(n_qubits + n_anciallae <= std::numeric_limits<dd::QubitCount>::max());
    Simulator<Config>::rootEdge = Simulator<Config>::dd->makeZeroState(static_cast<dd::QubitCount>(n_qubits + n_anciallae));
    Simulator<Config>::rootEdge = Simulator<Config>::dd->multiply(setup_op, Simulator<Config>::rootEdge);
    Simulator<Config>::dd->incRef(Simulator<Config>::rootEdge);

    std::size_t j_pre = 0;

    while ((iterations - j_pre) % 8 != 0) {
        //std::clog << "[INFO]  Pre-Iteration " << j_pre+1 << " of " << iterations%8 << " -- size:" << dd->size(rootEdge)  << "\n";
        auto tmp = Simulator<Config>::dd->multiply(full_iteration, Simulator<Config>::rootEdge);
        Simulator<Config>::dd->incRef(tmp);
        Simulator<Config>::dd->decRef(Simulator<Config>::rootEdge);
        Simulator<Config>::rootEdge = tmp;
        Simulator<Config>::dd->garbageCollect();
        j_pre++;
    }

    for (std::size_t j = j_pre; j < iterations; j += 8) {
        //std::clog << "[INFO]  Iteration " << j+1 << " of " << iterations << " -- size:" << dd->size(rootEdge)  << "\n";
        auto tmp = Simulator<Config>::dd->multiply(full_iteration, Simulator<Config>::rootEdge);
        for (std::size_t i = 0; i < 7; ++i) {
            tmp = Simulator<Config>::dd->multiply(full_iteration, tmp);
        }
        Simulator<Config>::dd->incRef(tmp);
        Simulator<Config>::dd->decRef(Simulator<Config>::rootEdge);
        Simulator<Config>::rootEdge = tmp;
        Simulator<Config>::dd->garbageCollect();
    }

    return Simulator<Config>::MeasureAllNonCollapsing(shots);
}

template class GroverSimulator<dd::DDPackageConfig>;
