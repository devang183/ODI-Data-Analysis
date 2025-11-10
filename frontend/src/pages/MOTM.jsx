import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import { getMOTMLeaderboard, getPlayerMOTMAwards, searchPlayers } from '../services/api'

const MOTM = () => {
  const [leaderboard, setLeaderboard] = useState([])
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState(null)
  const [playerAwards, setPlayerAwards] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadLeaderboard()
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

  const loadLeaderboard = async () => {
    setLoading(true)
    try {
      const response = await getMOTMLeaderboard({ limit: 50 })
      setLeaderboard(response.data.data || [])
    } catch (err) {
      console.error('Error loading leaderboard:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadPlayerAwards = async () => {
    if (!selectedPlayer) return

    setLoading(true)
    try {
      const response = await getPlayerMOTMAwards(selectedPlayer.value)
      setPlayerAwards(response.data)
    } catch (err) {
      alert('Error loading player awards')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Man of the Match Awards</h1>
        <p className="page-subtitle">Top performers in ODI cricket</p>
      </div>

      <div className="card">
        <h3 className="card-title mb-3">Player MOTM Awards</h3>
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
              onClick={loadPlayerAwards}
              disabled={!selectedPlayer}
            >
              Load Awards
            </button>
          </div>
        </div>

        {playerAwards && playerAwards.statistics && (
          <div className="stats-grid mt-3">
            <div className="stat-card">
              <div className="stat-label">Total Awards</div>
              <div className="stat-value">{playerAwards.statistics.total_awards || 0}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">In Wins</div>
              <div className="stat-value">{playerAwards.statistics.awards_in_wins || 0}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">In Losses</div>
              <div className="stat-value">{playerAwards.statistics.awards_in_losses || 0}</div>
            </div>
          </div>
        )}

        {playerAwards && playerAwards.awards && playerAwards.awards.length > 0 && (
          <div className="mt-4">
            <h4 className="mb-2">Award Details</h4>
            <div style={{
              maxHeight: playerAwards.awards.length > 5 ? '350px' : 'auto',
              overflowY: playerAwards.awards.length > 5 ? 'auto' : 'visible',
              border: playerAwards.awards.length > 5 ? '1px solid #e1e8ed' : 'none',
              borderRadius: '4px'
            }}>
              <table className="data-table">
                <thead style={{
                  position: playerAwards.awards.length > 5 ? 'sticky' : 'static',
                  top: 0,
                  backgroundColor: '#fff',
                  zIndex: 10
                }}>
                  <tr>
                    <th>Date</th>
                    <th>Venue</th>
                    <th>Teams</th>
                    <th>Winner</th>
                    <th>Event</th>
                  </tr>
                </thead>
                <tbody>
                  {playerAwards.awards.map((award, index) => (
                    <tr key={index}>
                      <td>{award.match_date ? award.match_date.replace(/"/g, '') : 'N/A'}</td>
                      <td>{award.venue}</td>
                      <td>
                        {award.teams && (Array.isArray(award.teams)
                          ? award.teams.join(' vs ')
                          : (typeof award.teams === 'string' ? JSON.parse(award.teams).join(' vs ') : 'N/A'))}
                      </td>
                      <td><strong>{award.winner}</strong></td>
                      <td>{award.event_name}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="card-title mb-3">MOTM Leaderboard</h3>
        {loading ? (
          <div className="loading">Loading leaderboard...</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Player</th>
                <th>Total Awards</th>
                <th>First Award</th>
                <th>Latest Award</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((player, index) => (
                <tr key={player.player_name}>
                  <td>{index + 1}</td>
                  <td><strong>{player.player_name}</strong></td>
                  <td>{player.total_awards}</td>
                  <td>{player.first_award ? player.first_award.replace(/"/g, '') : 'N/A'}</td>
                  <td>{player.latest_award ? player.latest_award.replace(/"/g, '') : 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default MOTM
