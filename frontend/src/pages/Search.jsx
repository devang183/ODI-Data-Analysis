import React, { useState, useEffect } from 'react'
import { searchMatches, searchTeams, searchPlayers, searchVenues, searchSeasons, getMatchDetails } from '../services/api'
import { FiSearch, FiFilter, FiX } from 'react-icons/fi'

const Search = () => {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Filter options
  const [teams, setTeams] = useState([])
  const [venues, setVenues] = useState([])
  const [seasons, setSeasons] = useState([])

  // Filter values
  const [filters, setFilters] = useState({
    team: '',
    venue: '',
    date_from: '',
    date_to: '',
    season: '',
    page: 1,
    limit: 20
  })

  const [selectedMatch, setSelectedMatch] = useState(null)
  const [showFilters, setShowFilters] = useState(true)

  useEffect(() => {
    loadFilterOptions()
  }, [])

  useEffect(() => {
    handleSearch()
  }, [filters.page])

  const loadFilterOptions = async () => {
    try {
      const [teamsRes, venuesRes, seasonsRes] = await Promise.all([
        searchTeams(),
        searchVenues(),
        searchSeasons()
      ])
      setTeams(teamsRes.data.data || [])
      setVenues(venuesRes.data.data || [])
      setSeasons(seasonsRes.data.data || [])
    } catch (err) {
      console.error('Error loading filter options:', err)
    }
  }

  const handleSearch = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await searchMatches(filters)
      setMatches(response.data.data || [])
    } catch (err) {
      setError(err.response?.data?.error || 'Error searching matches')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (field, value) => {
    setFilters({ ...filters, [field]: value, page: 1 })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    handleSearch()
  }

  const clearFilters = () => {
    setFilters({
      team: '',
      venue: '',
      date_from: '',
      date_to: '',
      season: '',
      page: 1,
      limit: 20
    })
  }

  const viewMatchDetails = async (matchId) => {
    try {
      const response = await getMatchDetails(matchId)
      setSelectedMatch(response.data.data)
    } catch (err) {
      alert('Error loading match details')
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Search Matches</h1>
        <p className="page-subtitle">Find and explore ODI matches</p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <FiFilter /> Filters
          </h3>
          <button
            className="btn btn-outline"
            onClick={() => setShowFilters(!showFilters)}
          >
            {showFilters ? 'Hide' : 'Show'}
          </button>
        </div>

        {showFilters && (
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Team</label>
                <select
                  className="form-select"
                  value={filters.team}
                  onChange={(e) => handleFilterChange('team', e.target.value)}
                >
                  <option value="">All Teams</option>
                  {teams.map((team) => (
                    <option key={team} value={team}>{team}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Venue</label>
                <select
                  className="form-select"
                  value={filters.venue}
                  onChange={(e) => handleFilterChange('venue', e.target.value)}
                >
                  <option value="">All Venues</option>
                  {venues.map((venue) => (
                    <option key={venue} value={venue}>{venue}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Season</label>
                <select
                  className="form-select"
                  value={filters.season}
                  onChange={(e) => handleFilterChange('season', e.target.value)}
                >
                  <option value="">All Seasons</option>
                  {seasons.map((season) => (
                    <option key={season} value={season}>{season}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Date From</label>
                <input
                  type="date"
                  className="form-input"
                  value={filters.date_from}
                  onChange={(e) => handleFilterChange('date_from', e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Date To</label>
                <input
                  type="date"
                  className="form-input"
                  value={filters.date_to}
                  onChange={(e) => handleFilterChange('date_to', e.target.value)}
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
              <button type="submit" className="btn btn-primary">
                <FiSearch /> Search
              </button>
              <button type="button" className="btn btn-outline" onClick={clearFilters}>
                <FiX /> Clear Filters
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Results */}
      {loading && <div className="loading">Loading matches...</div>}

      {error && <div className="error">{error}</div>}

      {!loading && !error && matches.length === 0 && (
        <div className="empty-state">No matches found. Try adjusting your filters.</div>
      )}

      {!loading && !error && matches.length > 0 && (
        <div className="card">
          <h3 className="card-title mb-3">Matches ({matches.length})</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Venue</th>
                <th>Teams</th>
                <th>Winner</th>
                <th>Margin</th>
                <th>Season</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {matches.map((match) => (
                <tr key={match.id}>
                  <td>{match.match_date ? match.match_date.replace(/"/g, '') : 'N/A'}</td>
                  <td>{match.venue}</td>
                  <td>
                    {match.teams && (Array.isArray(match.teams)
                      ? match.teams.join(' vs ')
                      : (typeof match.teams === 'string' ? JSON.parse(match.teams).join(' vs ') : 'N/A'))}
                  </td>
                  <td><strong>{match.winner || 'No Result'}</strong></td>
                  <td>
                    {match.win_margin && typeof match.win_margin === 'object'
                      ? Object.entries(match.win_margin)[0]?.join(' ') || 'N/A'
                      : 'N/A'}
                  </td>
                  <td>{match.season}</td>
                  <td>
                    <button
                      className="btn btn-primary"
                      style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                      onClick={() => viewMatchDetails(match.id)}
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Match Details Modal */}
      {selectedMatch && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '2rem'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '2rem',
            maxWidth: '800px',
            maxHeight: '80vh',
            overflow: 'auto',
            position: 'relative'
          }}>
            <button
              onClick={() => setSelectedMatch(null)}
              style={{
                position: 'absolute',
                top: '1rem',
                right: '1rem',
                background: 'none',
                border: 'none',
                fontSize: '1.5rem',
                cursor: 'pointer'
              }}
            >
              <FiX />
            </button>
            <h2>Match Details</h2>
            <pre style={{ overflow: 'auto', maxHeight: '60vh' }}>
              {JSON.stringify(selectedMatch.metadata, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default Search
