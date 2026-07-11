import React from 'react';
import Navigation from '../../components/Navigation';

const ItinerariesPage = () => {
  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      <main style={{ padding: '3rem 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', aligniItems: 'center', marginBottom: '2rem' }}>
          <h1>My Festival Roadmaps</h1>
          <button style={{ padding: '1rem 2rem', backgroundColor: '#ff4d4d', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
            + Create New Itinerary
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>
          <div style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '20px', boxShadow: '0 4px 15px rgba(0,0,0,0.1)', borderTop: '5px solid #ff4d4d' }}>
            <h3 style={{ margin: '0 0 1rem 0' }}>European Summer Tour 2026</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.5rem', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                <span style={{ background: '#ddd', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem' }}>1</span>
                <span>Tomorrowland (Belgium)</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.5rem', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                <span style={{ background: '#ddd', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem' }}>2</span>
                <span>Carnival of Venice (Italy)</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.5rem', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                <span style={{ background: '#ddd', width: '24px', height: '24px', borderRadius: '50%', alignItems: 'center', justifyContent: 'center', fontSize: '0.7rem' }}>3</span>
                <span>Oktoberfest (Germany)</span>
              </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ color: '#888', fontSize: '0.8rem' }}>Collaborating with 3 friends</span>
              <a href="/my-page/itineraries/edit" style={{ color: '#ff4d4d', fontWeight: 'bold', textDecoration: 'none' }}>Edit Plan $\rightarrow$</a>
            </div>
          </div>
        </div>

        <div style={{ marginTop: '4rem', padding: '2rem', backgroundColor: '#fff', borderRadius: '20px', border: '1px dashed #ccc', textAlign: 'center' }}>
          <p style={{ color: '#888' }}>You can sync your itinerary directly to Google Calendar or Apple Calendar.</p>
          <button style={{ marginTop: '1rem', padding: '0.5rem 1rem', backgroundColor: '#1a1a1a', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Sync to Calendar
          </button>
        </div>
      </main>
    </div}
  );
};

export default ItinerariesPage;
