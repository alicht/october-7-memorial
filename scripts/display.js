const Display = {
    currentIndex: 0,
    victims: [],

    async initialize() {
        console.log('DOM loaded, initializing display...');
        const profileEl = document.getElementById('profile');

        if (profileEl) {
            profileEl.style.display = 'block';
        }

        try {
            // Keep static content visible while fetching data
            console.log('Starting to fetch data...');
            this.victims = await Scraper.fetchVictimData();
            console.log('Fetched victims data:', this.victims);

            if (this.victims && this.victims.length > 0) {
                await this.displayVictim(0);
            }
        } catch (error) {
            console.error('Display initialization failed:', error);
            // Keep showing static content on error
        }
    },

    async displayVictim(index) {
        try {
            const victim = this.victims[index];
            console.log('Displaying victim:', victim);

            if (!victim) {
                console.log('No victim data available, keeping static content');
                return;
            }

            // Update text content
            const nameEl = document.getElementById('victimName');
            const ageEl = document.getElementById('victimAge');
            const headlineEl = document.getElementById('victimHeadline');
            const bioEl = document.getElementById('victimBio');
            const imgEl = document.getElementById('victimImage');

            if (nameEl) nameEl.textContent = victim.name || 'Unknown';
            if (ageEl) ageEl.textContent = victim.age ? `${victim.age} years old` : '';
            if (headlineEl) headlineEl.textContent = victim.headline || '';
            if (bioEl) bioEl.textContent = victim.bio || '';

            if (imgEl) {
                console.log('Setting image source to:', victim.image);
                imgEl.onerror = () => {
                    console.log('Primary image failed to load, using fallback:', victim.image_fallback);
                    imgEl.src = victim.image_fallback;
                };
                imgEl.src = victim.image;
                imgEl.alt = `Memorial photo of ${victim.name}`;
            }

        } catch (error) {
            console.error('Error displaying victim:', error);
            // Keep showing static content on error
        }
    },

    showNextVictim() {
        try {
            this.currentIndex = (this.currentIndex + 1) % this.victims.length;
            this.displayVictim(this.currentIndex);
        } catch (error) {
            console.error('Error showing next victim:', error);
        }
    }
};

// Initialize when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Display.initialize();
});

// Make Display available globally
window.Display = Display;