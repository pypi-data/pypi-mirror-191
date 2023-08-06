/**
 * Return the minimum possible of characters not found in a row.
 * 
 * For example, given the string ``"c cc cccc"`` and the
 * character ``"c"``, returns the minimum number of characters in
 * a row that are not found, so ``3`` in this case.
 *
 * This function is useful in to compute the number of backticks
 * that must wrap markdown code spans. Given the code span
 * ``"code that contains 3 \`\`\` and 2 \`\` backticks"`` and
 * the character ``"`"``, this function returns  ``1``.
 *
 * Args:
 *     character (str): Character to search.
 *     text (str): Text inside which find the character repeated
 *       in a row.
 *
 * Returns:
 *     int: Minimum number possible of characters not found in a row.
 **/
pub fn n_backticks_to_wrap_codespan(
    character: char,
    text: &str,
) -> usize {
    let mut in_a_rows: Vec<usize> = vec![];
    let mut current_in_a_row = 0;

    for c in text.chars() {
        if c == character {
            current_in_a_row += 1;
        } else if current_in_a_row > 0 {
            if !in_a_rows.contains(&current_in_a_row) {
                in_a_rows.push(current_in_a_row)
            }
            current_in_a_row = 0;
        }
    }
    if current_in_a_row > 0 && !in_a_rows.contains(&current_in_a_row) {
        in_a_rows.push(current_in_a_row)
    }

    let mut result = 0;
    if in_a_rows.len() > 0 {
        let max = in_a_rows.iter().max().unwrap() + 2;
        for n in 1..max {
            if !in_a_rows.contains(&n) {
                result = n;
                break;
            }
        }
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case('c', &"c tt ccc cccc", 2)]
    #[case('c', &"c cc ttt cccc", 3)]
    #[case('c', &"t cc ttt cccc", 1)]
    #[case('c', &"c cc ccc tttt", 4)]
    fn n_backticks_to_wrap_codespan_test(
        #[case] character: char,
        #[case] text: &str,
        #[case] expected: usize,
    ) {
        assert_eq!(
            n_backticks_to_wrap_codespan(character, text),
            expected,
        );
    }
}
