use std::fs;

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
    let mut lefts = Vec::new();
    let mut rights = Vec::new();
    for row in rows {
        let (l, r) = row;
        lefts.push(l);
        rights.push(r);
    }
    lefts.sort();
    rights.sort();
    for (i, l) in lefts.iter().enumerate() {
        let r = rights[i];
        output += (l - r).abs();
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