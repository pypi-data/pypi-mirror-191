from pathlib import Path, PurePath
import os
from jinja2 import Environment, PackageLoader
import json
import os
import shutil


def write_file(output_dir, file_name, content):
    with open(output_dir / file_name, "w") as file:
        file.write(content)


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def write_file(output_dir, file_name, content):
    with open(output_dir / file_name, "w") as file:
        file.write(content)


def _generated_file_name(file):
    return file.replace(".template", "")


def _package_name(template_dir_path):
    parent = str(template_dir_path.parent)
    # single path segment
    if parent == ".":
        return f"eggfarm.templates"
    else:
        return f"eggfarm.templates.{parent.replace('/', '.')}"


def _generate_file_with_template(output_dir, template_dir, file, function_name):
    camel_cased_function_name = to_camel_case(function_name)
    function_class = f"{camel_cased_function_name}Function"

    template_dir_path = PurePath(template_dir)
    if template_dir_path.name:
        package_name = _package_name(template_dir_path)
        env = Environment(loader=PackageLoader(package_name, template_dir_path.name))
    else:
        env = Environment(loader=PackageLoader("eggfarm", "templates"))

    template = env.get_template(file)
    content = template.render(func_name=function_name, func_class=function_class)

    if template_dir == ".":
        file_dir = output_dir
    else:
        file_dir = os.path.join(output_dir, template_dir)

    write_file(Path(file_dir), _generated_file_name(file), content)


# the eggfarm.templates.__init__.py is just to make jinja2 happy to load template
def _is_template(file):
    return ".template" in file


def _check_output_dir(output_dir, default_dir):
    if output_dir is None:
        output_dir = default_dir

    output_dir_path = Path(os.path.join(output_dir))
    if output_dir_path.exists():
        if output_dir_path.is_file():
            raise FileExistsError(f"{output_dir} is a file, please specify a directory as output directory")
        elif any(os.scandir(output_dir_path)):
            raise FileExistsError(f"{output_dir} is not empty, please use an empty directory as output directory")
    else:
        output_dir_path.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_skeleton(args):
    function_name = args["function_name"]
    output_dir = _check_output_dir(args.get("output_dir"), function_name)

    print(f"generating table function skeleton for {function_name} under directory {output_dir}")
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "eggfarm/templates")

    for root, dirs, files in os.walk(templates_dir):
        if os.path.basename(root) == "__pycache__":
            continue
        for dir in dirs:
            if dir == "__pycache__":
                continue
            Path(os.path.join(output_dir, dir)).mkdir(parents=True, exist_ok=True)

        for file in files:
            if _is_template(file):
                template_dir = os.path.relpath(root, templates_dir)
                _generate_file_with_template(output_dir, template_dir, file, function_name)

    os.rename(os.path.join(output_dir, "func"), os.path.join(output_dir, function_name))
