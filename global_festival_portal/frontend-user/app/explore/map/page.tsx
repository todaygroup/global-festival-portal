import React from 'react';
import Navigation from '../../components/Navigation';

const MapPage = () => {
  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      <main style={{ padding: '3rem 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem' }}>Global Festival Map</h1>
          <p style={{ color: '#666' }}>Visually discover festivals across every continent.</p>
        </div>

        <div style={{ 
          width: '100%', 
          height: '70vh', 
          backgroundColor: '#e0e0e0', 
          borderRadius: '20px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          position: 'relative',
          border: '2px solid #ddd',
          backgroundImage: 'url("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/World_map_blank.svg/1200px-World_map_blank.svg.png")',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}>
          <div style={{ 
            position: 'absolute', 
            backgroundColor: 'rgba(255, 77, 77, 0.8)', 
            width: '15px', 
            height: '15px', 
            borderRadius: '50%', 
            top: '40%', 
            left: '45%', 
            boxShadow: '0 0 10px rgba(0,0,0,0.5)',
            cursor: 'pointer' 
          }} title="Example Festival"></div>
          
          <div style={{ 
            position: 'absolute', 
            backgroundColor: 'rgba(255, 77, 77, 0.8)', 
            width: '15px', 
            height: '15px', 
            borderRadius: '50%', 
            top: '35%', 
            left: '75%', 
            boxShadow: '0 0 10px rgba(0,0,0,0.5)',
            cursor: 'pointer' 
          }} title="Example Festival"></div>

          <div style={{ 
            backgroundColor: 'white', 
            padding: '1rem 2rem', 
            borderRadius: '30px', 
            boxShadow: '0 4px 10px rgba(0,0,0,0.3)', 
            position: 'absolute', 
            bottom: '20px', 
            left: '50%', 
            transform: 'translateX(-50%)',
            fontWeight: 'bold',
            color: '#ff4d4d',
            border: '2px solid #ff4d4d'
          }}>
            Interactive Map v1.0 (Powered by PostGIS)
          </div>
        </div>

        <div style={{ marginTop: '3rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '12px', border: '1px solid #ddd' }}>
            <h3>Filter by Continent</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
              {['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania'].map(c => (
                <span key={c} style={{ padding: '0.4rem 0.8rem', backgroundColor: '#eee', borderRadius: '15px', fontSize: '0.8rem', cursor: 'pointer' }}>{c}</span>
              ))}
            </div>
          </div>
          <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '12px', border: '1px solid #ddd' }}>
            <h3>Filter by Date</h3>
            <input type="date" style={{ width: '100%', padding: '0.5rem', marginTop: '1rem' }} />
          </div>
          <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '12px', border: '1px solid #ddd' }}>
            <h3>Filter by Vibe</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
              {['Chill', 'High-Energy', 'Mystical', 'Traditional', 'Modern'].map(v => (
                <span key={v} style={{ padding: '0.4rem 0.8rem', backgroundColor: '#eee', borderRadius: '15px', fontSize: '0.8rem', cursor: 'pointer' }}>{v}</span>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div}
  );
};

export default MapPage;
