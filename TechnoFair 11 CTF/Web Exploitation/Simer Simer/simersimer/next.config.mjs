/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: '/api/chat',
                destination: 'http://0.0.0.0:1204/api.php' // Proxy to API endpoint
            }
        ];
    }
};

export default nextConfig;
