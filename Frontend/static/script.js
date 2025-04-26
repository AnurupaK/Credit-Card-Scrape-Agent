document.addEventListener('DOMContentLoaded', function () {
    // Grab all important DOM elements
    const urlInput = document.querySelector('#url-box');
    const batchSizeInput = document.querySelector('#batch');
    const startBtn = document.querySelector('#start');
    const nextBtn = document.querySelector('#next');
    const csvBtn = document.querySelector('#csv');
    const card_info_screen = document.querySelector('.left-container');
    const waiting = document.querySelector('#waiting-area');

    let fetchInterval;

    // Starts a loading animation in the target element by cycling dots
    function startFetchingAnimation(targetElementId) {
        const el = document.getElementById(targetElementId);
        if (!el) return;

        let dotCount = 0;
        el.textContent = "🕐 Fetching";
        fetchInterval = setInterval(() => {
            dotCount = (dotCount + 1) % 4;
            el.textContent = "🕐 Fetching" + ".".repeat(dotCount);
        }, 500);
    }

    // Stops the loading animation and sets custom status text
    function stopFetchingAnimation(targetElementId, text = "✅ Fetched") {
        const el = document.getElementById(targetElementId);
        if (!el) return;

        clearInterval(fetchInterval);
        el.textContent = text;
    }

    // Disable a button visually and functionally
    function disableButton(btn) {
        btn.disabled = true;
        btn.style.cursor = "not-allowed";
        btn.style.opacity = "0.4";
        btn.style.transform = "none";
    }

    // Enable a button visually and functionally
    function enableButton(btn) {
        btn.disabled = false;
        btn.style.cursor = "pointer";
        btn.style.opacity = "1";
        btn.style.transform = "";
    }

    // Disable navigation buttons initially
    disableButton(nextBtn);
    disableButton(csvBtn);

    // Handle CSV export button click
    csvBtn.addEventListener('click', async function () {
        await download_data();
    });

    // Handle "Next Batch" scraping logic
    nextBtn.addEventListener('click', async function () {
        alert("✅ Next Batch Scraping started...");
        startFetchingAnimation('waiting-area');

        const result = await startNextBatch();
        if (!result) return;

        const { card_data_next, card_urls_next } = result;

        stopFetchingAnimation('waiting-area');

        card_data_next.forEach((element, index) => {
            const urlDiv = createUrlBlock(card_urls_next[index]);
            card_info_screen.appendChild(urlDiv);

            const cardContainer = document.createElement('div');
            cardContainer.classList.add('card-data');
            card_info_screen.appendChild(cardContainer);

            const cardTitle = document.createElement('h3');
            cardTitle.classList.add('card-title');
            cardTitle.innerHTML = `${element["Card Name"]}`;
            cardContainer.appendChild(cardTitle);

            exploreObjectAndCreateHTML(element, cardContainer);
        });
    });

    // Handle "Start" scraping logic
    startBtn.addEventListener('click', async function () {
        const url = urlInput.value.trim();
        const batchSize = parseInt(batchSizeInput.value.trim());
    
        // Validation
        if (!url || isNaN(batchSize) || batchSize <= 0) {
            alert("Please provide a valid URL and positive batch size.");
            return;
        }
    
        alert("✅ Scraping started...");
        startFetchingAnimation('waiting-area');
        disableButton(batchSizeInput);
    
        const result = await sendScrapeRequest(url, batchSize);
    
        if (!result) {
            enableButton(batchSizeInput);
            stopFetchingAnimation('waiting-area', '👋 Hello');
            return;
        }
    
        stopFetchingAnimation('waiting-area', '✅ Fetched');
    
        const { card_data, card_urls, total_links } = result;
        waiting.textContent = '🔗 Links: ' + total_links
        card_info_screen.innerHTML = '';
    
        card_data.forEach((element, index) => {
            const urlDiv = createUrlBlock(card_urls[index]);
            card_info_screen.appendChild(urlDiv);

            const cardContainer = document.createElement('div');
            cardContainer.classList.add('card-data');
            card_info_screen.appendChild(cardContainer);

            const cardTitle = document.createElement('h3');
            cardTitle.classList.add('card-title');
            cardTitle.innerHTML = `${element["Card Name"]}`;
            cardContainer.appendChild(cardTitle);

            exploreObjectAndCreateHTML(element, cardContainer);
        });
    
        enableButton(nextBtn);
        enableButton(csvBtn);
    });

    // Sends a POST request to start initial scraping
    async function sendScrapeRequest(url, batchSize) {
        const payload = { url, batch_size: batchSize };

        try {
            const response = await fetch('/api/start-scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok || data.success === false) {
                alert(`❌ ${data.message || 'Scraping failed.'}`);
                stopFetchingAnimation('waiting-area', '❌ Failed');
                return null;
            }

            alert("✅ Scraping done successfully!");
            return { card_data: data.card_data, card_urls: data.card_urls , total_links: data.total_links};
        } catch (error) {
            console.error("❌ Error during scraping:", error);
            alert("❌ Failed to start scraping.");
            stopFetchingAnimation('waiting-area', '❌ Failed');
            return null;
        }
    }

    // Fetches the next batch of results from the backend
    async function startNextBatch() {
        try {
            const response = await fetch('/api/start-next-batch', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (data.msg && data.msg.includes("No more batches")) {
                alert("🚫 All links have been scraped.");
                stopFetchingAnimation('waiting-area', '✅ All done');
                disableButton(nextBtn);
                return null;
            }

            alert("✅ Next batch scraping done.");
            return { card_data_next: data.card_data, card_urls_next: data.card_urls };
        } catch (error) {
            console.error("❌ Error during next batch scrape:", error);
            alert("❌ Failed to start next batch scraping.");
            stopFetchingAnimation('waiting-area', '❌ Failed');
            return null;
        }
    }

    // Creates a clickable link block for a URL
    function createUrlBlock(url) {
        const urlDiv = document.createElement('div');
        urlDiv.classList.add('url-catch');

        const link = document.createElement('a');
        link.href = url;
        link.target = "_blank";

        const emoji = document.createElement('span');
        emoji.textContent = '🔗';
        emoji.style.fontSize = '30px';
        emoji.style.marginRight = '8px';

        const linkText = document.createTextNode(url);

        link.appendChild(emoji);
        link.appendChild(linkText);
        urlDiv.appendChild(link);

        return urlDiv;
    }

    // Handles downloading of scraped data as CSV
    async function download_data() {
        try {
            const response = await fetch('/api/download-csv');

            if (!response.ok) throw new Error('CSV download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = 'cards_data.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('❌ Error downloading CSV:', error);
        }
    }

    // Recursively parses an object and appends its contents to the HTML
    function exploreObjectAndCreateHTML(obj, parentElement) {
        for (let key in obj) {
            const value = obj[key];

            const mainKey = document.createElement('div');
            mainKey.classList.add('main-key');
            mainKey.innerHTML = `<strong>${key}:</strong>`;
            parentElement.appendChild(mainKey);

            if (typeof value === 'object' && value !== null) {
                const section = document.createElement('div');
                section.classList.add('nested-section');
                parentElement.appendChild(section);

                if (Array.isArray(value)) {
                    value.forEach((item, idx) => {
                        const p = document.createElement('p');
                        p.innerHTML = `${idx + 1}: ${item}`;
                        section.appendChild(p);
                    });
                } else {
                    exploreObjectAndCreateHTML(value, section);
                }
            } else {
                const p = document.createElement('p');
                p.classList.add('value');
                p.innerHTML = `${value}`;
                parentElement.appendChild(p);
            }

            const space = document.createElement('div');
            space.classList.add('space');
            parentElement.appendChild(space);
        }
    }
});
