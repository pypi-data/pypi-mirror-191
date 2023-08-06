pub fn transform_line_by_line_skipping_codeblocks(
    text: &str,
    func: &dyn Fn(String) -> String,
) -> String {
    let mut lines: Vec<String> = vec![];

    let mut current_fenced_codeblock_delimiter: String = "".to_string();
    for line in text.lines() {
        let mut next_line: String = line.to_string();
        if current_fenced_codeblock_delimiter == "" {
            let trimmed_line = line.trim();
            if trimmed_line.starts_with("```") || trimmed_line.starts_with("~~~") {
                // enter fenced codeblock
                current_fenced_codeblock_delimiter =
                    trimmed_line[0..3].to_string();
            } else if !line.starts_with("    ") || line.starts_with("     ") {
                // don't enter indented code block (4 spaces)
                // but yes in nested content (+4 spaces)
                //
                // perform the transformation
                next_line = func(next_line.to_string())
            }
        } else if line.trim_start().starts_with(
            &current_fenced_codeblock_delimiter
        ) {
            current_fenced_codeblock_delimiter = "".to_string();
        }
        lines.push(next_line);
    }
    lines.join("\n")
}


#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    fn prepend_upper_a_transformer(line: String) -> String {
        format!("A{}", line)
    }

    #[rstest]
    #[case(
        &"foo\nbar\n\nbaz",
        prepend_upper_a_transformer,
        "Afoo\nAbar\nA\nAbaz",
    )]
    #[case(
        &concat!(
            "foo\n```\nfoo\n```\n~~~\nfoo\n~~~\n\n    foo",
            "\n     foo\n\nbar\n\nbaz",
        ),
        prepend_upper_a_transformer,
        concat!(
            "Afoo\n```\nfoo\n```\n~~~\nfoo\n~~~\nA\n    foo",
            "\nA     foo\nA\nAbar\nA\nAbaz",
        ).to_string(),
    )]
    fn transform_line_by_line_skipping_codeblocks_test(
        #[case] text: &str,
        #[case] func: impl Fn(String) -> String,
        #[case] expected: String,
    ) {
        assert_eq!(
            transform_line_by_line_skipping_codeblocks(
                text,
                &func,
            ),
            expected,
        );
    }
}
