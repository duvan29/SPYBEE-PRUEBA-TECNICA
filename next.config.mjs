import jsonLoader from 'json-loader';

const nextConfig = {
    reactStrictMode: true,
    webpack: (config) => {
        config.module.rules.push({
            test: /\.json$/,
            type: 'javascript/auto',
            use: [jsonLoader],
        });
        return config;
    },
    images: {
        domains: ['www.spybee.com.co'],
    },
};



export default nextConfig;