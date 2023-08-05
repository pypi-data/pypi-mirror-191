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

import functools
import gzip
from html import escape
from io import BytesIO as IO

import wtforms
from flask import after_this_request, request
from markupsafe import Markup
from wtforms.compat import text_type


def limit_sql(sql, limit, conn_type):
    sql = sql.strip()
    sql = sql.rstrip(";")
    if sql.lower().startswith("select"):
        if conn_type in ["mssql"]:
            sql = """\
            SELECT TOP {limit} * FROM (
            {sql}
            ) qry
            """.format(
                limit=limit, sql=sql
            )
        elif conn_type in ["oracle"]:
            sql = """\
            SELECT * FROM (
            {sql}
            ) qry
            WHERE ROWNUM <= {limit}
            """.format(
                limit=limit, sql=sql
            )
        else:
            sql = """\
            SELECT * FROM (
            {sql}
            ) qry
            LIMIT {limit}
            """.format(
                limit=limit, sql=sql
            )
    return sql


def gzipped(f):
    """
    Decorator to make a view compressed
    """

    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get("Accept-Encoding", "")

            if "gzip" not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (
                    response.status_code < 200
                    or response.status_code >= 300
                    or "Content-Encoding" in response.headers
            ):
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode="wb", fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers["Content-Encoding"] = "gzip"
            response.headers["Vary"] = "Accept-Encoding"
            response.headers["Content-Length"] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


class AceEditorWidget(wtforms.widgets.TextArea):
    """
    Renders an ACE code editor.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = """
        <div id="{el_id}" style="height:100px;">{contents}</div>
        <textarea
            id="{el_id}_ace" name="{form_name}"
            style="display:none;visibility:hidden;">
        </textarea>
        """.format(
            el_id=kwargs.get("id", field.id),
            contents=escape(text_type(field._value())),
            form_name=field.id,
        )
        return Markup(html)
