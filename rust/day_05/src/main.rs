use std::collections::HashMap;
use std::collections::hash_map::Entry::{Occupied, Vacant};
use std::fs;

struct Data {
    poset: HashMap<i32, Vec<i32>>,
    updates: Vec<Vec<i32>>,
}

fn process_input(input: String) -> Result<Data, String> {
    let mut data = Data {
        poset: HashMap::new(),
        updates: Vec::new(),
    };

    let mut reading_rules = true;
    for row in input.lines() {
        if row == "" {
            reading_rules = false;
            continue;
        }

        if reading_rules {
            let parts:Vec<i32> = row.split('|').map(|word| word.parse().unwrap()).collect();
            let left: i32 = *parts.get(0).unwrap();
            let right: i32 = *parts.get(1).unwrap();
            data.poset.entry(left).and_modify(|vec| vec.push(right)).or_insert(vec![right]);
        }
        else {
            let parts = row.split(',').map(|word| word.parse().unwrap()).collect();
            data.updates.push(parts);
        }
    }
    Ok(data)
}

fn is_good(update: Vec<i32>, poset: HashMap<i32, Vec<i32>>) -> Result<bool, String> {
    let mut added = HashMap::new();
    for (i, x) in update.iter().enumerate() {
        if poset.contains_key(x) {
            let vec = poset.get(x).unwrap();
            for y in vec {
                if added.contains_key(y) {
                    return Ok(false);
                }
            }
        }
        match added.entry(x) {
            Vacant(entry) => entry.insert(i),
            Occupied(_) => return Err("Doubly added key".to_string()),
        };
    }
    Ok(true)
}

fn part_1(input: String) -> Result<i32, String> {
    let data = process_input(input)?;

    let mut output = 0;
    for update in data.updates {
        if is_good(update.clone(), data.poset.clone())? {
            output += update[update.len() / 2];
        }
    }
    Ok(output)
}

fn sort(update: Vec<i32>, poset: HashMap<i32, Vec<i32>>) -> Result<Vec<i32>, String> {
    let mut added = HashMap::new();
    let mut state = Vec::from(update);
    let length = state.len();
    while added.len() < length {
        added.clear();

        for i in 0..length {
            let x = state[i];
            let mut not_good = false;
            if poset.contains_key(&x) {
                let vec = poset.get(&x).unwrap();
                for y in vec {
                    if added.contains_key(y) {
                        // move state[i] to before state[j] to make the poset condition true
                        let j = *added.get(y).unwrap();
                        let val = state.remove(i);
                        state.insert(j, val);
                        // break out and redo as this may make other conditions fail
                        not_good = true;
                        break;
                    }
                }
            }
            if not_good {
                break;
            }
            match added.entry(x) {
                Vacant(entry) => entry.insert(i),
                Occupied(_) => return Err("Doubly added key".to_string()),
            };
        }
    }
    Ok(state)
}

fn part_2(input: String) -> Result<i32, String> {
    let data = process_input(input)?;

    let mut output = 0;
    for update in data.updates {
        if !is_good(update.clone(), data.poset.clone())? {
            let sorted = sort(update, data.poset.clone())?;
            output += sorted[sorted.len() / 2];
        }
    }
    Ok(output)
}

fn main() {
    let test_cases_part_1 = [("test0.txt", 143)];
    let test_cases_part_2 = [("test0.txt", 123)];
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
