import React, { useState, useRef, useEffect } from 'react'
import { FiShare2, FiDownload, FiMoreHorizontal } from 'react-icons/fi'
import { FaWhatsapp, FaLinkedin } from 'react-icons/fa'
import { SiGmail } from 'react-icons/si'
import html2canvas from 'html2canvas'
import '../styles/ShareMenu.css'

const ShareMenu = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [isCapturing, setIsCapturing] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const getCurrentPageTitle = () => {
    const path = window.location.pathname
    const titles = {
      '/search': 'Match Search',
      '/phase-performance': 'Phase Performance',
      '/dismissal-patterns': 'Dismissal Patterns',
      '/batting-stats': 'Batting Statistics',
      '/bowling-stats': 'Bowling Statistics',
      '/vs-bowler': 'Batter vs Bowler',
      '/motm': 'Man of the Match',
      '/admin': 'Admin Dashboard'
    }
    return titles[path] || 'ODI Cricket Analytics'
  }

  const getShareText = () => {
    return `Check out ${getCurrentPageTitle()} on ODI Cricket Analytics`
  }

  const handleWhatsAppShare = () => {
    const text = encodeURIComponent(getShareText())
    const url = encodeURIComponent(window.location.href)
    window.open(`https://wa.me/?text=${text}%20${url}`, '_blank')
    setIsOpen(false)
  }

  const handleGmailShare = () => {
    const subject = encodeURIComponent(getCurrentPageTitle())
    const body = encodeURIComponent(`${getShareText()}\n\n${window.location.href}`)
    window.open(`https://mail.google.com/mail/?view=cm&fs=1&su=${subject}&body=${body}`, '_blank')
    setIsOpen(false)
  }

  const handleLinkedInShare = () => {
    const url = encodeURIComponent(window.location.href)
    window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank')
    setIsOpen(false)
  }

  const handleSaveAsImage = async () => {
    setIsCapturing(true)
    try {
      // Get the main content area
      const mainContent = document.querySelector('.main-content')
      if (!mainContent) {
        alert('Could not capture page content')
        return
      }

      // Scroll to top
      mainContent.scrollTop = 0

      // Capture the screenshot
      const canvas = await html2canvas(mainContent, {
        allowTaint: true,
        useCORS: true,
        scale: 2, // Higher quality
        backgroundColor: '#ffffff',
        logging: false,
        windowWidth: mainContent.scrollWidth,
        windowHeight: mainContent.scrollHeight
      })

      // Convert to blob and download
      canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        const fileName = `${getCurrentPageTitle().replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.png`
        link.download = fileName
        link.href = url
        link.click()
        URL.revokeObjectURL(url)
      })
    } catch (error) {
      console.error('Error capturing screenshot:', error)
      alert('Failed to capture screenshot. Please try again.')
    } finally {
      setIsCapturing(false)
      setIsOpen(false)
    }
  }

  const handleMoreOptions = () => {
    if (navigator.share) {
      navigator.share({
        title: getCurrentPageTitle(),
        text: getShareText(),
        url: window.location.href
      }).catch(err => {
        if (err.name !== 'AbortError') {
          console.log('Error sharing:', err)
        }
      })
    } else {
      // Fallback - copy to clipboard
      navigator.clipboard.writeText(window.location.href)
      alert('Link copied to clipboard!')
    }
    setIsOpen(false)
  }

  return (
    <div className="share-menu-container" ref={menuRef}>
      <button
        className="share-btn"
        onClick={() => setIsOpen(!isOpen)}
        disabled={isCapturing}
      >
        <FiShare2 /> {isCapturing ? 'Capturing...' : 'Share'}
      </button>

      {isOpen && (
        <div className="share-dropdown">
          <button className="share-option" onClick={handleWhatsAppShare}>
            <FaWhatsapp className="share-icon whatsapp" />
            <span>WhatsApp</span>
          </button>

          <button className="share-option" onClick={handleGmailShare}>
            <SiGmail className="share-icon gmail" />
            <span>Gmail</span>
          </button>

          <button className="share-option" onClick={handleLinkedInShare}>
            <FaLinkedin className="share-icon linkedin" />
            <span>LinkedIn</span>
          </button>

          <div className="share-divider"></div>

          <button className="share-option" onClick={handleSaveAsImage}>
            <FiDownload className="share-icon download" />
            <span>Save as Image</span>
          </button>

          <button className="share-option" onClick={handleMoreOptions}>
            <FiMoreHorizontal className="share-icon more" />
            <span>More Options</span>
          </button>
        </div>
      )}
    </div>
  )
}

export default ShareMenu
