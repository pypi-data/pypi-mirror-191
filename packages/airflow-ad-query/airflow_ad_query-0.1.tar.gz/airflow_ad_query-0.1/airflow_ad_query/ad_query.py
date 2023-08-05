#
# Copyright 2022 wano <whox@foxmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint

from airflow_ad_query.ad_query_view import appbuilder_view
from airflow_ad_query.commons import STATIC

__author__ = "wano"

__all__ = ["AirflowQueryPlugin"]

# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "ad_query_blueprint",
    __name__,
    template_folder="templates",
    static_folder=STATIC,
    static_url_path=STATIC,
    url_prefix="/ad_query",
)


# Defining the plugin class
class AirflowQueryPlugin(AirflowPlugin):
    name = "ad_query_plugin"
    flask_blueprints = [bp]
    appbuilder_views = [appbuilder_view]
