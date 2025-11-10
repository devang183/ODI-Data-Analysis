import React, { useState, useEffect } from 'react'
import { getDatabaseOverview, validateData } from '../services/api'

const Admin = () => {
  const [overview, setOverview] = useState(null)
  const [validation, setValidation] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadOverview()
  }, [])

  const loadOverview = async () => {
    setLoading(true)
    try {
      const response = await getDatabaseOverview()
      setOverview(response.data)
    } catch (err) {
      console.error('Error loading overview:', err)
    } finally {
      setLoading(false)
    }
  }

  const runValidation = async () => {
    setLoading(true)
    try {
      const response = await validateData()
      setValidation(response.data)
    } catch (err) {
      console.error('Error validating data:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Admin Dashboard</h1>
        <p className="page-subtitle">Database management and statistics</p>
      </div>

      {loading && <div className="loading">Loading...</div>}

      {!loading && overview && (
        <>
          <div className="card">
            <h3 className="card-title mb-3">Database Overview</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Total Matches</div>
                <div className="stat-value">{overview.overview.total_matches}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total Seasons</div>
                <div className="stat-value">{overview.overview.total_seasons}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total Venues</div>
                <div className="stat-value">{overview.overview.total_venues}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Total Players</div>
                <div className="stat-value">{overview.total_players}</div>
              </div>
            </div>

            <div className="mt-4">
              <h4>Date Range</h4>
              <p>
                <strong>Earliest Match:</strong>{' '}
                {overview.overview.earliest_match ? overview.overview.earliest_match.replace(/"/g, '') : 'N/A'}
              </p>
              <p>
                <strong>Latest Match:</strong>{' '}
                {overview.overview.latest_match ? overview.overview.latest_match.replace(/"/g, '') : 'N/A'}
              </p>
            </div>
          </div>

          {overview.teams && overview.teams.length > 0 && (
            <div className="card">
              <h3 className="card-title mb-3">Teams</h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Team</th>
                    <th>Matches Played</th>
                  </tr>
                </thead>
                <tbody>
                  {overview.teams.slice(0, 20).map((team, index) => (
                    <tr key={team.team_name}>
                      <td>{index + 1}</td>
                      <td><strong>{team.team_name}</strong></td>
                      <td>{team.matches_played}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      <div className="card">
        <h3 className="card-title mb-3">Data Validation</h3>
        <button className="btn btn-primary" onClick={runValidation}>
          Run Validation
        </button>

        {validation && (
          <div className="mt-4">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-label">Matches Without Innings</div>
                <div className="stat-value">{validation.validation.matches_without_innings}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Matches Without Outcome</div>
                <div className="stat-value">{validation.validation.matches_without_outcome}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Incomplete Data</div>
                <div className="stat-value">{validation.validation.matches_with_incomplete_data}</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Admin
