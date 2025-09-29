const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: "http://127.0.0.1:5000",
    APPURLREGEX: process.env['APPURLREGEX'] || "^.*$",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}

console.table(CONFIG)

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    headless: 'new',
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor'
    ],
    ipDataDir: '/home/bot/data/',
    ignoreHTTPSErrors: true
});

console.log("[*] Bot started...");


const visit = async (urlToVisit) => {
    const browser = await initBrowser;
    const context = await browser.createBrowserContext()
    try {
        const page = await context.newPage();

        await page.setCookie({
            name: "admin-key",
            httpOnly: false,
            value: process.env.ADMIN_KEY || "secret",
            url: CONFIG.APPURL,
            path: "/web",
            domain: new URL(CONFIG.APPURL).hostname
        })

        await page.setDefaultNavigationTimeout(5000);

        console.log(`[*] Bot visiting ${urlToVisit}`)
        await page.goto(urlToVisit, {
            waitUntil: 'networkidle2'
        });

        await new Promise(r => setTimeout(r, 1000));

        console.log("[*] Browser close...")
        await context.close()
        return true;
    } catch (e) {
        console.error('[-]', e);
        await context.close();
        return false;
    }
}

try {
    visit(process.argv[2])
        .then((res) => {
            if (res) {
                console.log("[*] Bot finished!");
                process.exit(0);
            }
        });
} catch (e) {
    console.error('[-]', e);
    process.exit(1);
}