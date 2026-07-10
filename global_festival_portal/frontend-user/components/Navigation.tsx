import React from 'react';

const Navigation = () => {
  return (
    <nav style={{ 
      display: 'flex', 
      justify-content: 'space-between', 
      alignItems: 'center', 
      padding: '1rem 2rem', 
      backgroundColor: '#1a1a1a', 
      color: 'white',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      borderBottom: '2px solid #ff4d4d'
    }}>
      <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#ff4d4d' }}>
        Festa Guide <span style={{ fontSize: '0.8rem', color: '#ccc', fontWeight: 'normal' }}>(festaguide.com)</span>
      </div>
      <ul style={{ display: 'flex', listStyle: 'none', gap: '2rem', margin: 0 }}>
        <li><a href="/" style={{ color: 'white', textDecoration: 'none' }}>Home</a></li>
        <li><a href="/explore" style={{ color: 'white', textDecoration: 'none' }}>Explore</a></li>
        <li><a href="/explore/map" style={{ color: 'white', textDecoration: 'none' }}>Global Map</a></li>
        <li><a href="/my-page" style={{ color: 'white', textDecoration: 'none' }}>My Page</a></li>
        <li><a href="/info-hub" style={{ color: 'white', textDecoration: 'none' }}>Info Hub</a></li>
      </ul>
      <div>
        <button style={{ padding: '0.5rem 1rem', backgroundColor: '#ff4d4d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Login
        </button>
      </div>
    </nav>
  );
};

export default Navigation;
