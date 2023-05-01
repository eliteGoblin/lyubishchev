from time_report_notebook import dict_tree_to_parent_tree


def test_dict_tree_to_parent_tree() -> None:
    examples = [
        (
            {
                "effective_output": {
                    "self_improving": {
                        "tech": {"lyubishchev": 3, "oj": 4, "software": 5},
                        "non_tech": {
                            "bibliotherapy": 1,
                            "linkedin": 2,
                            "audible": 6,
                        },
                    },
                    "work": 10,
                }
            },
            (
                [
                    "effective_output",
                    "self_improving",
                    "tech",
                    "lyubishchev",
                    "oj",
                    "software",
                    "non_tech",
                    "bibliotherapy",
                    "linkedin",
                    "audible",
                    "work",
                ],
                [
                    "",
                    "effective_output",
                    "self_improving",
                    "tech",
                    "tech",
                    "tech",
                    "self_improving",
                    "non_tech",
                    "non_tech",
                    "non_tech",
                    "effective_output",
                ],
                [0, 0, 0, 3, 4, 5, 0, 1, 2, 6, 10],
            ),
        ),
        (
            {
                "root": {
                    "a": {"aa": 1, "ab": 2},
                    "b": {"ba": 3, "bb": {"bba": 4, "bbb": {"bbba": 5}}},
                }
            },
            (
                [
                    "root",
                    "a",
                    "aa",
                    "ab",
                    "b",
                    "ba",
                    "bb",
                    "bba",
                    "bbb",
                    "bbba",
                ],
                ["", "root", "a", "a", "root", "b", "b", "bb", "bb", "bbb"],
                [0, 0, 1, 2, 0, 3, 0, 4, 0, 5],
            ),
        ),
    ]

    # Iterate over the examples and check the output of the function
    for example in examples:
        input_tree, expected_output = example

        # Call the function with the current input example
        nodes_name, parent_node, node_values = dict_tree_to_parent_tree(input_tree)

        # Check that the actual output matches the expected output
        assert nodes_name == expected_output[0]
        assert parent_node == expected_output[1]
        assert node_values == expected_output[2]
