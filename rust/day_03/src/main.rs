use std::fs;
use regex::Regex;

fn solve(text:String) -> i32 {
    let mut output = 0;
    let re_mul = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let mut results: Vec<(i32, i32)> = vec![];
    for (_, [x, y]) in re_mul.captures_iter(text.as_str()).map(|c| c.extract()) {
        results.push((x.parse::<i32>().unwrap(), y.parse::<i32>().unwrap()))
    }
    for res in results {
        let (l, r) = res;
        output += l * r;
    }
    // for row in rows {
    //     let r = row.unwrap();
    //     if is_safe(r.iter()) {
    //         output += 1;
    //     }
    //     else {
    //         for i in 0..r.len() {
    //             // try without the number at index i
    //             if is_safe(r.iter().enumerate().filter(|&(j, _)| j != i).map(|(_, e) | e)) {
    //                 output += 1;
    //                 break;
    //             }
    //         }
    //     }
    // }
    return output;
}

fn main() {
    let file_name = "input.txt";
    // let file_name = "test.txt";
    let contents = fs::read_to_string(file_name).expect("Should have been able to read the file");
    let answer = solve(contents);
    println!("{answer}");
}
