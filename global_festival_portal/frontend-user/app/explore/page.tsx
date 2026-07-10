import React from 'react';
import Navigation from '../components/Navigation';

const ExplorePage = ({ type = 'list' }) => {
  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      <main style={{ padding: '3rem 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>Explore Global Festivals</h1>
        
        <div style={{ display: 'flex', gap: '2rem' }}>
          <aside style={{ width: '300px', backgroundColor: 'white', padding: '1.5rem', borderRadius: '12px', height: 'fit-content', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
            <h3>🔍 Filters</h3>
            <div style={{ margin: '1rem 0' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Region</label>
              <select style={{ width: '100%', padding: '0.5rem' }}><option>All Regions</option><option>Asia</option><option>Europe</option><option>Americas</option></select>
            </div>
            <div style={{ margin: '1rem 0' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Vibe</label>
              <select style={{ width: '100%', padding: '0.5rem' }}><option>All Vibes</option><option>High Energy</option><option>Chill</option><option>Family-Friendly</option></select>
            </div>
            <div style={{ margin: '1rem 0' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Category</label>
              <select style={{ width: '100%', padding: '0.5rem' }}><option>All Categories</option><option>Music</option><option>Art</option><option>Food</option></select>
            </div>
            <button style={{ width: '100%', padding: '0.8rem', backgroundColor: '#ff4d4d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Apply Filters</button>
          </aside>

          <section style={{ flex: 1 }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '2rem' }}>
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} style={{ backgroundColor: 'white', borderRadius: '12px', overflow: 'hidden', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', border: '1px solid #ddd' }}>
                  <div style={{ height: '180px', backgroundColor: '#ddd', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                    Image Placeholder
                  </div>
                  <div style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span style={{ backgroundColor: '#ff4d4d', color: 'white', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem' }}>Verified</span>
                      <span style={{ fontSize: '0.8rem', color: '#888' }}>Japan</span>
                    </div>
                    <h4 style={{ margin: '0 0 1rem 0', fontSize: '1.2rem' }}>Festival Name {i}</h4>
                    <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
                      Date: 2026-04-15 <br />
                      Vibe: High Energy
                    </div>
                    <button style={{ width: '100%', padding: '0.6rem', border: '1px solid #ff4d4d', color: '#ff4d4d', backgroundColor: 'transparent', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>View Details</button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default ExplorePage;
