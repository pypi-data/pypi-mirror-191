# -*- mode: python -*-

import os
import pathlib
import re
import stat
import subprocess
from subprocess import PIPE, STDOUT, Popen

import pytest


def test_kubectl_version_matches_kubelet_version():
    """
    vagrant@vagrant:~$ kubectl version --output=yaml --client | awk '/gitVersion/{print $2;}'
    v1.26.1
    vagrant@vagrant:~$ kubelet --version
    Kubernetes v1.26.1
    vagrant@vagrant:~$
    """
    cmd = "kubectl version --output=yaml --client|awk '/gitVersion/{print $2;}'"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()
    assert "disk /opt/data" in output


def test_prometheus_config_exists():
    assert pathlib.Path("/etc/prometheus/prometheus.yml").exists()


def test_prometheus_config_is_valid():
    cmd = "/usr/local/bin/promtool check config /etc/prometheus/prometheus.yml"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "FAILED" not in stdout.decode()


def test_prometheus_alert_rules_are_valid():
    def runcmd(cmd):
        process = subprocess.Popen(
            cmd.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        assert stderr.decode() == ""
        assert "FAILED" not in stdout.decode()

    promdir = pathlib.Path("/etc/prometheus")
    for path in promdir.glob("prometheus-alertrules*.yml"):
        cmd = f"/usr/local/bin/promtool check rules {path}"
        runcmd(cmd)


def test_prometheus_data_dir_exists():
    assert pathlib.Path("/opt/data/data/prometheus").exists()


def test_prometheus_is_running():
    cmd = "systemctl status prometheus.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_prometheus_is_listening_on_expected_port():
    cmd = "lsof -i :9090 -P"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert "prometheus" in stdout.decode()
    assert "*:9090 (LISTEN)" in stdout.decode()


def test_blackbox_exporter_is_running():
    cmd = "systemctl status blackbox_exporter.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_grafana_config_exists():
    assert pathlib.Path("/etc/blackbox_exporter/blackbox.yml").exists()


def test_node_exporter_is_running():
    cmd = "systemctl status node_exporter.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_grafana_config_exists():
    assert pathlib.Path("/etc/grafana/grafana.ini").exists()


def test_grafana_is_running():
    cmd = "systemctl status grafana-server.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_grafana_can_read_ssl_certificate():
    # grafana-server service which runs as user grafana needs to
    # access proxy SSL/TLS certificate
    hostname = pathlib.Path("/var/streambox/provision/dns/dns1").read_text().strip()
    domain = pathlib.Path("/var/streambox/provision/dns/domain").read_text().strip()
    fqdn = f"{hostname}.{domain}"
    key_path = pathlib.Path(f"/etc/letsencrypt/live/{fqdn}/privkey.pem")

    cmd = f"sudo -u grafana cat {key_path}"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    assert stderr.decode() == ""
    assert process.returncode == 0


def test_node_exporter_is_running():
    cmd = "systemctl status node_exporter.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_node_exporter_is_listening_on_port_9100():
    cmd = "netstat -ntplu"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    found = False
    for line in stdout.decode().splitlines():
        mo = re.search(r"tcp.*:9100.*node_exporter", line)
        if mo:
            found = True

    assert stderr.decode() == ""
    assert found == True


def test_alertmanager_config_exists():
    assert pathlib.Path("/etc/alertmanager/alertmanager.yml").exists()


def test_alertmanager_proxy_credentials_config_is_valid():
    p = pathlib.Path("/etc/alertmanager/.credentials")
    assert p.exists()
    assert p.is_file()


def test_alertmanager_proxy_credentials_config_can_be_read_by_ngnix():
    p = pathlib.Path("/etc/alertmanager/.credentials")
    cmd = f"sudo -u nginx cat {p}"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 0
    assert stderr.decode() == ""


def test_alertmanager_proxy_credentials_config_permissions_are_correct():
    p = pathlib.Path("/etc/alertmanager/.credentials")
    st = os.stat(p)
    assert bool(st.st_mode & stat.S_IRGRP) == True
    assert bool(st.st_mode & stat.S_IRUSR) == True
    assert bool(st.st_mode & stat.S_IWGRP) == False
    assert bool(st.st_mode & stat.S_IXGRP) == False
    assert bool(st.st_mode & stat.S_IROTH) == False


def test_alertmanager_config_is_valid():
    cmd = "/usr/local/bin/amtool check-config /etc/alertmanager/alertmanager.yml"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert process.returncode == 0
    assert stderr.decode() == ""


def test_alertmanager_can_send_email():
    config = pathlib.Path("/etc/alertmanager/alertmanager.yml").read_text()
    assert "smtp_auth_password:" in config
    assert "smtp.gmail.com:587" in config
    assert not "@SMTP_AUTH_PASSWORD@" in config


def test_alertmanager_is_running():
    cmd = "systemctl status alertmanager.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()


def test_alertmanager_is_listening_on_expected_port():
    cmd = "lsof -i :9093 -P"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert "alertmana" in stdout.decode()
    assert "*:9093 (LISTEN)" in stdout.decode()


@pytest.mark.xfail(
    reason="this is on my bucket list.  I have forgotten what its goal was..."
)
def test_alertmanager_responds_to_GET_request():
    cmd = "curl -I http://localhost:9093"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert "HTTP/1.1 200 OK" in stdout.decode()


def test_profile_config_exists():
    assert "alias python=python3" in pathlib.Path("/root/.alias").read_text()


def test_nginx_user_exists():
    cmd = "id -u nginx"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    assert not "no such user" in p.stdout.read().decode()

    # sanity check
    cmd = "id -u nginx1"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    assert "no such user" in p.stdout.read().decode()


def test_nginx_index_html_exists():
    hostname = pathlib.Path("/var/streambox/provision/dns/dns1").read_text().strip()
    domain = pathlib.Path("/var/streambox/provision/dns/domain").read_text().strip()
    fqdn = f"{hostname}.{domain}"
    index_path = pathlib.Path(f"/var/www/{fqdn}/public_html/index.html")

    assert index_path.exists()
    assert index_path.is_file()
    assert index_path.stat().st_size != 0


def test_nginx_config_is_not_corrupted():
    cmd = "nginx -t"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()
    assert "syntax is ok" in output
    assert "test is successful" in output


@pytest.mark.xfail(
    reason="this seems innocuous, but perhaps we should fix this to keep logs clean"
)
def test_nginx_workaround_is_in_place():
    # https://www.digitalocean.com/community/questions/unable-to-start-nginx-failed-to-read-pid-from-file-run-nginx-pid?answer=31791

    cmd = "journalctl -xe"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()
    assert not "Failed to read PID from file /run/nginx.pid: Invalid argument" in output


def test_nginx_is_running():
    cmd = "systemctl status nginx.service"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert "Active: active (running)" in stdout.decode()

    cmd = "ss -tlpn"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert 'users:(("nginx"' in stdout.decode()
    assert ":80" in stdout.decode()


def test_nginx_proxy_is_reachable():
    hostname = pathlib.Path("/var/streambox/provision/dns/dns1").read_text().strip()
    domain = pathlib.Path("/var/streambox/provision/dns/domain").read_text().strip()

    cmd = f"curl -sSL -I https://{hostname}.{domain}:3000/login"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == "", "'iptables --flush' might fix this"


# FIXME:
@pytest.mark.xfail(
    reason="Should resovlve this, but it doesn't seem to adversly affect production"
)
def test_nginx_is_serving_the_correct_default_page():
    access_log = pathlib.Path(
        "/var/log/nginx/grafana.prometheus.streambox.com.access.log"
    )
    error_log = pathlib.Path(
        "/var/log/nginx/grafana.prometheus.streambox.com.error.log"
    )

    cmd = "curl --connect-timeout 1 --insecure -sSL http://grafana.prometheus.streambox.com:80"

    process = subprocess.Popen(
        cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    assert stderr.decode() == ""
    assert access_log.exists()
    assert access_log.is_file()
    assert access_log.stat().st_size != 0
    assert error_log.stat().st_size == 0


# FIXME:
@pytest.mark.xfail(reason="Need to close http alltogether")
def test_ensure_prometheus_ui_is_not_available_to_public():
    cmd = "curl --connect-timeout 1 -sS http://grafana.prometheus.streambox.com:3000"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read().decode()

    assert "curl: (28) Connection timed out after" in output


def test_certbot_certs_exist_exists():
    hostname = pathlib.Path("/var/streambox/provision/dns/dns1").read_text().strip()
    domain = pathlib.Path("/var/streambox/provision/dns/domain").read_text().strip()
    fqdn = f"{hostname}.{domain}"

    f1 = pathlib.Path(f"/etc/letsencrypt/live/{fqdn}/fullchain.pem")
    assert f1.exists()
    assert f1.is_file()
    assert f1.stat().st_size != 0

    f2 = pathlib.Path(f"/etc/letsencrypt/live/{fqdn}/privkey.pem")
    assert f1.exists()
    assert f1.is_file()
    assert f1.stat().st_size != 0
