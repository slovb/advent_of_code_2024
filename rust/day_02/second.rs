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

fn is_safe<'a, I>(mut values: I) -> bool
where
    I: Iterator<Item = &'a i32>
{
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
        let r = row.unwrap();
        if is_safe(r.iter()) {
            output += 1;
        }
        else {
            for i in 0..r.len() {
                // try without the number at index i
                if is_safe(r.iter().enumerate().filter(|&(j, _)| j != i).map(|(_, e) | e)) {
                    output += 1;
                    break;
                }
            }
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