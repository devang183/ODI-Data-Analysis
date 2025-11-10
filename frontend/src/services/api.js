import axios from 'axios'

// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
  ? `${import.meta.env.VITE_API_BASE_URL}/api`
  : 'http://localhost:5001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Search APIs
export const searchMatches = (params) => api.get('/search/matches', { params })
export const searchPlayers = () => api.get('/search/players')
export const searchTeams = () => api.get('/search/teams')
export const searchVenues = () => api.get('/search/venues')
export const searchSeasons = () => api.get('/search/seasons')
export const getMatchDetails = (matchId) => api.get(`/search/match/${matchId}`)

// Batting Stats APIs
export const getPlayerBattingStats = (playerName) => api.get(`/batting-stats/player/${encodeURIComponent(playerName)}`)
export const getPlayerInnings = (playerName) => api.get(`/batting-stats/player/${encodeURIComponent(playerName)}/innings`)
export const getPlayerVsTeam = (playerName, teamName) => api.get(`/batting-stats/player/${encodeURIComponent(playerName)}/vs-team/${encodeURIComponent(teamName)}`)
export const getBattingLeaderboard = (params) => api.get('/batting-stats/leaderboard', { params })

// Bowling Stats APIs
export const getPlayerBowlingStats = (playerName) => api.get(`/bowling-stats/player/${encodeURIComponent(playerName)}`)
export const getPlayerBowlingSpells = (playerName) => api.get(`/bowling-stats/player/${encodeURIComponent(playerName)}/spells`)
export const getPlayerBowlingVsTeam = (playerName, teamName) => api.get(`/bowling-stats/player/${encodeURIComponent(playerName)}/vs-team/${encodeURIComponent(teamName)}`)
export const getBowlingLeaderboard = (params) => api.get('/bowling-stats/leaderboard', { params })

// Phase Performance APIs
export const getPlayerPhasePerformance = (playerName) => api.get(`/phase-performance/player/${encodeURIComponent(playerName)}`)
export const getPlayerBowlingPhasePerformance = (playerName) => api.get(`/phase-performance/player/${encodeURIComponent(playerName)}/bowling`)
export const getTeamPhasePerformance = (teamName) => api.get(`/phase-performance/team/${encodeURIComponent(teamName)}`)
export const getCustomPhaseAnalysis = (playerName, params) => api.get(`/phase-performance/player/${encodeURIComponent(playerName)}/custom-analysis`, { params })

// Dismissal Patterns APIs
export const getPlayerDismissalPatterns = (playerName) => api.get(`/dismissal-patterns/player/${encodeURIComponent(playerName)}`)
export const getPlayerDismissalByPhase = (playerName) => api.get(`/dismissal-patterns/player/${encodeURIComponent(playerName)}/by-phase`)
export const getBowlerVictims = (bowlerName) => api.get(`/dismissal-patterns/bowler/${encodeURIComponent(bowlerName)}/victims`)

// Vs Bowler APIs
export const getBatterVsBowler = (batterName, bowlerName) => api.get(`/vs-bowler/batter/${encodeURIComponent(batterName)}/bowler/${encodeURIComponent(bowlerName)}`)
export const getBatterVsAllBowlers = (batterName, params) => api.get(`/vs-bowler/batter/${encodeURIComponent(batterName)}/bowlers`, { params })
export const getBowlerVsAllBatters = (bowlerName, params) => api.get(`/vs-bowler/bowler/${encodeURIComponent(bowlerName)}/batters`, { params })

// MOTM APIs
export const getPlayerMOTMAwards = (playerName) => api.get(`/motm/player/${encodeURIComponent(playerName)}`)
export const getMOTMLeaderboard = (params) => api.get('/motm/leaderboard', { params })
export const getMOTMByYear = () => api.get('/motm/by-year')
export const getTeamMOTMPlayers = (teamName) => api.get(`/motm/team/${encodeURIComponent(teamName)}`)

// Admin APIs
export const getDatabaseOverview = () => api.get('/admin/stats/overview')
export const validateData = () => api.get('/admin/data/validate')
export const exportData = (filters) => api.post('/admin/data/export', filters)
export const clearCache = () => api.post('/admin/cache/clear')
export const getLogs = () => api.get('/admin/logs')

// Player Profile APIs
export const getPlayerProfile = (playerName) => api.get(`/player-profile/${encodeURIComponent(playerName)}`)
export const searchPlayerProfiles = (searchTerm) => api.get('/player-profile/search', { params: { q: searchTerm } })

export default api
