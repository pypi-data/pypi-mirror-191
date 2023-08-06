import importlib.util
import pprint
import sys
import time

import markdown_utils as rs_md_utils

spec = importlib.util.spec_from_file_location(
    "markdown_utils",
    "src/markdown_utils.py",
)
py_md_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(py_md_utils)

TIMEOUT = 500  # ms
WARN_TIMEOUT = 300

IMPLEMENTATIONS = [
    ("Python", py_md_utils),
    ("Rust", rs_md_utils),
]

FUNCTIONS = [
    (
        "modify_headings_offset",
        20000,
        (
            (("# Foo\n## Bar\n### Baz\n", 1), "## Foo\n### Bar\n#### Baz"),
            (("# Foo\n## Bar\n### Baz\n", 3), "#### Foo\n##### Bar\n###### Baz"),
            (("## Foo\n### Bar\n#### Baz\n", -1), "# Foo\n## Bar\n### Baz"),
        ),
    ),
    (
        "n_backticks_to_wrap_codespan",  # function name
        20000,  # iterations
        (
            # function arguments, expected results
            (("r", "0000r0rr00rrrr00rrrrr00"), 3),
            (("r", "00000rr00rrrr00rrrrr00"), 1),
            (("r", "0000000rrrr00rrrrr00"), 1),
            (("r", "0000000"), 0),
            (("r", "0r00rr00rrr00"), 4),
        ),
    ),
    (
        "parse_link_references",
        20000,
        (
            (
                ('[foo]: http://example1.com "Title 1"\n',),
                [
                    ["foo", "http://example1.com", "Title 1"],
                ],
            ),
            (
                (
                    '[bar]: http://example2.com "Title 2"\n'
                    '[baz]: http://example3.com "Title 3"\n',
                ),
                [
                    ["bar", "http://example2.com", "Title 2"],
                    ["baz", "http://example3.com", "Title 3"],
                ],
            ),
        ),
    ),
]

EXITCODE = 0

for func_name, iterations, args_expected_results in FUNCTIONS:
    perf_stats = {}

    sys.stdout.write(f"{func_name}(...)\n")
    for lang, impl in IMPLEMENTATIONS:
        start = time.time()
        test_failed = False
        for func_args, expected_result in args_expected_results:
            func = getattr(impl, func_name)
            for _ in range(iterations):
                func(*func_args)
            result = func(*func_args)
            if result != expected_result:
                if not test_failed:
                    sys.stdout.write(
                        f"FAILED! ({lang})"
                        f" {func_name}{pprint.pformat(func_args)}"
                        f" returned '{result}'"
                        f" instead of '{expected_result}'\n"
                    )
                    EXITCODE = 1
                    test_failed = True
        end = time.time()
        ms = (end - start) * 1000
        sys.stdout.write(f"  {lang}: {ms} ms\n")

        perf_stats[lang] = ms

    x_faster = perf_stats["Python"] / perf_stats["Rust"]
    if x_faster <= 1:
        sys.stdout.write(
            f"FAILED!    {perf_stats['Rust'] / perf_stats['Python']}x slower\n"
        )
        EXITCODE = 1
    else:
        sys.stdout.write(f"     {x_faster}x faster\n")

    if max(perf_stats.values()) > TIMEOUT:
        sys.stdout.write(f"FAILED! The test is too long\n")
        EXITCODE = 1

    if max(perf_stats.values()) > WARN_TIMEOUT:
        sys.stdout.write(f"WARNING! The test is too long\n")

    sys.stdout.write("\n")
