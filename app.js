const app = {
    data: null,
    currentView: 'home',
    currentFestivalId: null,
    map: null,

    async init() {
        try {
            const response = await fetch('./festivals_master.json');
            if (!response.ok) throw new Error('Network response was not ok');
            const json = await response.json();
            
            // Robust parsing: Handle both Object and Array formats
            this.data = Array.isArray(json) ? json : (json.festivals || []);
            
            if (this.data.length === 0) {
                throw new Error('No festival data found in the master file.');
            }
            
            console.log('Data loaded successfully', this.data);
            this.navigate('home');
        } catch (e) {
            console.error('Failed to load festival data:', e);
            document.getElementById('app-viewport').innerHTML = `
                <div class="flex flex-col items-center justify-center h-screen text-red-500 font-medium p-4 text-center">
                    <span class="text-5xl mb-4">🚨</span>
                    <h2 class="text-2xl mb-2">Data Loading Error</h2>
                    <p class="text-slate-500 max-w-md">${e.message}<br>Please check if festivals_master.json is correctly deployed.</p>
                </div>
            `;
        }
    },

    navigate(view, id = null) {
        this.currentView = view;
        this.currentFestivalId = id;
        this.render();
        window.scrollTo(0, 0);
    },

    render() {
        const viewport = document.getElementById('app-viewport');
        switch(this.currentView) {
            case 'home': viewport.innerHTML = this.viewHome(); break;
            case 'explore': viewport.innerHTML = this.viewExplore(); this.initMap(); break;
            case 'detail': viewport.innerHTML = this.viewDetail(); break;
            case 'planner': viewport.innerHTML = this.viewPlanner(); break;
        }
    },

    viewHome() {
        const featured = this.data.slice(0, 6);
        return `
            <div class="animate-fade-in">
                <section class="relative py-20 lg:py-32 overflow-hidden bg-slate-900 text-white">
                    <div class="absolute inset-0 opacity-40">
                        <img src="https://images.unsplash.com/photo-1533174072545-7a46656a29d4?auto=format&fit=crop&w=1920&q=80" class="w-full h-full object-cover" />
                    </div>
                    <div class="relative max-w-7xl mx-auto px-4 text-center">
                        <h1 class="text-5xl lg:text-7xl font-bold mb-6 tracking-tight">Discover the World's <br><span class="text-indigo-400">Cultural Wonders</span></h1>
                        <p class="text-xl text-slate-300 mb-10 max-w-2xl mx-auto">The ultimate intelligence portal for global festivals. Planned with precision, designed for experience.</p>
                        <div class="flex flex-col sm:flex-row justify-center gap-4">
                            <button onclick="app.navigate('explore')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-full font-semibold transition-all shadow-lg shadow-indigo-500/30">Start Exploring Map</button>
                            <button onclick="app.navigate('planner')" class="bg-white/10 backdrop-blur hover:bg-white/20 text-white px-8 py-4 rounded-full font-semibold transition-all border border-white/20">My Travel Planner</button>
                        </div>
                    </div>
                </section>
                <section class="max-w-7xl mx-auto px-4 py-20">
                    <div class="flex justify-between items-end mb-12">
                        <div>
                            <h2 class="text-3xl font-bold text-slate-900 mb-2">Featured Festivals</h2>
                            <p class="text-slate-500">High-fidelity curated selection based on SDS v2.0</p>
                        </div>
                        <button onclick="app.navigate('explore')" class="text-indigo-600 font-semibold hover:text-indigo-800 transition-colors">View All →</button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        ${featured.map((f, idx) => this.cardTemplate(f, idx)).join('')}
                    </div>
                </section>
            </div>
        `;
    },

    viewExplore() {
        return `
            <div class="flex flex-col md:flex-row h-screen overflow-hidden">
                <div class="w-full md:w-96 bg-white border-r border-slate-200 flex flex-col z-20">
                    <div class="p-6 border-b border-slate-100">
                        <h3 class="text-xl font-bold mb-4">Explore World</h3>
                        <div class="relative">
                            <input type="text" id="fest-search" oninput="app.filterFestivals(this.value)" placeholder="Search festivals..." class="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition-all">
                            <span class="absolute left-3 top-2.5 text-slate-400">🔍</span>
                        </div>
                    </div>
                    <div id="fest-list" class="flex-1 overflow-y-auto p-4 space-y-4">
                        ${this.data.map((f, idx) => this.listTemplate(f, idx)).join('')}
                    </div>
                </div>
                <div class="flex-1 relative">
                    <div id="map"></div>
                </div>
            </div>
        `;
    },

    viewDetail() {
        const f = this.data[this.currentFestivalId];
        if (!f) return `<div class="p-20 text-center">Festival not found.</div>`;
        return `
            <div class="max-w-5xl mx-auto px-4 py-12 animate-fade-in">
                <button onclick="app.navigate('explore')" class="mb-8 flex items-center gap-2 text-slate-500 hover:text-indigo-600 transition-colors font-medium">← Back to Explore</button>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
                    <div class="lg:col-span-2 space-y-12">
                        <section>
                            <h1 class="text-4xl lg:text-6xl font-extrabold text-slate-900 mb-4">${f.identity.name_local || 'Unknown'}</h1>
                            <p class="text-2xl text-slate-500 font-light">${f.identity.name_en || 'No English Name'}</p>
                            <div class="mt-6 flex flex-wrap gap-3">
                                <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-semibold">${f.identity.category || 'Festival'}</span>
                                <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-sm font-medium">📍 ${f.identity.address || 'Location TBA'}</span>
                            </div>
                        </section>
                        <section class="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
                                <h3 class="text-lg font-bold mb-4 flex items-center gap-2">📅 Timing</h3>
                                <div class="space-y-3 text-slate-600">
                                    <div class="flex justify-between"><span>Period:</span> <span class="font-medium">${f.temporal.start_date} - ${f.temporal.end_date}</span></div>
                                    <div class="flex justify-between"><span>Frequency:</span> <span class="font-medium">${f.temporal.frequency}</span></div>
                                    <div class="flex justify-between"><span>Best Time:</span> <span class="font-medium">${f.temporal.best_time_to_visit}</span></div>
                                </div>
                            </div>
                            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
                                <h3 class="text-lg font-bold mb-4 flex items-center gap-2">🚚 Logistics</h3>
                                <div class="space-y-3 text-slate-600">
                                    <a href="${f.logistics.official_url}" target="_blank" class="block text-indigo-600 font-medium hover:underline truncate">🌐 Official Website</a>
                                    <div class="flex flex-col gap-1"><span class="text-xs text-slate-400 uppercase font-bold">Transport</span><span class="text-sm">${f.logistics.transport_tips}</span></div>
                                    <div class="flex flex-col gap-1"><span class="text-xs text-slate-400 uppercase font-bold">Stay</span><span class="text-sm">${f.logistics.accommodation_tips}</span></div>
                                </div>
                            </div>
                        </section>
                        <section>
                            <h3 class="text-2xl font-bold mb-6">Experience Deep Dive</h3>
                            <div class="prose prose-slate max-w-none text-slate-600 leading-relaxed text-lg">${f.experience.deep_description}</div>
                            <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="p-6 rounded-2xl bg-amber-50 border border-amber-100">
                                    <h4 class="text-amber-800 font-bold mb-3">✨ Highlights</h4>
                                    <ul class="list-disc list-inside space-y-2 text-amber-700">${f.experience.highlights.split(',').map(h => `<li>${h}</li>`).join('')}</ul>
                                </div>
                                <div class="p-6 rounded-2xl bg-blue-50 border border-blue-100">
                                    <h4 class="text-blue-800 font-bold mb-3">💡 Local Tips</h4>
                                    <p class="text-blue-700">${f.experience.local_insider_tips}</p>
                                </div>
                            </div>
                        </section>
                    </div>
                    <div class="space-y-6">
                        <div class="p-6 rounded-2xl bg-slate-900 text-white">
                            <h3 class="text-lg font-bold mb-4">Verification</h3>
                            <div class="space-y-4 text-sm text-slate-400">
                                <div class="flex justify-between"><span>Last Update:</span> <span class="text-white">${f.verification.last_updated}</span></div>
                                <div class="flex justify-between"><span>Source:</span> <a href="${f.verification.source_url}" class="text-indigo-400 hover:underline truncate ml-4" target="_blank">View Source →</a></div>
                            </div>
                        </div>
                        <button onclick="app.addToPlanner(${this.currentFestivalId})" class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl font-bold transition-all shadow-lg shadow-indigo-500/30">Add to My Planner</button>
                    </div>
                </div>
            </div>
        `;
    },

    viewPlanner() {
        return `<div class="max-w-4xl mx-auto px-4 py-20 text-center"><div class="mb-8 text-6xl">🗺️</div><h1 class="text-4xl font-bold mb-4">My Travel Planner</h1><p class="text-slate-500 mb-12">Your curated festival itinerary will appear here.</p><button onclick="app.navigate('explore')" class="bg-indigo-600 text-white px-8 py-3 rounded-full font-semibold">Go to Map</button></div>`;
    },

    cardTemplate(f, idx) {
        return `
            <div class="festival-card bg-white rounded-3xl border border-slate-200 overflow-hidden cursor-pointer transition-transform hover:scale-[1.02]" onclick="app.navigate('detail', ${idx})">
                <div class="h-48 bg-slate-200 relative overflow-hidden">
                    <div class="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent"></div>
                    <div class="absolute bottom-4 left-4 text-white font-bold text-lg">${f.identity.name_local}</div>
                    <div class="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold text-indigo-600 shadow-sm">${f.identity.category}</div>
                </div>
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2 text-slate-900 truncate">${f.identity.name_local}</h3>
                    <p class="text-slate-500 text-sm mb-4 line-clamp-2">${f.experience.deep_description}</p>
                    <div class="flex items-center justify-between text-xs font-medium">
                        <span class="text-slate-400">📍 ${f.identity.address}</span>
                        <span class="text-indigo-600 font-bold">Details →</span>
                    </div>
                </div>
            </div>
        `;
    },

    listTemplate(f, idx) {
        return `
            <div class="p-4 rounded-xl border border-slate-100 hover:border-indigo-300 hover:bg-indigo-50 cursor-pointer transition-all festival-card" onclick="app.navigate('detail', ${idx})">
                <h4 class="font-bold text-slate-800 truncate">${f.identity.name_local}</h4>
                <p class="text-xs text-slate-500 truncate">${f.identity.address}</p>
            </div>
        `;
    },

    initMap() {
        if (this.map) this.map.remove();
        this.map = L.map('map').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(this.map);
        this.data.forEach((f, idx) => {
            if (f.logistics && f.logistics.gps_coords) {
                const { lat, lon } = f.logistics.gps_coords;
                if (lat && lon) {
                    L.marker([lat, lon]).addTo(this.map).bindPopup(`<b>${f.identity.name_local}</b><br><button onclick="app.navigate('detail', ${idx})" class="text-indigo-600 font-bold text-xs">View Details</button>`);
                }
            }
        });
    },

    filterFestivals(query) {
        const q = query.toLowerCase();
        const filtered = this.data.filter(f => 
            (f.identity.name_local && f.identity.name_local.toLowerCase().includes(q)) || 
            (f.identity.name_en && f.identity.name_en.toLowerCase().includes(q)) ||
            (f.identity.address && f.identity.address.toLowerCase().includes(q))
        );
        document.getElementById('fest-list').innerHTML = filtered.map((f) => {
            const originalIdx = this.data.indexOf(f);
            return this.listTemplate(f, originalIdx);
        }).join('');
    },

    addToPlanner(id) { alert('Added to planner!'); }
};

window.onload = () => app.init();
