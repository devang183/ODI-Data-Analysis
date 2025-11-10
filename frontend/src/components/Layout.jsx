import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { FiMenu, FiX, FiSearch, FiBarChart2, FiPieChart, FiTrendingUp, FiTarget, FiUsers, FiAward, FiSettings } from 'react-icons/fi'
import ShareMenu from './ShareMenu'
import '../styles/Layout.css'

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const location = useLocation()

  const menuItems = [
    { path: '/search', icon: <FiSearch />, label: 'Search' },
    { path: '/phase-performance', icon: <FiBarChart2 />, label: 'Phase Performance' },
    { path: '/dismissal-patterns', icon: <FiPieChart />, label: 'Dismissal Patterns' },
    { path: '/batting-stats', icon: <FiTrendingUp />, label: 'Batting Stats' },
    { path: '/bowling-stats', icon: <FiTarget />, label: 'Bowling Stats' },
    { path: '/vs-bowler', icon: <FiUsers />, label: 'Vs Bowler' },
    { path: '/motm', icon: <FiAward />, label: 'MOTM' },
    { path: '/admin', icon: <FiSettings />, label: 'Admin' }
  ]

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <button
            className="menu-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <FiX /> : <FiMenu />}
          </button>
          <h1 className="app-title">ODI Cricket Analytics</h1>
        </div>
        <div className="header-right">
          <ShareMenu />
        </div>
      </header>

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className={`main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
        {children}
      </main>
    </div>
  )
}

export default Layout
