use crate::transformers::{transform_line_by_line_skipping_codeblocks};

/**
 * Modify the headings offset of Markdown content.
 * 
 * Only works for number sign (``#``) headings syntax.
 *
 * This function is secure, so if you try to decrease the offset
 * of a heading to a negative value that exceeds the top level
 * heading, it will be set to the minimum valid possible to not
 * modify the hierarchy of section nodes.
 *
 * Args:
 *   text (str): Text to modify.
 *   offset (int): Relative offset for headings, can be a positive
 *     or a negative number.
 *
 * Returns:
 *   str: New modified content.
 **/
 pub fn modify_headings_offset(text: &str, offset: i8) -> String {
    if offset >= 0 {
        transform_line_by_line_skipping_codeblocks(
            text,
            &transform_positive_headings_offset_function_factory(
                offset.try_into().unwrap(),
            ),
        )
    } else {
        let usize_abs_offset = offset.abs().try_into().unwrap();
        transform_line_by_line_skipping_codeblocks(
            text,
            &transform_negative_headings_offset_function_factory(
                usize_abs_offset,
                parse_max_valid_negative_heading_offset(
                    text,
                    usize_abs_offset,
                ),
            ),
        )
    }
}

fn transform_positive_headings_offset_function_factory(
    offset: usize,
) -> impl Fn(String) -> String {
    move |line| {
        match line.starts_with("#") {
            true => {
                let mut new_line = "#".repeat(offset);
                new_line.push_str(&line);
                new_line
            },
            false => line.to_string(),
        }
    }
}

fn parse_heading_line_offset(line: &str) -> usize {
    let mut offset = 0;
    for c in line.chars() {
        if c != '#' {
            break
        }
        offset += 1;
    }
    offset
}

fn parse_max_valid_negative_heading_offset(
    text: &str,
    offset: usize,
) -> usize {
    let mut max_valid_offset = 5;
    for line in text.lines() {
        if !line.starts_with("#") {
            continue;
        }
        let current_line_offset = parse_heading_line_offset(line);

        if current_line_offset > offset {
            let relative_offset = current_line_offset - offset;
            if relative_offset > max_valid_offset {
                max_valid_offset = relative_offset;
            }
        } else {
            if current_line_offset > 0 && max_valid_offset > current_line_offset - 1 {
                max_valid_offset = current_line_offset - 1;
            }
        }
        if max_valid_offset == 0 {
            break;
        }
    }
    max_valid_offset
}

fn transform_negative_headings_offset_function_factory(
    offset: usize,
    max_valid_offset: usize,
) -> impl Fn(String) -> String {
    move |line| {
        if !line.starts_with("#") || max_valid_offset == 0 {
            return line;
        }

        let current_line_offset = parse_heading_line_offset(&line);
        let mut new_line: String;

        if offset > max_valid_offset {
            new_line = "#".repeat(current_line_offset - max_valid_offset)
        } else {
            new_line = "#".repeat(current_line_offset - offset);
        }
        new_line.push_str(line.trim_start_matches("#"));
        return new_line;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case(&"# A\n## B\n\n###C", 1, "## A\n### B\n\n####C")]
    #[case(&"# A\n## B\n\n###C", 0, "# A\n## B\n\n###C")]
    #[case(&"## A\n### B\n\n####C", -1, "# A\n## B\n\n###C")]
    #[case(&"### A\n#### B\n\n#####C", -2, "# A\n## B\n\n###C")]
    #[case(&"### A\n#### B\n\n#####C", -5, "# A\n## B\n\n###C")]
    #[case(&"### A\n# B\n\n##C", -2, "### A\n# B\n\n##C")]
    #[case(&"#### A\n## B\n\n###C", -2, "### A\n# B\n\n##C")]
    #[case(
        &"# A\n```\n## B\n```\n###C",
        1,
        "## A\n```\n## B\n```\n####C",
    )]
    #[case(
        &"# A\n~~~\n## B\n~~~\n###C",
        1,
        "## A\n~~~\n## B\n~~~\n####C",
    )]
    #[case(
        &"# A\n\n    ## B\n\n###C",
        1,
        "## A\n\n    ## B\n\n####C",
    )]
    fn modify_headings_offset_test(
        #[case] text: &str,
        #[case] offset: i8,
        #[case] expected: String,
    ) {
        assert_eq!(
            modify_headings_offset(
                text,
                offset,
            ),
            expected,
        );
    }
}

