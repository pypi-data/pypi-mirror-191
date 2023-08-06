import typing as t

import pandas as pd
from sarus_data_spec.config import WHITELISTED_TRANSFORMS

from sarus.utils import _registered_functions, _registered_methods


def generate_op_list() -> t.Tuple[t.List[str], t.List[str]]:
    """Generate the list of registered operations and whitelisted operations.

    NB: This does not list DataspecWrappers without any operations declared.
    """
    global _registered_functions, _registered_methods

    methods = pd.DataFrame.from_records(_registered_methods)
    methods.columns = ["module", "class", "method", "code"]

    functions = pd.DataFrame.from_records(_registered_functions)
    functions.columns = ["module", "function", "code"]

    all_items = methods.append(functions, ignore_index=True)

    lines, whitelisted_lines = [], []
    for mod_name, mod_df in all_items.groupby(by="module"):
        has_whitelisted = False
        mod_whitelisted_lines = []

        lines.append(f"\n# {mod_name}")
        mod_whitelisted_lines.append(f"# {mod_name}")

        fns = (
            mod_df.loc[:, ["function", "code"]]
            .dropna()
            .sort_values(by="function")
        )
        mask = fns.code.apply(lambda x: x in WHITELISTED_TRANSFORMS)
        whitelisted_fns = fns[mask]
        if len(fns) > 0:
            lines.append("\n## Functions")
            lines += list(map(lambda x: f"- `{x}`", fns.function))
        if len(whitelisted_fns) > 0:
            has_whitelisted = True
            mod_whitelisted_lines.append("\n## Functions")
            mod_whitelisted_lines += list(
                map(lambda x: f"- `{x}`", whitelisted_fns.function)
            )

        for class_name, class_df in mod_df.groupby("class"):
            if class_name == "DataSpecWrapper":
                class_name = "Generic Operations"
            lines.append(f"\n## {class_name}")
            methods = (
                class_df.loc[:, ["method", "code"]]
                .dropna()
                .sort_values(by="method")
            )
            mask = methods.code.apply(lambda x: x in WHITELISTED_TRANSFORMS)
            lines += list(map(lambda x: f"- `{x}`", methods.method))

            whitelisted_methods = methods[mask]
            if len(whitelisted_methods) > 0:
                has_whitelisted = True
                mod_whitelisted_lines.append(f"\n## {class_name}")
                mod_whitelisted_lines += list(
                    map(lambda x: f"- `{x}`", whitelisted_methods.method)
                )

        if has_whitelisted:
            whitelisted_lines += mod_whitelisted_lines

    return lines, whitelisted_lines


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    default_output_dir = (
        Path(__file__).parent.parent.parent / "docs" / "sdk_documentation"
    )
    ops_file = "op_list.md"
    whitelisted_file = "whitelisted_op_list.md"

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", "-n", dest="dry_run", action="store_true")
    parser.add_argument(
        "--output-dir",
        "-o",
        dest="output_dir",
        default=str(default_output_dir),
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    ops_lines, whitelisted_ops_lines = generate_op_list()

    ops_path = output_dir / ops_file
    whitelisted_ops_path = output_dir / whitelisted_file

    ops_txt = "\n".join(ops_lines)
    whitelisted_ops_txt = "\n".join(whitelisted_ops_lines)

    if args.dry_run:
        with open(ops_path) as f:
            current_ops = f.read()

        with open(whitelisted_ops_path) as f:
            current_whitelisted_ops = f.read()

        if ops_txt != current_ops:
            raise ValueError("Ops list is not up to date.")

        if whitelisted_ops_txt != current_whitelisted_ops:
            raise ValueError("Whitelisted ops list is not up to date.")

        print("Everything up to date.")
    else:
        print(f"Writing ops to {ops_path}")
        with open(ops_path, "w") as f:
            f.write(ops_txt)

        print(f"Writing whitelisted ops to {whitelisted_ops_path}")
        with open(whitelisted_ops_path, "w") as f:
            f.write(whitelisted_ops_txt)
