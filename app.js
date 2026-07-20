const app = {
    data: null,
    currentView: 'home',
    currentFestivalId: null,
    map: null,

    async init() {
        try {
            const response = await fetch('./festivals_master.json');
            const json = await response.json();
            this.data = json.festivals;
            console.log('Data loaded successfully', this.data);
            this.navigate('home');
        } catch (e) {
            console.error('Failed to load festival data:', e);
            document.getElementById('app-viewport').innerHTML = `
                <div class="flex items-center justify-center h-screen text-red-500 font-medium">
                    Error loading data. Please ensure the JSON file is present and served via a web server.
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
            case 'home':
                viewport.innerHTML = this.viewHome();
                break;
            case 'explore':
                viewport.innerHTML = this.viewExplore();
                this.initMap();
                break;
            case 'detail':
                viewport.innerHTML = this.viewDetail();
                break;
            case 'planner':
                viewport.innerHTML = this.viewPlanner();
                break;
        }
    },

    // --- VIEWS ---

    viewHome() {
        const featured = this.data.slice(0, 6);
        return `
            <div class="animate-fade-in">
                <!-- Hero Section -->
                <section class="relative py-20 lg:py-32 overflow-hidden bg-slate-900 text-white">
                    <div class="absolute inset-0 opacity-40">
                        <img src="https://images.unsplash.com/photo-1533174072545-7a46656a29d4?auto=format&fit=crop&w=1920&q=80" class="w-full h-full object-cover" />
                    </div>
                    <div class="relative max-w-7xl mx-auto px-4 text-center">
                        <h1 class="text-5xl lg:text-7xl font-bold mb-6 tracking-tight">Discover the World's <br><span class="text-indigo-400">Cultural Wonders</span></h1>
                        <p class="text-xl text-slate-300 mb-10 max-w-2xl mx-auto">The ultimate intelligence portal for global festivals. From hidden gems to world-famous celebrations, planned with precision.</p>
                        <div class="flex flex-col sm:flex-row justify-center gap-4">
                            <button onclick="app.navigate('explore')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-full font-semibold transition-all shadow-lg shadow-indigo-500/30">Start Exploring Map</button>
                            <button onclick="app.navigate('planner')" class="bg-white/10 backdrop-blur hover:bg-white/20 text-white px-8 py-4 rounded-full font-semibold transition-all border border-white/20">My Travel Planner</button>
                        </div>
                    </div>
                </section>

                <!-- Trending Festivals -->
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
                <!-- Sidebar -->
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
                <!-- Map -->
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
                <button onclick="app.navigate('explore')" class="mb-8 flex items-center gap-2 text-slate-500 hover:text-indigo-600 transition-colors font-medium">
                    ← Back to Explore
                </button>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
                    <!-- Left Column: Core Info -->
                    <div class="lg:col-span-2 space-y-12">
                        <section>
                            <h1 class="text-4xl lg:text-6xl font-extrabold text-slate-900 mb-4">${f.identity.name_local || 'Unknown Festival'}</h1>
                            <p class="text-2xl text-slate-500 font-light">${f.identity.name_en || 'No English Name'}</p>
                            <div class="mt-6 flex flex-wrap gap-3">
                                <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm font-semibold">${f.identity.category || 'Festival'}</span>
                                ${f.identity.address ? `<span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-sm font-medium">📍 ${f.identity.address}</span>` : ''}
                            </div>
                        </section>

                        <section class="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
                                <h3 class="text-lg font-bold mb-4 flex items-center gap-2">📅 Temporal Intelligence</h3>
                                <div class="space-y-3 text-slate-600">
                                    <div class="flex justify-between"><span>Start Date:</span> <span class="font-medium">${f.temporal.start_date || 'TBA'}</span></div>
                                    <div class="flex justify-between"><span>End Date:</span> <span class="font-medium">${f.temporal.end_date || 'TBA'}</span></div>
                                    <div class="flex justify-between"><span>Frequency:</span> <span class="font-medium">${f.temporal.frequency || 'Unknown'}</span></div>
                                </div>
                                ${f.temporal.detailed_schedule ? `<div class="mt-4 p-3 bg-slate-50 rounded text-sm">${f.temporal.detailed_schedule}</div>` : ''}
                            </div>
                            <div class="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
                                <h3 class="text-lg font-bold mb-4 flex items-center gap-2">🚚 Logistics</h3>
                                <div class="space-y-3 text-slate-600">
                                    <a href="${f.logistics.official_url || '#'}" target="_blank" class="block text-indigo-600 font-medium hover:underline truncate">🌐 Official Website</a>
                                    <div class="flex flex-col gap-1">
                                        <span class="text-xs text-slate-400 uppercase font-bold">Transport</span>
                                        <span class="text-sm">${f.logistics.transport || 'No transport info available.'}</span>
                                    </div>
                                    <div class="flex flex-col gap-1">
                                        <span class="text-xs text-slate-400 uppercase font-bold">Accommodation</span>
                                        <span class="text-sm">${f.logistics.accommodation_tips || 'No accommodation tips.'}</span>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section>
                            <h3 class="text-2xl font-bold mb-6">Experience Deep Dive</h3>
                            <div class="prose prose-slate max-w-none text-slate-600 leading-relaxed text-lg">
                                ${f.experience.deep_description || 'Detailed description coming soon.'}
                            </div>
                            <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="p-6 rounded-2xl bg-amber-50 border border-amber-100">
                                    <h4 class="text-amber-800 font-bold mb-3 flex items-center gap-2">✨ Highlights</h4>
                                    <ul class="list-disc list-inside space-y-2 text-amber-700">
                                        ${f.experience.highlights.length ? f.experience.highlights.map(h => `<li>${h}</li>`).join('') : '<li>No highlights listed.</li>'}
                                    </ul>
                                </div>
                                <div class="p-6 rounded-2xl bg-blue-50 border border-blue-100">
                                    <h4 class="text-blue-800 font-bold mb-3 flex items-center gap-2">💡 Local Tips</h4>
                                    <ul class="list-disc list-inside space-y-2 text-blue-700">
                                        ${f.experience.local_tips.length ? f.experience.local_tips.map(t => `<li>${t}</li>`).join('') : '<li>No local tips available.</li>'}
                                    </ul>
                                </div>
                            </div>
                        </section>

                        <section>
                            <h3 class="text-2xl font-bold mb-6">Multimedia Assets</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                ${f.multimedia.official_images.length ? f.multimedia.official_images.map(img => `<img src="${img}" class="rounded-xl w-full object-cover h-64 bg-slate-200" />`).join('') : '<div class="h-64 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 italic">No images available</div>'}
                                ${f.multimedia.official_videos.length ? f.multimedia.official_videos.map(vid => `<div class="h-64 bg-slate-800 rounded-xl flex items-center justify-center text-white">Video: ${vid}</div>`).join('') : ''}
                            </div>
                        </section>
                    </div>

                    <!-- Right Column: Metadata -->
                    <div class="space-y-6">
                        <div class="p-6 rounded-2xl bg-slate-900 text-white">
                            <h3 class="text-lg font-bold mb-4">Verification Status</h3>
                            <div class="space-y-4 text-sm text-slate-400">
                                <div class="flex justify-between"><span>Last Update:</span> <span class="text-white">${f.verification.update_date}</span></div>
                                <div class="flex justify-between"><span>Source:</span> <a href="${f.verification.source_url || '#'}" class="text-indigo-400 hover:underline truncate ml-4" target="_blank">${f.verification.source_url || 'Not provided'}</a></div>
                                <div class="pt-4 mt-4 border-t border-slate-700">
                                    <p class="text-xs">Data verified against SDS v2.0 architectural standards.</p>
                                </div>
                            </div>
                        </div>
                        <button onclick="app.addToPlanner(${this.currentFestivalId})" class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl font-bold transition-all shadow-lg shadow-indigo-500/30">Add to My Planner</button>
                    </div>
                </div>
            </div>
        `;
    },

    viewPlanner() {
        return `
            <div class="max-w-4xl mx-auto px-4 py-20 text-center">
                <div class="mb-8 text-6xl">🗺️</div>
                <h1 class="text-4xl font-bold mb-4">My Travel Planner</h1>
                <p class="text-slate-500 mb-12">Your curated festival itinerary will appear here. Start exploring the map to add festivals to your route.</p>
                <button onclick="app.navigate('explore')" class="bg-indigo-600 text-white px-8 py-3 rounded-full font-semibold">Go to Map</button>
            </div>
        `;
    },

    // --- HELPERS ---

    cardTemplate(f, idx) {
        return `
            <div class="festival-card bg-white rounded-3xl border border-slate-200 overflow-hidden cursor-pointer" onclick="app.navigate('detail', ${idx})">
                <div class="h-48 bg-slate-200 relative overflow-hidden">
                    <img src="https://images.unsplash.com/photo-1514525253361-597763938923?auto=format&fit=crop&w=600&q=80" class="w-full h-full object-cover opacity-80" />
                    <div class="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold text-indigo-600 shadow-sm">${f.identity.category || 'Festival'}</div>
                </div>
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2 text-slate-900 truncate">${f.identity.name_local || 'Unknown Festival'}</h3>
                    <p class="text-slate-500 text-sm mb-4 line-clamp-2">${f.experience.deep_description || 'No description available for this event.'}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-medium text-slate-400">📍 ${f.identity.address || 'Location TBA'}</span>
                        <span class="text-indigo-600 text-sm font-bold">Details →</span>
                    </div>
                </div>
            </div>
        `;
    },

    listTemplate(f, idx) {
        return `
            <div class="p-4 rounded-xl border border-slate-100 hover:border-indigo-300 hover:bg-indigo-50 cursor-pointer transition-all festival-card" onclick="app.navigate('detail', ${idx})">
                <h4 class="font-bold text-slate-800 truncate">${f.identity.name_local || 'Unknown Festival'}</h4>
                <p class="text-xs text-slate-500 truncate">${f.identity.address || 'Global'}</p>
            </div>
        `;
    },

    initMap() {
        if (this.map) {
            this.map.remove();
        }

        this.map = L.map('map').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        this.data.forEach((f, idx) => {
            if (f.identity.coordinates && f.identity.coordinates.latitude && f.identity.coordinates.longitude) {
                const marker = L.marker([f.identity.coordinates.latitude, f.identity.coordinates.longitude]).addTo(this.map);
                marker.bindPopup(`<b>${f.identity.name_local || 'Unknown'}</b><br><button onclick="app.navigate('detail', ${idx})" class="text-indigo-600 font-bold text-xs">View Details</button>`);
            }
        });
    },

    filterFestivals(query) {
        const q = query.toLowerCase();
        const listContainer = document.getElementById('fest-list');
        const filtered = this.data.filter(f => 
            (f.identity.name_local && f.identity.name_local.toLowerCase().includes(q)) || 
            (f.identity.name_en && f.identity.name_en.toLowerCase().includes(q)) ||
            (f.identity.address && f.identity.address.toLowerCase().includes(q))
        );
        
        listContainer.innerHTML = filtered.map((f, idx) => {
            // We need the original index for the detail view
            const originalIdx = this.data.indexOf(f);
            return this.listTemplate(f, originalIdx);
        }).join('');
    },

    addToPlanner(id) {
        alert('Added to planner! (MVP functionality: this would save to localStorage or DB)');
    }
};

window.onload = () => app.init();
