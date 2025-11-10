import React, { useState, useEffect } from 'react'
import { getPlayerBattingStats, getBattingLeaderboard, searchPlayers } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import Select from 'react-select'
import PlayerProfile from '../components/PlayerProfile'

const BattingStats = () => {
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [playerStats, setPlayerStats] = useState(null)
  const [playerProfile, setPlayerProfile] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(false)
  const [sortBy, setSortBy] = useState('runs')

  useEffect(() => {
    loadPlayers()
    loadLeaderboard()
  }, [])

  useEffect(() => {
    if (sortBy) {
      loadLeaderboard()
    }
  }, [sortBy])

  const loadPlayers = async () => {
    try {
      const response = await searchPlayers()
      setPlayers(response.data.data || [])
    } catch (err) {
      console.error('Error loading players:', err)
    }
  }

  const loadLeaderboard = async () => {
    setLoading(true)
    try {
      const response = await getBattingLeaderboard({ sort_by: sortBy, limit: 20 })
      setLeaderboard(response.data.data || [])
    } catch (err) {
      console.error('Error loading leaderboard:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadPlayerStats = async () => {
    if (!selectedPlayer) return

    setLoading(true)
    try {
      const response = await getPlayerBattingStats(selectedPlayer.value)
      setPlayerStats(response.data.stats)
      setPlayerProfile(response.data.profile)
    } catch (err) {
      alert('Error loading player stats')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Batting Statistics</h1>
        <p className="page-subtitle">Explore player batting performance</p>
      </div>

      {/* Player Search */}
      <div className="card">
        <h3 className="card-title mb-3">Player Stats</h3>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div className="form-group" style={{ flex: 1 }}>
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
          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button
              className="btn btn-primary"
              onClick={loadPlayerStats}
              disabled={!selectedPlayer}
            >
              Load Stats
            </button>
          </div>
        </div>

        {playerProfile && <PlayerProfile profile={playerProfile} />}

        {playerStats && (
          <div className="stats-grid mt-3">
            <div className="stat-card">
              <div className="stat-label">Matches</div>
              <div className="stat-value">{playerStats.matches_played}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Total Runs</div>
              <div className="stat-value">{playerStats.total_runs}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Average</div>
              <div className="stat-value">{playerStats.batting_average || 'N/A'}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Strike Rate</div>
              <div className="stat-value">{playerStats.strike_rate}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Balls Faced</div>
              <div className="stat-value">{playerStats.balls_faced}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Fours</div>
              <div className="stat-value">{playerStats.fours}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Sixes</div>
              <div className="stat-value">{playerStats.sixes}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Dismissals</div>
              <div className="stat-value">{playerStats.times_dismissed}</div>
            </div>
          </div>
        )}
      </div>

      {/* Leaderboard */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Top Batsmen</h3>
          <div className="form-group" style={{ margin: 0, minWidth: '200px' }}>
            <select
              className="form-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="runs">Most Runs</option>
              <option value="average">Best Average</option>
              <option value="strike_rate">Best Strike Rate</option>
              <option value="matches">Most Matches</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading leaderboard...</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Player</th>
                <th>Matches</th>
                <th>Runs</th>
                <th>Balls</th>
                <th>Average</th>
                <th>Strike Rate</th>
                <th>4s</th>
                <th>6s</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((player, index) => (
                <tr key={player.player_name}>
                  <td>{index + 1}</td>
                  <td><strong>{player.player_name}</strong></td>
                  <td>{player.matches}</td>
                  <td>{player.total_runs}</td>
                  <td>{player.balls_faced}</td>
                  <td>{player.average || 'N/A'}</td>
                  <td>{player.strike_rate}</td>
                  <td>{player.fours}</td>
                  <td>{player.sixes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default BattingStats
