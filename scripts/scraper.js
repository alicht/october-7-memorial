const Scraper = {
    PROXY_URL: 'http://localhost:8000/scrape',
    PHOTOS_DIR: 'assets/photos/',

    async fetchVictimData() {
        try {
            console.log('Fetching victim data from:', this.PROXY_URL);
            const response = await fetch(this.PROXY_URL);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const victims = await response.json();
            console.log('Received victim data:', victims);

            if (!Array.isArray(victims) || victims.length === 0) {
                throw new Error('Invalid data format received');
            }

            return victims.map(victim => {
                console.log('Processing victim:', victim);
                // Use local photo path if available, otherwise use the fallback
                const localPhotoPath = victim.local_photo ? 
                    `${this.PHOTOS_DIR}${victim.local_photo}` : 
                    'assets/memorial-photo.svg';

                return {
                    name: String(victim.name || 'Unknown'),
                    age: victim.age ? parseInt(String(victim.age), 10) : 0,
                    headline: String(victim.headline || ''),
                    bio: String(victim.bio || ''),
                    image: localPhotoPath,
                    image_fallback: 'assets/memorial-photo.svg'
                };
            });
        } catch (error) {
            console.error('Error fetching victim data:', error);
            throw error;
        }
    }
};

// Make Scraper available globally
window.Scraper = Scraper;