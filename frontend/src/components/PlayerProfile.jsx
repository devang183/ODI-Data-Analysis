import React from 'react'

const PlayerProfile = ({ profile }) => {
  if (!profile) return null

  return (
    <div className="player-profile-card" style={{
      backgroundColor: '#f8f9fa',
      border: '1px solid #e1e8ed',
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '20px',
      display: 'flex',
      gap: '20px',
      alignItems: 'center'
    }}>
      {profile.image_path && (
        <div style={{ flexShrink: 0 }}>
          <img
            src={profile.image_path}
            alt={profile.fullname}
            style={{
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              objectFit: 'cover',
              border: '3px solid #0066cc'
            }}
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
        </div>
      )}

      <div style={{ flex: 1 }}>
        <h2 style={{ margin: '0 0 10px 0', fontSize: '24px', color: '#14171a' }}>
          {profile.fullname}
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '10px',
          marginTop: '15px'
        }}>
          {profile.country_name && (
            <div className="profile-info-item">
              <span style={{ fontSize: '12px', color: '#657786', fontWeight: 'bold', display: 'block' }}>
                Country
              </span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
                {profile.country_image_path && (
                  <img
                    src={profile.country_image_path}
                    alt={profile.country_name}
                    style={{ width: '20px', height: '15px', objectFit: 'cover' }}
                    onError={(e) => { e.target.style.display = 'none' }}
                  />
                )}
                <span style={{ fontSize: '14px', color: '#14171a', fontWeight: '500' }}>
                  {profile.country_name}
                </span>
              </div>
            </div>
          )}

          {profile.position && (
            <div className="profile-info-item">
              <span style={{ fontSize: '12px', color: '#657786', fontWeight: 'bold', display: 'block' }}>
                Role
              </span>
              <span style={{ fontSize: '14px', color: '#14171a', fontWeight: '500', display: 'block', marginTop: '4px' }}>
                {profile.position}
              </span>
            </div>
          )}

          {profile.battingstyle && (
            <div className="profile-info-item">
              <span style={{ fontSize: '12px', color: '#657786', fontWeight: 'bold', display: 'block' }}>
                Batting
              </span>
              <span style={{ fontSize: '14px', color: '#14171a', fontWeight: '500', display: 'block', marginTop: '4px' }}>
                {profile.battingstyle}
              </span>
            </div>
          )}

          {profile.bowlingstyle && profile.bowlingstyle.toLowerCase() !== 'null' && (
            <div className="profile-info-item">
              <span style={{ fontSize: '12px', color: '#657786', fontWeight: 'bold', display: 'block' }}>
                Bowling
              </span>
              <span style={{ fontSize: '14px', color: '#14171a', fontWeight: '500', display: 'block', marginTop: '4px' }}>
                {profile.bowlingstyle}
              </span>
            </div>
          )}

          {profile.dateofbirth && (
            <div className="profile-info-item">
              <span style={{ fontSize: '12px', color: '#657786', fontWeight: 'bold', display: 'block' }}>
                Date of Birth
              </span>
              <span style={{ fontSize: '14px', color: '#14171a', fontWeight: '500', display: 'block', marginTop: '4px' }}>
                {profile.dateofbirth}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PlayerProfile
