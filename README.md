# Decentralized OSINT Aggregator

## Overview
This project is a **Decentralized OSINT Aggregator** designed to collect and process open-source intelligence (OSINT) data from multiple platforms. It leverages Python for data fetching, caching, and JSON file management, while Rust handles lightweight and efficient JSON processing.

## Project Structure
```
.
├── main.py                  # Python entry point for OSINT aggregation
├── rust_osint_processor.rs  # Rust file for JSON processing
├── config.json               # Configuration file for API endpoints, headers, and tokens
├── .env                      # Environment variables containing API tokens
├── processed_data.json       # Output file containing aggregated OSINT data
├── requirements.txt          # Python dependencies
├── Cargo.toml                 # Rust dependencies
├── README.md                 # Project documentation
```

## Features
- Multi-source OSINT data aggregation.
- Rate-limited, concurrent fetching with caching.
- Secure configuration management using environment variables.
- Rust-powered JSON processing for optimized performance.
- Error handling, logging, and data validation.

## Setup

### 1. Clone the repository:
```bash
$ git clone https://github.com/yourusername/osint-aggregator.git
$ cd osint-aggregator
```

### 2. Create and activate a virtual environment:
```bash
$ python -m venv venv
$ source venv/bin/activate   # On Linux/Mac
$ venv\Scripts\activate      # On Windows
```

### 3. Install dependencies:
```bash
$ pip install -r requirements.txt
```

### 4. Set up environment variables:
Create a `.env` file in the root directory and add your API tokens:
```
TWITTER_API_TOKEN=your_twitter_token
FACEBOOK_API_TOKEN=your_facebook_token
YOUTUBE_API_TOKEN=your_youtube_token
REDDIT_API_TOKEN=your_reddit_token
```

### 5. Configure your sources:
Edit `config.json` to specify your OSINT sources, headers, and endpoints.

```json
{
  "sources": [
    {
      "name": "Twitter",
      "endpoint": "https://api.twitter.com/2/tweets/search/recent",
      "headers": { "Authorization": "Bearer YOUR_API_TOKEN" },
      "params": { "query": "#cybersecurity", "max_results": 10 }
    },
    {
      "name": "Reddit",
      "endpoint": "https://www.reddit.com/r/netsec/new.json",
      "params": { "limit": 10 }
    }
  ],
  "rate_limit": 5,
  "cache_ttl": 300
}
```

### 6. Build and run the Rust processor:
```bash
$ cargo build --release
$ ./target/release/rust_osint_processor < processed_data.json
```

### 7. Run the Python OSINT Aggregator:
```bash
$ python main.py
```

## Error Handling
- **API errors:** Automatically logged with detailed error messages.
- **Caching:** Results cached to prevent redundant API calls.
- **Validation:** Input data validation prevents malformed requests.

## Testing
Run unit tests using:
```bash
$ python -m unittest discover tests/
```

## Contribution
Feel free to fork the repository and submit pull requests. Follow the coding standards outlined in the project and ensure your code is covered with unit tests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
🔥 Built with Python & Rust — because OSINT deserves speed and security! 🚀

