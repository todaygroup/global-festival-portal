import React, { useState, useEffect } from 'react';
import Navigation from '../components/Navigation';

const HomePage = () => {
  const [festivals, setFestivals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchFestivals();
  }, []);

  const fetchFestivals = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/festivals');
      const data = await response.json();
      setFestivals(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching festivals:', error);
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    // In a real app, this would trigger a new API call with search params
    const filtered = festivals.filter(f => 
      f.name_en.toLowerCase().includes(searchQuery.toLowerCase()) || 
      f.country_code.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFestivals(filtered);
  };

  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      
      <main style={{ padding: '3rem 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>Discover the World's Greatest Festivals</h1>
          <p style={{ fontSize: '1.2rem', color: '#666' }}>The most reliable, comprehensive, and AI-powered global festival portal.</p>
          
          <form onSubmit={handleSearch} style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem' }}>
             <input 
               type="text" 
               value={searchQuery}
               onChange={(e) => setSearchQuery(e.target.value)}
               placeholder="Search festivals by name, vibe, or country..." 
               style={{ padding: '1rem', width: '400px', borderRadius: '4px', border: '1px solid #ddd' }} 
             />
             <button type="submit" style={{ padding: '1rem 2rem', backgroundColor: '#ff4d4d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Search</button>
          </form>
        </header>

        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
          {loading ? (
            <p style={{ textAlign: 'center', gridColumn: '1 / -1' }}>Loading festivals...</p>
          ) : (
            festivals.map(f => (
              <div key={f.id} style={{ backgroundColor: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', borderLeft: '5px solid #ff4d4d' }}>
                <h3 style={{ margin: '0 0 0.5rem 0' }}>{f.name_en}</h3>
                <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '1rem' }}>{f.country_code} | {f.category || 'General'}</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ backgroundColor: '#eee', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem' }}>{f.vibe || 'Unknown'}</span>
                  <a href={`/festival/${f.id}`} style={{ color: '#ff4d4d', fontWeight: 'bold', textDecoration: 'none' }}>Details $\rightarrow$</a>
                </div>
              </div>
            ))
          )}
        </section>

        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2rem' }}>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #ddd' }}>
            <h3>Explore Map</h3>
            <p> styled a simple layout for an interactive map placeholder</p>
            <a href="/explore/map" style={{ color: '#ff4d4d', fontWeight: 'bold' }}>Enter Map $\rightarrow$</a>
          </div>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #ddd' }}>
            <h3>AI Radar</h3>
            <p>Find festivals tailored to your personal tastes.</p>
            <a href="/explore/radar" style={{ color: '#ff4d4d', fontWeight: 'bold' }}>Start Sync $\rightarrow$</p>
          </div>
          <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #django-dark' }}>
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
