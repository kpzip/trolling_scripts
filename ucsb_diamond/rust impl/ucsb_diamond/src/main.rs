use std::fs;
use reqwest::blocking::Client;
use reqwest::redirect::Policy;
use crate::config::Config;

mod config;

fn main() {
    println!("UCSB Diamond v{}", env!("CARGO_PKG_VERSION"));
    println!("Reading Config...");
    let cfg: Config = serde_json::from_str(fs::read_to_string("config.json").unwrap().as_str()).unwrap();
    println!("Connecting to UCSB Gold...");
    let client = Client::builder().redirect(Policy::limited(25)).build().unwrap();
    let login_page = client.get("https://my.sa.ucsb.edu/gold/StudentSchedule.aspx").header("Cookie", cfg.token()).send();
    println!("{}", login_page.unwrap().text().unwrap());
}
