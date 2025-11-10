const DetailedSimulation = ({ detailedData }) => {
  if (!detailedData) {
    return null
  }

  const { qubits, summary, sifted_key, qber, error_rate, eve_fraction } = detailedData

  return (
    <div className="card p-6 space-y-6">
      <div className="flex items-center gap-3">
        <span className="text-3xl">🔬</span>
        <h2 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
          Step-by-Step Simulation Details
        </h2>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="stat-card text-center">
          <h3 className="text-xs text-gray-400 mb-1">Total Qubits</h3>
          <p className="text-lg font-semibold text-blue-400">{summary.total_qubits}</p>
        </div>
        <div className="stat-card text-center">
          <h3 className="text-xs text-gray-400 mb-1">Bases Matched</h3>
          <p className="text-lg font-semibold text-green-400">{summary.matching_bases}</p>
        </div>
        {eve_fraction > 0 && (
          <div className="stat-card text-center">
            <h3 className="text-xs text-gray-400 mb-1">Eve Intercepts</h3>
            <p className="text-lg font-semibold text-red-400">{summary.eve_interceptions}</p>
          </div>
        )}
        <div className="stat-card text-center">
          <h3 className="text-xs text-gray-400 mb-1">Final QBER</h3>
          <p className="text-lg font-semibold text-purple-400">{(qber * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Educational Info */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 space-y-2">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <span>📚</span> How BB84 Works:
        </h3>
        <ul className="text-sm text-gray-300 space-y-1 ml-6 list-disc">
          <li><strong>Alice</strong> sends qubits encoded with random bits in random bases (Z or X)</li>
          <li><strong>Bob</strong> measures each qubit with a randomly chosen basis</li>
          <li>When <strong>bases match</strong>: Bob measures the correct bit (unless there's noise/Eve)</li>
          <li>When <strong>bases don't match</strong>: Bob gets a random bit (50/50 chance)</li>
          {eve_fraction > 0 && (
            <li><strong>Eve</strong> intercepts some qubits, measures them, and resends - this introduces ~25% error on intercepted qubits</li>
          )}
          <li>After transmission, Alice and Bob compare bases and keep only matching ones (sifting)</li>
        </ul>
      </div>

      {/* Qubit Details Table */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <span>⚛️</span> Qubit-by-Qubit Analysis:
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/20">
                <th className="px-3 py-2 text-left text-gray-400">#</th>
                <th className="px-3 py-2 text-center text-gray-400">Alice Bit</th>
                <th className="px-3 py-2 text-center text-gray-400">Alice Basis</th>
                <th className="px-3 py-2 text-center text-gray-400">State</th>
                {eve_fraction > 0 && (
                  <>
                    <th className="px-3 py-2 text-center text-gray-400">Eve?</th>
                    <th className="px-3 py-2 text-center text-gray-400">Eve Basis</th>
                  </>
                )}
                <th className="px-3 py-2 text-center text-gray-400">Bob Basis</th>
                <th className="px-3 py-2 text-center text-gray-400">Bob Got</th>
                <th className="px-3 py-2 text-center text-gray-400">Match?</th>
                <th className="px-3 py-2 text-center text-gray-400">Correct?</th>
                <th className="px-3 py-2 text-center text-gray-400">In Key?</th>
              </tr>
            </thead>
            <tbody>
              {qubits.map((qubit) => (
                <tr
                  key={qubit.index}
                  className={`border-b border-white/10 ${
                    qubit.bases_match
                      ? 'bg-green-500/5 hover:bg-green-500/10'
                      : 'bg-white/5 hover:bg-white/10'
                  } transition-colors`}
                >
                  <td className="px-3 py-2 font-mono text-gray-400">{qubit.index}</td>
                  <td className="px-3 py-2 text-center font-mono font-bold text-blue-400">{qubit.alice_bit}</td>
                  <td className={`px-3 py-2 text-center font-mono ${
                    qubit.bases_match ? 'text-green-400 font-bold' : 'text-gray-400'
                  }`}>
                    {qubit.alice_basis}
                  </td>
                  <td className="px-3 py-2 text-center font-mono text-purple-400">{qubit.alice_state}</td>
                  {eve_fraction > 0 && (
                    <>
                      <td className="px-3 py-2 text-center">
                        {qubit.eve_intercepted ? (
                          <span className="text-red-400" title="Eve intercepted this qubit">👁️</span>
                        ) : (
                          <span className="text-gray-600">-</span>
                        )}
                      </td>
                      <td className={`px-3 py-2 text-center font-mono ${
                        qubit.eve_intercepted && qubit.eve_caused_error ? 'text-red-400 font-bold' : 'text-gray-500'
                      }`}>
                        {qubit.eve_intercepted ? qubit.eve_basis : '-'}
                      </td>
                    </>
                  )}
                  <td className={`px-3 py-2 text-center font-mono ${
                    qubit.bases_match ? 'text-green-400 font-bold' : 'text-orange-400'
                  }`}>
                    {qubit.bob_basis}
                  </td>
                  <td className="px-3 py-2 text-center font-mono font-bold text-cyan-400">{qubit.bob_measured}</td>
                  <td className="px-3 py-2 text-center">
                    {qubit.bases_match ? (
                      <span className="text-green-400 text-xl" title="Bases matched!">✓</span>
                    ) : (
                      <span className="text-orange-400 text-xl" title="Bases different">✗</span>
                    )}
                  </td>
                  <td className="px-3 py-2 text-center">
                    {qubit.bits_match ? (
                      <span className="text-green-400 text-xl">✓</span>
                    ) : (
                      <span className="text-red-400 text-xl">✗</span>
                    )}
                  </td>
                  <td className="px-3 py-2 text-center">
                    {qubit.kept_in_key ? (
                      <span className="text-green-400 font-bold">Yes</span>
                    ) : (
                      <span className="text-gray-500">No</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="bg-white/5 rounded-lg p-4 space-y-2">
          <h4 className="text-sm font-semibold text-gray-400">Legend:</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-gray-400">
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 bg-green-500/20 rounded"></span>
              <span>Bases matched - bit should be correct (unless errors)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-4 h-4 bg-white/5 rounded"></span>
              <span>Bases didn't match - bit is random (50/50)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-400 text-xl">✓</span>
              <span>Match or correct</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-orange-400 text-xl">✗</span>
              <span>Bases different</span>
            </div>
            {eve_fraction > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-red-400">👁️</span>
                <span>Eve intercepted this qubit</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="stat-card bg-green-500/10 border-green-500/30">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">When Bases Matched:</h3>
          <p className="text-2xl font-bold text-green-400">{summary.correct_when_bases_match}/{summary.matching_bases}</p>
          <p className="text-xs text-gray-400 mt-1">
            {((summary.correct_when_bases_match / Math.max(summary.matching_bases, 1)) * 100).toFixed(1)}% correct
            {summary.matching_bases > 0 && summary.correct_when_bases_match < summary.matching_bases && (
              <span className="text-red-400"> (errors from noise/Eve)</span>
            )}
          </p>
        </div>

        <div className="stat-card bg-orange-500/10 border-orange-500/30">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">When Bases Didn't Match:</h3>
          <p className="text-2xl font-bold text-orange-400">
            {summary.correct_when_bases_dont_match}/{summary.non_matching_bases}
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {summary.non_matching_bases > 0
              ? `${((summary.correct_when_bases_dont_match / summary.non_matching_bases) * 100).toFixed(1)}% correct (random, ~50% expected)`
              : 'N/A - all bases matched'
            }
          </p>
        </div>
      </div>

      {/* Eve Impact */}
      {eve_fraction > 0 && summary.eve_interceptions > 0 && (
        <div className="stat-card bg-red-500/10 border-red-500/30">
          <h3 className="text-sm font-semibold text-gray-300 mb-2 flex items-center gap-2">
            <span>👁️</span> Eve's Impact:
          </h3>
          <div className="space-y-2 text-sm">
            <p className="text-gray-300">
              Eve intercepted <strong className="text-red-400">{summary.eve_interceptions}</strong> qubits and caused{' '}
              <strong className="text-red-400">{summary.eve_caused_errors}</strong> errors
            </p>
            <p className="text-xs text-gray-400">
              When Eve intercepts a qubit and measures in wrong basis (50% chance), she has 50% chance of flipping
              the bit. This introduces ~25% error rate on intercepted qubits, which increases the QBER and reveals eavesdropping.
            </p>
          </div>
        </div>
      )}

      {/* Final Sifted Key */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <span>🔑</span> Final Sifted Key (from matched bases only):
        </h3>
        <div className="bg-black/40 rounded-lg p-4 font-mono text-sm break-all border border-green-500/30">
          {sifted_key}
        </div>
        <p className="text-xs text-gray-400">
          This key is created from the {summary.matching_bases} qubits where Alice and Bob used the same basis.
          The QBER of {(qber * 100).toFixed(1)}% indicates the error rate in this sifted key.
        </p>
      </div>
    </div>
  )
}

export default DetailedSimulation
