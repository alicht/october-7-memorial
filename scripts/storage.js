const StorageManager = {
    CACHE_KEY: 'memorial_data',
    CACHE_TIMESTAMP_KEY: 'memorial_data_timestamp',
    CACHE_DURATION: 24 * 60 * 60 * 1000, // 24 hours

    async saveData(data) {
        const timestamp = Date.now();
        await chrome.storage.local.set({
            [this.CACHE_KEY]: data,
            [this.CACHE_TIMESTAMP_KEY]: timestamp
        });
    },

    async getData() {
        const result = await chrome.storage.local.get([
            this.CACHE_KEY,
            this.CACHE_TIMESTAMP_KEY
        ]);

        if (!result[this.CACHE_KEY] || !result[this.CACHE_TIMESTAMP_KEY]) {
            return null;
        }

        const timestamp = result[this.CACHE_TIMESTAMP_KEY];
        if (Date.now() - timestamp > this.CACHE_DURATION) {
            return null;
        }

        return result[this.CACHE_KEY];
    },

    async clearCache() {
        await chrome.storage.local.remove([
            this.CACHE_KEY,
            this.CACHE_TIMESTAMP_KEY
        ]);
    }
};
