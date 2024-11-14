use std::fs;
use reqwest::blocking::Client;
use crate::config::Config;

mod config;

fn main() {
    println!("UCSB Diamond v{}", env!("CARGO_PKG_VERSION"));
    println!("Reading Config...");
    let cfg: Config = serde_json::from_str(fs::read_to_string("config.json").unwrap().as_str()).unwrap();
    println!("Connecting to UCSB Gold...");
    let client = Client::new();
    let login_page = client.get("https://sso.ucsb.edu/cas/login?service=https%3a%2f%2fmy.sa.ucsb.edu%2fgold%2fAlertMessage.aspx");


}
