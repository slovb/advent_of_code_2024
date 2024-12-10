use std::fs;
use std::str::FromStr;

fn parse_input<T: FromStr>(contents: String) -> Vec<Result<Vec<T>, T::Err>> {
    let mut output = Vec::new();
    for row in contents.lines() {
        let parts = row.split_whitespace().map(|word| word.parse()).collect();
        output.push(parts);
    }
    return output;
}

fn is_safe(row: Vec<i32>) -> bool {
    let mut values = row.iter();
    let mut last_diff = 0;
    let mut prev = values.next().unwrap();
    for val in values {
        let diff = prev - val;
        if diff == 0 || diff.abs() > 3 {
            return false;
        }
        if diff * last_diff < 0 {
            return false;  
        }
        last_diff = diff;
        prev = val;
    }
    return true;
}

fn solve(rows: Vec<Result<Vec<i32>, <i32 as FromStr>::Err>>) -> i32 {
    let mut output = 0;
    for row in rows {
        if is_safe(row.unwrap()) {
            output += 1;
        }
    }
    return output;
}

fn main() {
    let file_name = "input.txt";
    // let file_name = "test.txt";
    let contents = fs::read_to_string(file_name).expect("Should have been able to read the file");
    let rows = parse_input::<i32>(contents);
    let answer = solve(rows);
    println!("{answer}");
}