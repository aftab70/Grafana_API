from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel,
    Target, GridPos,
    OPS_FORMAT
)

dashboard = Dashboard(
    title="Python generated example dashboard",
    description="Example dashboard using the Random Walk and default Prometheus datasource",
    tags=[
        'example'
    ],
    timezone="browser",
    panels=[
        TimeSeries(
            title="Random Walk",
            dataSource='default',
            targets=[
                Target(
                    datasource='grafana',
                    expr='example',
                ),
            ],
            gridPos=GridPos(h=8, w=16, x=0, y=0),
        ),
        GaugePanel(
            title="Random Walk",
            dataSource='default',
            targets=[
                Target(
                    datasource='grafana',
                    expr='example',
                ),
            ],
            gridPos=GridPos(h=4, w=4, x=17, y=0),
        ),
        TimeSeries(
            title="Prometheus http requests",
            dataSource='prometheus',
            targets=[
                Target(
                    expr='rate(prometheus_http_requests_total[5m])',
                    legendFormat="{{ handler }}",
                    refId='A',
                ),
            ],
            unit=OPS_FORMAT,
            gridPos=GridPos(h=8, w=16, x=0, y=10),
        ),
    ],
).auto_panel_ids()

print(type(dashboard))


from grafanalib.core import Dashboard
from grafanalib._gen import DashboardEncoder
import json
import requests
from os import getenv


def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    '''
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param dashboard - Dashboard() created via grafanalib
    '''

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }, sort_keys=True, indent=2, cls=DashboardEncoder)


def upload_to_grafana(json, server, api_key, verify=True):

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    r = requests.post(f"http://{server}/api/dashboards/db", data=my_dashboard_json, headers=headers, verify=verify)
    # TODO: add error handling
    print(f"{r.status_code} - {r.content}")
    print(json)


api_key = "eyJrIjoiYnRycHk0STJUMzVyUFI2ZkZ5NFEzdDh1QzBDMHlDS1kiLCJuIjoiYWRtaW4iLCJpZCI6MX0="
server = "20.25.0.107:3000"

my_dashboard_json = get_dashboard_json(dashboard, overwrite=True)
upload_to_grafana(my_dashboard_json, server, api_key)
