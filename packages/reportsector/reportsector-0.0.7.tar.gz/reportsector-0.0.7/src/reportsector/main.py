import pathlib

import jinja2
import pkg_resources

from . import utils


def main():
    package = __name__.split(".")[0]
    TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates"))

    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(loader=loader, keep_trailing_newline=True)
    cache_paths = []
    install_paths = []
    other_script_paths = []

    ##############################
    # yq install
    ##############################
    template = env.get_template("yq.sh.j2")
    path = pathlib.Path("cache_yq.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_yq.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # yj install
    ##############################
    template = env.get_template("yq.sh.j2")
    path = pathlib.Path("cache_yj.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_yj.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # containerd
    ##############################
    template = env.get_template("containerd.sh.j2")
    path = pathlib.Path("cache_containerd.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_containerd.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # runc
    ##############################
    template = env.get_template("runc.sh.j2")
    path = pathlib.Path("cache_runc.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_runc.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # kubectl
    ##############################
    template = env.get_template("kubectl.sh.j2")
    path = pathlib.Path("cache_kubectl.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_kubectl.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # nerdctl
    ##############################
    template = env.get_template("nerdctl.sh.j2")
    path = pathlib.Path("cache_nerdctl.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_nerdctl.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # kubeadmin init
    ##############################
    template = env.get_template("kubeadm-init.sh.j2")
    path = pathlib.Path("kubeadm-init.sh")
    other_script_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # buildkit install
    ##############################
    template = env.get_template("buildkit.sh.j2")
    path = pathlib.Path("cache_buildkit.sh")
    cache_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    path = pathlib.Path("install_buildkit.sh")
    install_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # install.sh
    ##############################
    template = env.get_template("aggregate.sh.j2")
    path = pathlib.Path("install.sh")
    other_script_paths.append(path)
    rendered = template.render(cache_only=False)
    path.write_text(rendered)
    path.chmod(0o775)

    ##############################
    # cache.sh
    ##############################
    template = env.get_template("aggregate.sh.j2")
    path = pathlib.Path("cache.sh")
    other_script_paths.append(path)
    rendered = template.render(cache_only=True)
    path.write_text(rendered)
    path.chmod(0o775)

    # end scripts

    script_paths = cache_paths + install_paths + other_script_paths
    utils.prettify_paths(*script_paths)

    cache_dir = pathlib.Path("stage")
    pathlib.Path.mkdir(cache_dir, parents=True, exist_ok=True)
