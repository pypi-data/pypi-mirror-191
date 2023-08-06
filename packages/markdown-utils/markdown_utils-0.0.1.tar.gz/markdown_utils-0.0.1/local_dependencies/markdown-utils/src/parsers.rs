pub struct MarkdownLineByLineSkippingCodeblocksParser<'a> {
    lines_iterator: std::str::Lines<'a>,
    current_fenced_codeblock_delimiter: String,
}

impl MarkdownLineByLineSkippingCodeblocksParser<'_> {
    pub fn new(text: &str) -> MarkdownLineByLineSkippingCodeblocksParser {
        MarkdownLineByLineSkippingCodeblocksParser {
            lines_iterator: text.lines(),
            current_fenced_codeblock_delimiter: "".to_string(), 
        }
    }
}

impl Iterator for MarkdownLineByLineSkippingCodeblocksParser<'_> {
    type Item = String;

    fn next(&mut self) -> Option<String> {
        let line = self.lines_iterator.next();
        if line == None {
            return None;
        }
        if self.current_fenced_codeblock_delimiter == "" {
            let trimmed_line = line?.trim();
            if trimmed_line.starts_with("```") || trimmed_line.starts_with("~~~") {
                // enter fenced codeblock
                self.current_fenced_codeblock_delimiter =
                    trimmed_line[0..3].to_string();
            } else if !line?.starts_with("    ") || line?.starts_with("     ") {
                // don't enter indented code block (4 spaces)
                // but yes in nested content (+4 spaces)
                return Some(line?.to_string());
            } else {
                return self.next();
            }
        } else if line?.trim_start().starts_with(
            &self.current_fenced_codeblock_delimiter
        ) {
            self.current_fenced_codeblock_delimiter = "".to_string();
        }
        return self.next();
    }
}
