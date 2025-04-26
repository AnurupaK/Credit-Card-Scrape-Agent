from flask import Flask, render_template, jsonify, request, send_file
from modules.credit_card_links import ExtractLinks
from GeminiCreditCardAgent.crew import CardScrape
from modules.data_pre_process import card_pre_process, make_csv
import io

# Create Flask app with custom template and static folder paths
app = Flask(__name__, template_folder="../Frontend/templates", static_folder="../Frontend/static")

# Global state to keep track of scraping progress
SCRAPER_STATE = {
    'all_links': [],
    'start': 0,
    'stop': 0,
    'batch_size': 5,
    'url': '',
    'all_card_links': [],
    'all_card_info': [],
    'link_visit_status': True,
    'cards_formatted_output': []
}

# Home route - resets global state and renders frontend
@app.route('/')
def home():
    SCRAPER_STATE.update({
        'all_links': [],
        'start': 0,
        'stop': 0,
        'batch_size': 5,
        'url': '',
        'all_card_links': [],
        'all_card_info': [],
        'link_visit_status': True,
        'cards_formatted_output': []
    })
    return render_template('index.html')


# Route to start initial scraping based on input URL and batch size
@app.route('/api/start-scrape', methods=['POST'])
def start_scraping():
    try:
        data = request.get_json()
        url = data['url']
        batch_size = data['batch_size']

        if batch_size > 5:
            return jsonify({'success': False, 'message': 'Batch size too large. Maximum allowed is 5.'})

        # Extract links if not already done
        if SCRAPER_STATE['link_visit_status']:
            extractor = ExtractLinks(url=url)
            SCRAPER_STATE['all_links'] = extractor.do_extraction()
            SCRAPER_STATE['link_visit_status'] = False

        if not SCRAPER_STATE['all_links']:
            return jsonify({'msg': '❌ No links found.'}), 404

        # Update state for batch slicing
        SCRAPER_STATE['start'] = 0
        SCRAPER_STATE['stop'] = batch_size
        SCRAPER_STATE['batch_size'] = batch_size
        SCRAPER_STATE['url'] = url

        # Scrape card data for first batch
        scraper = CardScrape(
            all_links=SCRAPER_STATE['all_links'],
            start_batch_size=SCRAPER_STATE['start'],
            stop_batch_size=SCRAPER_STATE['stop']
        )
        card_data = scraper.execute()

        for url, card_info in card_data.items():
            SCRAPER_STATE['all_card_info'].append(card_info.raw)
            SCRAPER_STATE['all_card_links'].append(url)

        # Clean/process the scraped data
        card_details_list = card_pre_process(SCRAPER_STATE['all_card_info'])
        SCRAPER_STATE['cards_formatted_output'] = card_details_list

        return jsonify({'card_data': card_details_list, 'card_urls': SCRAPER_STATE['all_card_links']})
    except Exception as e:
        print(e)


# Route to load and scrape the next batch of card links
@app.route('/api/start-next-batch', methods=['GET'])
def start_next_batch_scraping():
    try:
        SCRAPER_STATE['all_card_info'] = []
        SCRAPER_STATE['all_card_links'] = []

        # Calculate next batch range
        all_links = SCRAPER_STATE['all_links']
        batch_size = SCRAPER_STATE['batch_size']
        start = SCRAPER_STATE['start'] + batch_size
        stop = SCRAPER_STATE['stop'] + batch_size

        if start >= len(all_links):
            return jsonify({'msg': '🚫 No more batches to run.'}), 200

        # Update batch positions
        SCRAPER_STATE['start'] = start
        SCRAPER_STATE['stop'] = stop

        # Scrape next batch
        scraper = CardScrape(
            all_links=all_links,
            start_batch_size=start,
            stop_batch_size=stop
        )
        card_data = scraper.execute()

        for url, card_info in card_data.items():
            SCRAPER_STATE['all_card_info'].append(card_info.raw)
            SCRAPER_STATE['all_card_links'].append(url)

        # Process new batch and append results
        card_details_list = card_pre_process(SCRAPER_STATE['all_card_info'])
        SCRAPER_STATE['cards_formatted_output'] += card_details_list

        return jsonify({'card_data': card_details_list, 'card_urls': SCRAPER_STATE['all_card_links']})
    except Exception as e:
        print(e)


# Route to generate and download CSV file from all collected card data
@app.route('/api/download-csv', methods=['GET'])
def create_csv():
    try:
        df = make_csv(SCRAPER_STATE['cards_formatted_output'])
        csv_stream = io.StringIO()
        df.to_csv(csv_stream, index=False)
        csv_stream.seek(0)

        bytes_stream = io.BytesIO(csv_stream.getvalue().encode('utf-8'))
        bytes_stream.seek(0)

        return send_file(
            bytes_stream,
            mimetype='text/csv',
            download_name='cards_data.csv',
            as_attachment=True
        )
    except Exception as e:
        print(f'Error downloading csv: {e}')
        return "Error creating CSV", 500


# Run Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
