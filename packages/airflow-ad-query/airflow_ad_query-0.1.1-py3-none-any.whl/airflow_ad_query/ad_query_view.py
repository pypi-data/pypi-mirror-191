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
import logging

# Importing base classes that we need to derive
from airflow.models import Connection
from airflow.security import permissions
from airflow.utils.session import provide_session
from airflow.www import auth
from flask import request, flash, Response
from flask_appbuilder import expose, BaseView as AppBuilderBaseView
from wtforms import (
    Form,
    SelectField,
    TextAreaField,
)

from airflow_ad_query import utils
from airflow_ad_query.commons import (
    MENU_CATEGORY,
    MENU_LABEL,
    QUERY_LIMIT,
    JS_FILES,
    ROUTE,
)

log = logging.getLogger(__name__)


# Creating a flask appbuilder BaseView
class AppBuilderQueryView(AppBuilderBaseView):
    default_view = "query"

    route_base = ROUTE
    class_permission_name = permissions.RESOURCE_ADTOOL = "Data Query"
    base_permissions = [permissions.ACTION_CAN_ACCESS_MENU, permissions.ACTION_CAN_READ]

    @expose("/query", methods=["POST", "GET"])
    @utils.gzipped
    @provide_session
    @auth.has_access([(permissions.ACTION_CAN_READ, permissions.RESOURCE_ADTOOL)])
    def query(self, session=None):
        dbs = session.query(Connection).order_by(Connection.conn_id).all()
        session.expunge_all()
        db_choices = []
        for db in dbs:
            db_choices.append(db.conn_id)
        conn_id_str = request.form.get("conn_id")
        csv = request.form.get("csv") == "true"
        sql = request.form.get("sql")

        class QueryForm(Form):
            conn_id = SelectField("Layout", choices=db_choices)
            sql = TextAreaField("SQL", widget=utils.AceEditorWidget())

        data = {
            "conn_id": conn_id_str,
            "sql": sql,
        }
        results = None
        has_data = False
        error = False
        if conn_id_str and request.method == "POST":
            db = [db for db in dbs if db.conn_id == conn_id_str][0]
            try:
                hook = db.get_hook()
                df = hook.get_pandas_df(
                    utils.limit_sql(sql, QUERY_LIMIT, conn_type=db.conn_type)
                )
                has_data = len(df) > 0
                df = df.fillna("")
                results = (
                    df.to_html(
                        classes=["table", "table-bordered", "table-striped", "no-wrap"],
                        index=False,
                        na_rep="",
                    )
                    if (has_data and not csv)
                    else ""
                )
            except Exception:
                log.exception("Query SQL execute failed")
                flash("SQL 执行失败，请检查 SQL 语句", "danger")
                error = True

        if has_data and len(df) == QUERY_LIMIT:
            flash("Query output truncated at " + str(QUERY_LIMIT) + " rows", "info")

        if not has_data and error:
            flash("No data", "error")

        if csv and not error:
            return Response(
                response=df.to_csv(index=False), status=200, mimetype="text/csv"
            )

        form = QueryForm(request.form, data=data)
        session.commit()
        return self.render_template(
            "query.html",
            form=form,
            title="Simple Query",
            js_files=JS_FILES,
            results=results or "",
            has_data=has_data,
        )


appbuilder_ad_query_view = AppBuilderQueryView()
appbuilder_view = {
    "name": MENU_LABEL,
    "category": MENU_CATEGORY,
    "view": appbuilder_ad_query_view,
}
