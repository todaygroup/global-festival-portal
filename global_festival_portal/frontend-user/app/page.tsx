import React from 'react';
import Navigation from '../components/Navigation';

const HomePage = () => {
  const progress = {
    data_acquisition: 15,
    refinement: 5,
    verification: 2,
    infra_setup: 80,
    ui_implementation: 30,
  };

  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      
      <main style={{ padding: '3rem 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Discover the World's Greatest Festivals</h1>
          <p style={{ fontSize: '1.2rem', color: '#666' }}>The most reliable, comprehensive, and AI-powered global festival portal.</p>
          
          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem' }}>
             <input type="text" placeholder="Search festivals by name, vibe, or country..." style={{ padding: '1rem', width: '400px', borderRadius: '4px', border: '1px solid #ddd' }} />
             <button style={{ padding: '1rem 2rem', backgroundColor: '#ff4d4d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Search</button>
          </div>
        </header>

        <section style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', marginBottom: '3rem' }}>
          <h2 style={{ borderBottom: '2px solid #ff4d4d', display: 'inline-block', marginBottom: '2rem' }}>🚀 System Implementation Progress (Real-time)</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
            {Object.entries(progress).map(([key, value]) => (
              <div key={key} style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ textTransform: 'capitalize', fontWeight: 'bold' }}>{key.replace('_', ' ')}</span>
                  <span>{value}%</span>
                </div>
                <div style={{ backgroundColor: '#eee', borderRadius: '10px', height: '10px', overflow: 'hidden' }}>
                  <div style={{ backgroundColor: '#ff4d4d', width: `${value}%`, height: '100%', transition: 'width 1s ease-in-out' }}></div>
                </div>
              </div>
            ))}
          </div>
          <p style={{ marginTop: '2rem', color: '#888', fontSize: '0.9rem', fontStyle: 'italic' }}>
            * Our Parallel Agent Swarm is currently collecting and verifying real-world data from 100+ countries.
          </p>
        </section>

        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #ddd' }}>
            <h3>Explore Map</h3>
            <p>Discover festivals visually across the globe.</p>
            <a href="/explore/map" style={{ color: '#ff4d4d', fontWeight: 'bold' }}>Enter Map $\rightarrow$</a>
          </div>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #ddd' }}>
            <h3>AI Radar</h3>
            <p>Find festivals tailored to your personal tastes.</p>
            <a href="/explore/radar" style={{ color: '#ff4d4d', fontWeight: 'bold' }}>Start Sync $\rightarrow$</a>
          </div>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #ddd' }}>
            <h3>My Itineraries</h3>
            <p>Plan your dream festival tour with friends.</p>
            <a href="/my-page/itineraries" style={{ color: '#ff4d4d', fontWeight: 'bold' }}>My Plans $\rightarrow$</a>
          </div>
        </section>
      </main>
    </div>
  );
};

export default HomePage;
