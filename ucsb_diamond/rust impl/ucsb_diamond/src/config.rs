use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    token: String,
    username: String,
    password: String,
    classes: Vec<ClassInfo>
}

impl Config {
    pub fn username(&self) -> &str {
        &self.username
    }

    pub fn password(&self) -> &str {
        &self.password
    }

    pub fn token(&self) -> &str {
        &self.token
    }

    pub fn classes(&self) -> &Vec<ClassInfo> {
        &self.classes
    }
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ClassInfo {
    name: String,
    preferred_code: String,
    alt_codes: Vec<String>,
}

impl ClassInfo {
    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn preferred_code(&self) -> &str {
        &self.preferred_code
    }

    pub fn alt_codes(&self) -> &Vec<String> {
        &self.alt_codes
    }
}