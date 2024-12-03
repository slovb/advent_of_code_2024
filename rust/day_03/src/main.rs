use std::fs;
use regex::Regex;

fn sum_products(text:String) -> i32 {
    let mut output = 0;
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let mut results: Vec<(i32, i32)> = vec![];
    for (_, [x, y]) in re.captures_iter(text.as_str()).map(|c| c.extract()) {
        results.push((x.parse::<i32>().unwrap(), y.parse::<i32>().unwrap()))
    }
    for res in results {
        let (l, r) = res;
        output += l * r;
    }
    return output;
}

fn grab_active(text:String) -> Vec<String> {
    let mut output: Vec<String> = Vec::new();
    let re = Regex::new(r"(?:do\(\)|^)(?s)(.*?)(?:don't\(\)|$)").unwrap();
    for (_, [s]) in re.captures_iter(text.as_str()).map(|c| c.extract()) {
        output.push(s.to_owned());
    }
    return output;
}

fn main() {
    let file_name = "input.txt";
    // let file_name = "test.txt";
    // let file_name = "test2.txt";
    let contents = fs::read_to_string(file_name).expect("Should have been able to read the file");
    let answer = sum_products(contents.clone());
    println!("{answer}");

    let mut total = 0;
    let actives = grab_active(contents).into_iter();
    for active in actives {
        total += sum_products(active);
    }
    println!("{total}");
}
