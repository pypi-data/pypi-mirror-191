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
__all__ = [
    "PLUGIN_NAME",
    "MENU_CATEGORY",
    "MENU_LABEL",
    "ROUTE",
    "STATIC",
    "QUERY_LIMIT",
    "JS_FILES",
]

PLUGIN_NAME = "ad_query"
MENU_CATEGORY = ""
MENU_LABEL = "Data Query"
ROUTE = "/" + PLUGIN_NAME
STATIC = "static"
QUERY_LIMIT = 10000

JS_FILES = [
    "ace.js",
    "jquery.dataTables.js",
    "mode-sql.js",
    "dataTables.bootstrap.js",
    "jquery.dataTables.min.js",
    "theme-crimson_editor.js",
]
