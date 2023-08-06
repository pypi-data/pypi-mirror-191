use crate::parsers::{MarkdownLineByLineSkippingCodeblocksParser};

pub struct MarkdownLinkReferencesParser<'a> {
    lines_iterator: MarkdownLineByLineSkippingCodeblocksParser<'a>,
}

impl MarkdownLinkReferencesParser<'_> {
    pub fn new(text: &str) -> MarkdownLinkReferencesParser {
        MarkdownLinkReferencesParser {
            lines_iterator: MarkdownLineByLineSkippingCodeblocksParser::new(text),
        }
    }
}

impl Iterator for MarkdownLinkReferencesParser<'_> {
    type Item = Vec<String>;

    fn next(&mut self) -> Option<Vec<String>> {
        let line = self.lines_iterator.next();
        match line {
            Some(line) => {
                if line.chars().next().unwrap_or('\0') == '[' {
                    return Some(parse_line_link_references(&line));
                } else {
                    return self.next();
                }
            },
            None => return None,
        }
    }
}

fn parse_line_link_references(line: &str) -> Vec<String> {
    let mut id: String = "".to_string();
    let mut link: String = "".to_string();
    let mut title: String = "".to_string();

    /*
     * States representing the context while parsing
     */
    let mut state: u8 = 1;
    let inside_id = 1;
    let after_id = 2;
    let inside_link = 4;
    let after_link = 8;
    //let inside_title = 16;

    // Escaping identifier closer
    let mut escaping_id_closer = false;

    // First index of link and title in line
    let mut link_first_index: usize = 0;
    let mut title_first_index: usize = 0;

    let mut ic: usize = 0;
    for c in line.chars() {
        if state == inside_id {
            if escaping_id_closer {
                if c != ']' {
                    escaping_id_closer = false;
                }
            } else if c == '\\' {
                escaping_id_closer = true;
            }
            if !escaping_id_closer && c == ']' {
                id = line[1..ic].to_string();
                state = state << 1;
            }
        } else if state == after_id {
            if c == '<' {
                state = state << 1;
                link_first_index = ic + 1;
            } else if c != ' ' && c != ':' {
                state = state << 1;
                link_first_index = ic;
            }
        } else if state == inside_link {
            if c == '>' || c == ' ' {
                link = line[link_first_index..ic].to_string();
                state = state << 1;
            }
        } else if state == after_link {
            if c == '"' || c == '\'' {
                state = state << 1;
                title_first_index = ic + 1;
            }
        } else {
            if c == '"' || c == '\'' {
                title = line[title_first_index..ic].to_string();
                break;
            }
        }
        ic += 1;
    }

    // if there is no title the inside title state
    // has not been reached
    if state == inside_link && link.len() == 0 {
        link = line[link_first_index..].trim_end().to_string();
    }

    vec![id, link, title]
}


/**
 * Parse link references found in Markdown content.
 *
 * Args:
 *     text (str): Markdown content to be parsed.
 *
 * Returns:
 *     list: Tuples or lists with 3 values ``(target, href, title)``
 *     for each link reference. If a title is not found or an
 *     identifier is empty they will be returned as empty strings.
 **/
pub fn parse_link_references(
    text: &str,
) -> Vec<Vec<String>> {
    let mut result: Vec<Vec<String>> = vec![];

    let links_iterator = MarkdownLinkReferencesParser::new(text);
    for link in links_iterator {
        result.push(link);
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case(
        &concat!(
            "[id1]: https://link1 \"Title 1\"\n\n\n",
            "[id2]: https://link2 \"Title 2\"\n\n\n"
        ),
        vec![
            vec![
                "id1".to_string(),
                "https://link1".to_string(),
                "Title 1".to_string(),
            ],
            vec![
                "id2".to_string(),
                "https://link2".to_string(),
                "Title 2".to_string(),
            ],
        ]
    )]
    #[case(
        &concat!(
            "[id-1]: https://link1 'Title 1'\n",
        ),
        vec![
            vec![
                "id-1".to_string(),
                "https://link1".to_string(),
                "Title 1".to_string(),
            ],
        ]
    )]
    #[case(
        &concat!(
            "[]: https://link1 \"Title 1\"\n",
        ),
        vec![
            vec![
                "".to_string(),
                "https://link1".to_string(),
                "Title 1".to_string(),
            ],
        ]
    )]
    #[case(
        &concat!(
            "[]: https://link1\n",
        ),
        vec![
            vec![
                "".to_string(),
                "https://link1".to_string(),
                "".to_string(),
            ],
        ]
    )]
    #[case(
        &concat!(
            "[id1]: https://link1 \"Title 1\"\n\n\n",
            "```\n[id2]: https://link2 \"Title 2\"\n```\n\n",
            "```\n[id3]: https://link3 \"Title 3\"\n```\n\n",
            "    [id4]: https://link4 \"Title 4\"\n```\n\n",
        ),
        vec![
            vec![
                "id1".to_string(),
                "https://link1".to_string(),
                "Title 1".to_string(),
            ],
        ]
    )]
    fn parse_link_references_test(
        #[case] text: &str,
        #[case] expected: Vec<Vec<String>>,
    ) {
        assert_eq!(parse_link_references(text), expected,);
    }
}
