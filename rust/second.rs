use std::fs;
use std::collections::HashMap;

fn parse_input(contents: String) -> Vec<(i32, i32)> {
    let mut output = Vec::new();
    for row in contents.lines() {
        let mut parts = row.split_whitespace();
        let left = parts.next().unwrap().parse::<i32>().unwrap();
        let right = parts.next().unwrap().parse::<i32>().unwrap();
        output.push((left, right));
    }
    return output;
}

fn solve(rows: Vec<(i32, i32)>) -> i32 {
    let mut output = 0;
    let mut map = HashMap::new();
    for row in rows.iter() {
        let (_l, r) = row;
        let value = map.entry(r).or_insert(0);
        *value += 1;
    }
    for row in rows.iter() {
        let (l, _r) = row;
        if map.contains_key(&l) {
            output += l * map.get(&l).unwrap();
        }
    }
    return output;
}

fn main() {
    let file_name = "input.txt";
    // let file_name = "test.txt";
    let contents = fs::read_to_string(file_name).expect("Should have been able to read the file");
    let rows = parse_input(contents);
    let answer = solve(rows);
    println!("{answer}");
}