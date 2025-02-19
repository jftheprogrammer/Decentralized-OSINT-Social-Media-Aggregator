use std::io::{self, Read};
use std::fs::File;
use std::path::Path;
use serde_json::{Value, json};
use std::error::Error;
use log::{error, info};
use simplelog::*;
use std::time::Instant;

fn main() -> Result<(), Box<dyn Error>> {
    // Initialize logging
    CombinedLogger::init(vec![
        TermLogger::new(LevelFilter::Info, Config::default(), TerminalMode::Mixed, ColorChoice::Auto),
        WriteLogger::new(LevelFilter::Error, Config::default(), File::create("errors.log")?)
    ])?;

    let start_time = Instant::now();

    // Read JSON from stdin
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).map_err(|e| {
        error!("Failed to read from stdin: {}", e);
        e
    })?;

    // Parse JSON
    let json_data: Value = serde_json::from_str(&buffer).map_err(|e| {
        error!("Failed to parse JSON: {}", e);
        e
    })?;

    // Example processing: count the number of sources
    let source_count = json_data.as_array().map(|arr| arr.len()).unwrap_or(0);

    // Create output JSON
    let output = json!({
        "source_count": source_count,
        "processed_data": json_data
    });

    // Print JSON to stdout
    println!("{}", serde_json::to_string_pretty(&output).expect("Failed to serialize JSON"));

    // Save to file with error handling
    if let Err(e) = save_to_file(&output, "processed_data.json") {
        error!("Error saving to file: {}", e);
    }

    info!("Processing completed in {:.2?}", start_time.elapsed());

    Ok(())
}

fn save_to_file(data: &Value, filename: &str) -> Result<(), Box<dyn Error>> {
    let path = Path::new(filename);
    let file = File::create(&path)?;
    serde_json::to_writer_pretty(file, data)?;
    Ok(())
}
