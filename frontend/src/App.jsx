import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Search from './pages/Search'
import PhasePerformance from './pages/PhasePerformance'
import DismissalPatterns from './pages/DismissalPatterns'
import BattingStats from './pages/BattingStats'
import BowlingStats from './pages/BowlingStats'
import VsBowler from './pages/VsBowler'
import MOTM from './pages/MOTM'
import Admin from './pages/Admin'
import './styles/App.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/search" replace />} />
          <Route path="/search" element={<Search />} />
          <Route path="/phase-performance" element={<PhasePerformance />} />
          <Route path="/dismissal-patterns" element={<DismissalPatterns />} />
          <Route path="/batting-stats" element={<BattingStats />} />
          <Route path="/bowling-stats" element={<BowlingStats />} />
          <Route path="/vs-bowler" element={<VsBowler />} />
          <Route path="/motm" element={<MOTM />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
