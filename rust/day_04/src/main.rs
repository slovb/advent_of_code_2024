use std::collections::HashSet;
use std::fs;

struct Data {
    x_positions: HashSet<(i32, i32)>,
    m_positions: HashSet<(i32, i32)>,
    a_positions: HashSet<(i32, i32)>,
    s_positions: HashSet<(i32, i32)>,
}

fn process_input(input: String) -> Result<Data, String> {
    let mut data = Data {
        x_positions: HashSet::new(),
        m_positions: HashSet::new(),
        a_positions: HashSet::new(),
        s_positions: HashSet::new(),
    };
    let mut x = 0;
    let mut y = 0;
    for row in input.lines() {
        for c in row.chars() {
            match c {
                'X' => data.x_positions.insert((x, y)),
                'M' => data.m_positions.insert((x, y)),
                'A' => data.a_positions.insert((x, y)),
                'S' => data.s_positions.insert((x, y)),
                _ => return Err("BROKEN INPUT".to_string()),
            };
            x += 1;
        }
        x = 0;
        y += 1;
    }
    Ok(data)
}

fn part_1(input: String) -> Result<i32, String> {
    let data = process_input(input)?;
    fn test_offset(data: &Data, pos_x: (i32, i32), offset: (i32, i32)) -> bool {
        let mut pos = pos_x;
        pos = (pos.0 + offset.0, pos.1 + offset.1); // take a step
        if !data.m_positions.contains(&pos) {
            return false;
        }
        pos = (pos.0 + offset.0, pos.1 + offset.1); // take a step
        if !data.a_positions.contains(&pos) {
            return false;
        }
        pos = (pos.0 + offset.0, pos.1 + offset.1); // take a step
        if !data.s_positions.contains(&pos) {
            return false;
        }
        return true;
    }
    let offsets = [(1, 0), (1, 1), (0, 1), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)];
    let mut output = 0;
    for pos_x in data.x_positions.iter() {
        for offset in offsets {
            if test_offset(&data, *pos_x, offset) {
                output += 1;
            }
        }
    }
    Ok(output)
}

fn part_2(input: String) -> Result<i32, String> {
    let data = process_input(input)?;
    fn test_offset(data: &Data, pos_a: (i32, i32), offset: (i32, i32)) -> bool {
        let mut off = offset;
        let mut pos = (pos_a.0 + off.0, pos_a.1 + off.1);
        if !data.m_positions.contains(&pos) {
            return false;
        }
        off = (-off.1, off.0); // rotate 90
        pos = (pos_a.0 + off.0, pos_a.1 + off.1);
        if !data.m_positions.contains(&pos) {
            return false;
        }
        off = (-off.1, off.0); // rotate 90
        pos = (pos_a.0 + off.0, pos_a.1 + off.1);
        if !data.s_positions.contains(&pos) {
            return false;
        }
        off = (-off.1, off.0); // rotate 90
        pos = (pos_a.0 + off.0, pos_a.1 + off.1);
        if !data.s_positions.contains(&pos) {
            return false;
        }
        return true;
    }
    let offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1)];
    let mut output = 0;
    for pos_a in data.a_positions.iter() {
        for offset in offsets {
            if test_offset(&data, *pos_a, offset) {
                output += 1;
            }
        }
    }
    Ok(output)
}

fn main() {
    let test_cases_part_1 = [("test0.txt", 18)];
    let test_cases_part_2 = [("test0.txt", 9)];
    let input = fs::read_to_string("input.txt").expect("Should have been able to read input.txt");

    for case in test_cases_part_1 {
        let (file_name, target) = case;
        let test_input =
            fs::read_to_string(file_name).expect("Should have been able to read the file");

        match part_1(test_input) {
            Ok(result) => {
                println!("PART 1 ({file_name})   {result}");
                if result != target {
                    println!("TEST FAILED");
                    return;
                }
            }
            Err(err) => {
                println!("PART 1 ({file_name})   {err}");
                return;
            }
        };
    }

    match part_1(input.clone()) {
        Ok(result) => {
            println!("PART 1 (input.txt)   {result}");
        }
        Err(err) => {
            println!("PART 1 (input.txt)   {err}");
            return;
        }
    }

    for case in test_cases_part_2 {
        let (file_name, target) = case;
        let test_input =
            fs::read_to_string(file_name).expect("Should have been able to read the file");

        match part_2(test_input) {
            Ok(result) => {
                println!("PART 2 ({file_name})   {result}");
                if result != target {
                    println!("TEST FAILED");
                    return;
                }
            }
            Err(err) => {
                println!("PART 2 ({file_name})   {err}");
                return;
            }
        };
    }

    match part_2(input) {
        Ok(result) => {
            println!("PART 2 (input.txt)   {result}");
        }
        Err(err) => {
            println!("PART 2 (input.txt)   {err}");
            return;
        }
    }
}
