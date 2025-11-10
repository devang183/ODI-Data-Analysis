import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import { getCustomPhaseAnalysis, searchPlayers } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const PhasePerformance = () => {
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [loading, setLoading] = useState(false)

  // Form parameters
  const [ballsBefore, setBallsBefore] = useState(15)
  const [overStart, setOverStart] = useState(7)
  const [oversToAnalyze, setOversToAnalyze] = useState(3)
  const [minBallsInPhase, setMinBallsInPhase] = useState(10)

  // Results
  const [analysisData, setAnalysisData] = useState(null)

  useEffect(() => {
    loadPlayers()
  }, [])

  const loadPlayers = async () => {
    try {
      const response = await searchPlayers()
      setPlayers(response.data.data || [])
    } catch (err) {
      console.error('Error loading players:', err)
    }
  }

  const loadAnalysis = async () => {
    if (!selectedPlayer) {
      alert('Please select a player')
      return
    }

    setLoading(true)
    try {
      const response = await getCustomPhaseAnalysis(selectedPlayer.value, {
        balls_before: ballsBefore,
        over_start: overStart,
        overs_to_analyze: oversToAnalyze,
        min_balls_in_phase: minBallsInPhase
      })
      setAnalysisData(response.data)
    } catch (err) {
      alert('Error loading analysis or no data found for the given criteria')
      setAnalysisData(null)
    } finally {
      setLoading(false)
    }
  }

  const formatRunDistribution = (distribution) => {
    if (!distribution) return []
    return distribution.map(item => ({
      name: item.run_range,
      frequency: item.frequency
    }))
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2 className="page-title">Phase Performance Analysis</h2>
        <p className="page-subtitle">Analyze performance in custom batting phases</p>
      </div>

      <div className="card">
        <h3 className="card-title mb-3">Analysis Parameters</h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Select Player</label>
            <Select
              value={selectedPlayer}
              onChange={setSelectedPlayer}
              options={players.map(p => ({ value: p, label: p }))}
              placeholder="Search for a player..."
              isClearable
              isSearchable
              styles={{
                control: (base) => ({
                  ...base,
                  minHeight: '42px',
                  borderColor: '#e1e8ed'
                }),
                menu: (base) => ({
                  ...base,
                  zIndex: 100
                })
              }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              Balls Played Before Phase
              <span style={{ fontSize: '12px', color: '#657786', display: 'block' }}>
                Minimum balls faced before analysis phase
              </span>
            </label>
            <input
              type="number"
              className="form-select"
              value={ballsBefore}
              onChange={(e) => setBallsBefore(parseInt(e.target.value) || 0)}
              min="0"
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              Overs Played Before Phase
              <span style={{ fontSize: '12px', color: '#657786', display: 'block' }}>
                Over number when analysis phase begins
              </span>
            </label>
            <input
              type="number"
              className="form-select"
              value={overStart}
              onChange={(e) => setOverStart(parseInt(e.target.value) || 0)}
              min="0"
              max="49"
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              Next Overs to Analyze
              <span style={{ fontSize: '12px', color: '#657786', display: 'block' }}>
                Number of overs in analysis phase
              </span>
            </label>
            <input
              type="number"
              className="form-select"
              value={oversToAnalyze}
              onChange={(e) => setOversToAnalyze(parseInt(e.target.value) || 1)}
              min="1"
              max="10"
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              Balls in Next Phase
              <span style={{ fontSize: '12px', color: '#657786', display: 'block' }}>
                Minimum balls to face in analysis phase
              </span>
            </label>
            <input
              type="number"
              className="form-select"
              value={minBallsInPhase}
              onChange={(e) => setMinBallsInPhase(parseInt(e.target.value) || 1)}
              min="1"
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button
              className="btn btn-primary"
              onClick={loadAnalysis}
              disabled={!selectedPlayer || loading}
              style={{ width: '100%' }}
            >
              {loading ? 'Analyzing...' : 'Analyze Performance'}
            </button>
          </div>
        </div>

        {analysisData && (
          <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
            <p style={{ fontSize: '14px', color: '#657786', margin: 0 }}>
              <strong>Query:</strong> If {selectedPlayer.label} has played {ballsBefore} balls by over {overStart},
              what happens in the next {oversToAnalyze} overs (minimum {minBallsInPhase} balls)?
            </p>
          </div>
        )}
      </div>

      {analysisData && (
        <>
          {/* Summary Stats */}
          <div className="card">
            <h3 className="card-title mb-3">Summary Statistics</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
              <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#1da1f2', marginBottom: '0.5rem' }}>
                  {analysisData.summary.avg_runs_per_ball || 0}
                </div>
                <div style={{ fontSize: '14px', color: '#657786' }}>Average Runs</div>
              </div>

              <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#17bf63', marginBottom: '0.5rem' }}>
                  {analysisData.summary.strike_rate || 0}
                </div>
                <div style={{ fontSize: '14px', color: '#657786' }}>Strike Rate</div>
              </div>

              <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#e0245e', marginBottom: '0.5rem' }}>
                  {analysisData.summary.dismissal_rate || 0}%
                </div>
                <div style={{ fontSize: '14px', color: '#657786' }}>Dismissal Rate</div>
              </div>

              <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#794bc4', marginBottom: '0.5rem' }}>
                  {analysisData.summary.innings_analyzed || 0}
                </div>
                <div style={{ fontSize: '14px', color: '#657786' }}>Innings Analyzed</div>
              </div>
            </div>
          </div>

          {/* Run Distribution Chart */}
          {analysisData.run_distribution && analysisData.run_distribution.length > 0 && (
            <div className="card">
              <h3 className="card-title mb-3">Run Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={formatRunDistribution(analysisData.run_distribution)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="frequency" fill="#1da1f2" name="Frequency" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Totals */}
          <div className="card">
            <h3 className="card-title mb-3">Detailed Totals</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
              <div style={{ padding: '1rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '14px', color: '#657786', marginBottom: '0.5rem' }}>Total Runs Scored</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#14171a' }}>
                  {analysisData.totals.total_runs}
                </div>
              </div>

              <div style={{ padding: '1rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '14px', color: '#657786', marginBottom: '0.5rem' }}>Total Balls Faced</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#14171a' }}>
                  {analysisData.totals.total_balls}
                </div>
              </div>

              <div style={{ padding: '1rem', backgroundColor: '#f7f9fa', borderRadius: '8px' }}>
                <div style={{ fontSize: '14px', color: '#657786', marginBottom: '0.5rem' }}>Times Dismissed</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#14171a' }}>
                  {analysisData.totals.times_dismissed}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {!analysisData && !loading && (
        <div className="card">
          <div style={{ textAlign: 'center', padding: '3rem', color: '#657786' }}>
            <p>Select a player and configure parameters to analyze performance</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default PhasePerformance
