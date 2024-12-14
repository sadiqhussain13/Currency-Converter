self.addEventListener('install', function(event) {
    console.log('Service Worker Installed.');
});

self.addEventListener('fetch', function(event) {
    console.log('Service Worker Fetch:', event.request.url);
});
