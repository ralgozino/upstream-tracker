# Quick and Dirty POC to track upstream releases.
import requests
import requests.auth
import os

from rich.table import Table
from rich.live import Live
import datetime

URLS = [
    'https://github.com/projectcalico/calico/releases',
    'https://github.com/kubernetes-sigs/ip-masq-agent/releases/latest',
    'https://github.com/prometheus-operator/prometheus-operator/releases/latest',
    'https://github.com/prometheus/prometheus/releases/latest',
    'https://github.com/prometheus/alertmanager/releases/latest',
    'https://github.com/grafana/grafana/releases/latest',
    'https://github.com/bloomberg/goldpinger/releases/latest',
    'https://github.com/brancz/kube-rbac-proxy',
    'https://github.com/kubernetes/kube-state-metrics/releases/latest',
    'https://github.com/prometheus/node_exporter/releases/latest',
    'https://github.com/kubernetes-sigs/metrics-server/releases/latest',
    'https://github.com/thanos-io/thanos/releases',
    'https://github.com/elastic/elasticsearch/releases/latest',
    'https://github.com/elastic/elasticsearch/releases/latest',
    'https://github.com/lmenezes/cerebro/releases/latest',
    'https://github.com/elastic/curator/releases/latest',
    'https://github.com/fluent/fluentd/releases/latest',
    'https://github.com/elastic/kibana/releases/latest',
    'https://github.com/jetstack/cert-manager/releases/latest',
    'https://github.com/kubernetes/ingress-nginx/releases/latest',
    'https://github.com/stakater/Forecastle/releases/latest',
    'https://github.com/tiagoapimenta/nginx-ldap-auth/releases/latest',
    'https://github.com/kubernetes/ingress-nginx/releases/latest',
    'https://github.com/pomerium/pomerium/releases',
    'https://github.com/vmware-tanzu/velero/releases/latest',
    'https://github.com/vmware-tanzu/velero/releases/latest',
    'https://github.com/open-policy-agent/gatekeeper/releases',
    'https://github.com/sighupio/gatekeeper-policy-manager/releases/',
    'https://github.com/goharbor/harbor/releases/latest',
    'https://github.com/istio/istio/releases/latest',
    'https://github.com/Kong/kong/releases/latest',
    'https://github.com/Kong/kubernetes-ingress-controller/releases/latest',
    'https://github.com/hashicorp/vault/releases/latest',
    'https://github.com/prometheus/statsd_exporter/releases/latest',
    'https://github.com/OpenVPN/openvpn/releases',
    'https://github.com/keycloak/keycloak/releases/latest',
    'https://github.com/zalando/postgres-operator/releases/latest',
    'https://github.com/prometheus-community/postgres_exporter/releases/latest',
    'https://github.com/spotahome/redis-operator/releases/latest',
    'https://github.com/redis/redis/releases/latest ',
    'https://gitlab.com/gitlab-org/gitlab-runner/-/releases',
    'https://github.com/mongodb/mongo/releases',
    'https://github.com/mongo-express/mongo-express/releases',
    'https://github.com/rabbitmq/rabbitmq-server/releases/latest',
    'https://github.com/heketi/heketi/releases/latest',
    'https://github.com/jenkinsci/docker-inbound-agent/releases/latest',
    'https://github.com/jenkinsci/jenkins/releases/tag/latest',
]

# IMPROVEMENT: ask for all or last X releases and calculate the latest one using
# semver. The `/latest` endpoint returns the latest release chronologically, not
# the latest version
API_ENDPOINT = 'https://api.github.com/repos/{owner}/{repo}/releases/latest'

table = Table(title="Latest Upstream Releases")

table.add_column("Project", justify="left", style="cyan", no_wrap=True)
table.add_column("Release Name", style="magenta")
table.add_column("Release Tag", style="purple")
table.add_column("Release Date", justify="left", style="green")
table.add_column("Is Draft?", justify="left")
table.add_column("Is Prerelease?", justify="left")


with Live(table, refresh_per_second=4) as live:
    # IMPROVEMENT: Parallelize these requests
    for repo in URLS:
        repo_name = f'{repo.split("/")[3]}/{repo.split("/")[4]}'
        api_endpoint = API_ENDPOINT.format(
            owner=repo.split('/')[3], repo=repo.split('/')[4])
        response = requests.get(api_endpoint,
                                auth=requests.auth.HTTPBasicAuth(
                                    'ralgozino', os.environ.get('HOMEBREW_GITHUB_API_TOKEN'))
                                )
        data = response.json()
        if data.get('published_at'):
            published_date = datetime.datetime.fromisoformat(
                data.get('published_at').replace('Z', '')).strftime('%d-%B-%Y')
        else:
            published_date = 'FAILED'
        table.add_row(repo_name,
                      data.get('name', 'FAILED'),
                      data.get('tag_name', 'FAILED'),
                      published_date,
                      str(data.get('draft', 'FAILED')),
                      str(data.get('prerelease', 'FAILED'),)
                      )
