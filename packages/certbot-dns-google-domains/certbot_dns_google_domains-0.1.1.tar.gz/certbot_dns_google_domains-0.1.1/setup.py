# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_dns_google_domains']

package_data = \
{'': ['*']}

install_requires = \
['certbot>=1.23.0', 'dataclasses-json>=0.5.7,<0.6.0', 'zope.interface>=5.5.0']

entry_points = \
{'certbot.plugins': ['dns-google-domains = '
                     'certbot_dns_google_domains.dns_google_domains:Authenticator']}

setup_kwargs = {
    'name': 'certbot-dns-google-domains',
    'version': '0.1.1',
    'description': 'Certbot DNS authenticator for Google Domains',
    'long_description': "# certbot-dns-google-domains\n\n## Named Arguments\n\nOption|Description\n---|---|\n`--authenticator dns-google-domains`|Select this authenticator plugin.\n`--dns-google-domains-credentials FILE`|Path to the INI file with credentials.\n`--dns-google-domains-propagation-seconds INT`|How long to wait for DNS changes to propagate. Default = 30s.\n\n## Credentials\n\nThe credentials file includes the access token for Google Domains.\n\n```.ini\ndns_google_domains_access_token = abcdef\n```\n\n## Usage Example\n\n### Docker / Podman\n\n``` bash\ndocker run \\\n  -v '/var/lib/letsencrypt:/var/lib/letsencrypt' \\\n  -v '/etc/letsencrypt:/etc/letsencrypt' \\\n  --cap-drop=all \\\n  ghcr.io/aaomidi/certbot-dns-google-domains:latest \\\n  certbot certonly \\\n  --authenticator 'dns-google-domains' \\\n  --dns-google-domains-credentials '/var/lib/letsencrypt/dns_google_domains_credentials.ini' \\\n  --no-eff --non-interactive --server 'https://acme-staging-v02.api.letsencrypt.org/directory' \\\n  --agree-tos --email 'email@example.com' -d 'example.com'\n```\n\nNotes:\n- `-v '/var/lib/letsencrypt:/var/lib/letsencrypt'` is where certbot by default outputs certificates, keys, and account information.\n- `-v '/etc/letsencrypt:/etc/letsencrypt'` is where certbot keeps its configuration.\n- `--authenticator 'dns-google-domains'` uses the dns-google-domains authenticator.\n- `--dns-google-domains-credentials '/var/lib/letsencrypt/dns_google_domains_credentials.ini'` is the path to the credentials file.\n",
    'author': 'Amir Omidi',
    'author_email': 'amir@aaomidi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2',
}


setup(**setup_kwargs)
