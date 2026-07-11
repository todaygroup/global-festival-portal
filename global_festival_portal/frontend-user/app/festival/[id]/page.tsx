import React, { useState, useEffect } from 'react';
import Navigation from '../../components/Navigation';

const FestivalDetail = ({ params }) => {
  const [festival, setFestival] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFestival = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/festivals/${params.id}`);
        const data = await response.json();
        setFestival(data);
      } catch (error) {
        console.error('Error fetching festival:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchFestival();
  }, [params.id]);

  if (loading) return <div style={{ textAlign: 'center', padding: '5rem' }}>Loading festival details...</div>;
  if (!festival) return <div style={{ textAlign: 'center', padding: '5rem' }}>Festival not found.</div>;

  return (
    <div style={{ fontFamily: 'sans-serif', backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Navigation />
      <main style={{ padding: '3rem 2rem', maxWidth: '1000px', margin: '0 auto' }}>
        <div style={{ backgroundColor: 'white', borderRadius: '20px', overflow: 'hidden', boxShadow: '0 10px 25px rgba(0,0,0,0.1)' }}>
          <div style={{ height: '300px', backgroundColor: '#ddd', position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem', color: '#888' }}>
            Festival Banner Image
            <div style={{ position: 'absolute', top: '20px', right: '20px', backgroundColor: '#ff4d4d', color: 'white', padding: '0.5rem 1rem', borderRadius: '20px', fontWeight: 'bold', fontSize: '0.9rem' }}>
              ✓ Verified
            </div>
          </div>
          
          <div style={{ padding: '3rem' }}>
            <h1 style={{ fontSize: '2.5rem', margin: '0 0 1rem 0' }}>{festival.name_en}</h1>
            <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '2rem' }}>
              {festival.city}, {festival.country_code} | {festival.category}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '3rem' }}>
              <div>
                <h2 style={{ borderBottom: '2px solid #ff4d4d', display: 'inline-block', marginBottom: '1rem' }}>About the Festival</h2>
                <p style={{ lineHeight: '1.6', color: '#444', marginBottom: '2rem' }}>
                  {festival.description || 'No detailed description available. This festival is one of the most anticipated events in the region, offering a unique cultural experience.'}
                </p>

                <h2 style={{ borderBottom: '2px solid #ff4d4d', display: 'inline-block', marginBottom: '1rem' }}>Logistics & Planner</h2>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
                  <div style={{ padding: '1rem', backgroundColor: '#f9f9f9', borderRadius: '8px', border: '1px solid #eee' }}>
                    <strong>Start Date:</strong> {festival.start_date}
                  </div>
                  <div style={{ padding: '1rem', backgroundColor: '#f9f9f9', borderRadius: '8px', border: '1px solid #eee' }}>
                    <strong>End Date:</strong> {festival.end_date}
                  </div>
                </div>
                <a href={festival.official_url} target="_blank" rel="noopener noreferrer" style={{ display: 'inline-block', padding: '1rem 2rem', backgroundColor: '#ff4d4d', color: 'white', textDecoration: 'none', borderRadius: '8px', fontWeight: 'bold' }}>
                  Visit Official Website
                </a>
              </div>

              <div style={{ backgroundColor: '#fefefe', padding: '1.5rem', borderRadius: '12px', border: '1px solid #eee' }}>
                <h3 style={{ marginTop: 0 }}>Quick Info</h3>
                <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.9rem', color: '#666', lineHeight: '2' }}>
                  <li><strong>Vibe:</strong> {festival.vibe || 'N/A'}</li>
                  <li><strong>Verification:</strong> {festival.verification_status}</li>
                  <li><strong>Category:</strong> {festival.category}</li>
                </ul>
                <button style={{ width: '100%', padding: '0.8rem', marginTop: '1rem', backgroundColor: '#1a1a1a', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
                  + Add to My List
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default FestivalDetail;
