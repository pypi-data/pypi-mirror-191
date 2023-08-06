# OSITAH validation sub-application

from datetime import datetime
from uuid import uuid4

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import dcc, html
from dash.dependencies import MATCH, Input, Output, State
from flask import session

from ositah.app import app
from ositah.utils.agents import get_agents
from ositah.utils.exceptions import SessionDataMissing
from ositah.utils.menus import (
    DATA_SELECTED_SOURCE_ID,
    TABLE_TYPE_DUMMY_STORE,
    TABLE_TYPE_TABLE,
    TEAM_SELECTED_VALUE_ID,
    TEAM_SELECTION_DATE_ID,
    VALIDATION_PERIOD_SELECTED_ID,
    build_accordion,
    create_progress_bar,
    team_list_dropdown,
)
from ositah.utils.period import get_validation_period_data, get_validation_period_id
from ositah.utils.projects import (
    CATEGORY_DEFAULT,
    DATA_SOURCE_HITO,
    DATA_SOURCE_OSITAH,
    get_team_projects,
    project_time,
    time_unit,
)
from ositah.utils.utils import (
    SEMESTER_HOURS,
    SEMESTER_WEEKS,
    TEAM_LIST_ALL_AGENTS,
    TIME_UNIT_HOURS,
    TIME_UNIT_HOURS_EN,
    TIME_UNIT_WEEKS,
    WEEK_HOURS,
    GlobalParams,
    general_error_jumbotron,
    no_session_id_jumbotron,
)

TABLE_COLUMN_VALIDATION = "Validation"

TABLE_ID_DECLARATION_STATS = "declaration-stats"
TABLE_ID_MISSING_AGENTS = "missing-agents"
TABLE_ID_VALIDATION = "validation"

VALIDATION_TAB_MENU_ID = "validation-tabs"
TAB_ID_DECLARATION_STATS = "declaration-stats-tab"
TAB_ID_MISSING_AGENTS = "missing-agents-tab"
TAB_ID_VALIDATION = "validation-tab"

VALIDATION_LOAD_INDICATOR_ID = "validation-data-load-indicator"
VALIDATION_SAVED_INDICATOR_ID = "validation-saved-data-load-indicator"
VALIDATION_DISPLAY_INTERVAL_ID = "validation-display-callback-interval"
VALIDATION_SAVED_ACTIVE_TAB_ID = "validation-saved-active-tab"

VALIDATION_DECLARATIONS_SELECT_ALL = 0
VALIDATION_DECLARATIONS_SELECT_NOT_VALIDATED = 1
VALIDATION_DECLARATIONS_SELECT_VALIDATED = 2
VALIDATION_DECLARATIONS_SWITCH_ID = "validation-declaration-set-switch"
VALIDATION_DECLARATIONS_SELECTED_ID = "validation-selected-declaration-set"


def build_validation_table(team, team_selection_date, declaration_set: int, period_date: str):
    """
    Build the agent list of the selected team with their declarations. Returns a table.

    :param team: selected team
    :param team_selection_date: last time the team selection was changed
    :param declaration_set: selected declaration set (all, validated or non-validated ones)
    :param period_date: a date that must be inside the declaration period
    :return: DBC table
    """
    global_params = GlobalParams()
    column_names = global_params.columns
    try:
        session_data = global_params.get_session_data()
    except SessionDataMissing:
        return no_session_id_jumbotron()

    if session["user_email"] in global_params.roles["read-only"]:
        validation_disabled = True
    else:
        if session_data.get_role() in global_params.validation_params["override_period"]:
            validation_disabled = False
        else:
            validation_disabled = not validation_started(period_date)

    validation_data = get_all_validation_status(period_date)

    project_declarations = get_team_projects(
        team, team_selection_date, period_date, DATA_SOURCE_HITO
    )
    if project_declarations is None:
        return html.Div(
            [
                dbc.Alert(
                    f"Aucune déclaration effectuée pour l'équipe '{team}'",
                    color="warning",
                ),
            ]
        )
    declarations = category_declarations(project_declarations)

    if team == TEAM_LIST_ALL_AGENTS:
        declaration_list = declarations
    else:
        declaration_list = declarations[declarations[column_names["team"]].str.match(team)]
    declaration_list["validation_disabled"] = validation_disabled

    data_columns = [CATEGORY_DEFAULT]
    data_columns.extend(global_params.project_categories.keys())

    validated_project_declarations = get_team_projects(
        team, team_selection_date, period_date, DATA_SOURCE_OSITAH, use_cache=False
    )
    if validated_project_declarations is None:
        declaration_list["validated"] = False
        declaration_list["hito_missing"] = False
        validated_declarations_num = 0
        hito_missing_num = 0
        hito_missing_msg = ""
    else:
        validated_declarations_num = len(validated_project_declarations)
        validated_declarations = category_declarations(
            validated_project_declarations, use_cache=False
        )
        # Do an outer merge to detect validated declarations removed from Hito
        declaration_list = declaration_list.merge(
            validated_declarations,
            how="outer",
            on=column_names["agent_id"],
            indicator=True,
            suffixes=[None, "_val"],
        )
        declaration_list["validated"] = (declaration_list._merge == "both") | (
            declaration_list._merge == "right_only"
        )
        declaration_list["hito_missing"] = declaration_list._merge == "right_only"
        hito_missing_num = len(declaration_list.loc[declaration_list["hito_missing"]])
        if hito_missing_num > 0:
            columns_fillna = {c: 0 for c in [*data_columns, "total_hours", "percent_global"]}
            declaration_list.loc[declaration_list["hito_missing"]] = declaration_list.fillna(
                value=columns_fillna
            )
            declaration_list.loc[
                declaration_list["hito_missing"], column_names["fullname"]
            ] = declaration_list[f"{column_names['fullname']}_val"]
            declaration_list.loc[
                declaration_list["hito_missing"], column_names["team"]
            ] = declaration_list[f"{column_names['team']}_val"]
            declaration_list.loc[declaration_list["hito_missing"], "suspect"] = True
            declaration_list.loc[declaration_list["hito_missing"], "validation_disabled"] = True
            declaration_list.sort_values(by=column_names["fullname"], inplace=True)
            hito_missing_msg = (
                f" dont {hito_missing_num} supprimé"
                f"{'s' if hito_missing_num > 1 else ''} de Hito"
            )
        else:
            hito_missing_msg = ""
        for category in data_columns:
            time_ok_column = f"{category}_time_ok"
            declaration_list.loc[declaration_list.validated, time_ok_column] = np.isclose(
                declaration_list.loc[declaration_list.validated, category],
                declaration_list.loc[declaration_list.validated, f"{category}_val"],
                rtol=1e-5,
                atol=0,
            )
    validated_number = len(declaration_list[declaration_list["validated"]])

    if declaration_set == VALIDATION_DECLARATIONS_SELECT_ALL:
        selected_declarations = declaration_list
    elif declaration_set == VALIDATION_DECLARATIONS_SELECT_VALIDATED:
        selected_declarations = declaration_list[declaration_list["validated"]]
    elif declaration_set == VALIDATION_DECLARATIONS_SELECT_NOT_VALIDATED:
        selected_declarations = declaration_list[~declaration_list["validated"]]
    else:
        return general_error_jumbotron(f"Invalid declaration set ID ({declaration_set})")

    columns = [*data_columns]
    columns.insert(0, column_names["fullname"])
    columns.append("percent_global")
    rows_number = len(selected_declarations)

    table_header = [
        html.Thead(
            html.Tr(
                [
                    *[
                        html.Th(
                            [
                                html.Div(
                                    [
                                        html.I(f"{global_params.column_titles[c]} "),
                                    ]
                                ),
                                html.Div(time_unit(c, english=False, parenthesis=True)),
                            ],
                            className="text-center",
                        )
                        for c in columns
                    ],
                    html.Th(TABLE_COLUMN_VALIDATION),
                ],
            )
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(
                            build_accordion(
                                i,
                                selected_declarations.iloc[i - 1][column_names["fullname"]],
                                agent_project_time(
                                    selected_declarations.iloc[i - 1][column_names["fullname"]]
                                ),
                                agent_tooltip_txt(selected_declarations.iloc[i - 1], data_columns),
                                "validated_hito_missing"
                                if selected_declarations.iloc[i - 1]["hito_missing"]
                                else "",
                            ),
                            className="accordion",
                            key=f"validation-table-cell-{i}-fullname",
                        ),
                        *[
                            activity_time_cell(selected_declarations.iloc[i - 1], c, i)
                            for c in data_columns
                        ],
                        activity_time_cell(selected_declarations.iloc[i - 1], "percent_global", i),
                        html.Td(
                            [
                                dbc.Checklist(
                                    options=[
                                        {
                                            "label": "",
                                            "value": 1,
                                            "disabled": selected_declarations.iloc[i - 1][
                                                "validation_disabled"
                                            ],
                                        }
                                    ],
                                    value=[
                                        int(
                                            selected_declarations.iloc[i - 1][
                                                column_names["agent_id"]
                                            ]
                                            in validation_data.index
                                        )
                                    ],
                                    id={"type": "validation-switch", "id": i},
                                    key=f"validation-switch-{i}",
                                    switch=True,
                                ),
                                # The dcc.Store is created to ease validation callback management
                                # by passing the agent ID and providing an Output object (but
                                # nothing will be written in it).
                                dcc.Store(
                                    id={"type": "validation-agent-id", "id": i},
                                    data=selected_declarations.iloc[i - 1][
                                        column_names["agent_id"]
                                    ],
                                ),
                            ],
                            className="align-middle",
                            key=f"validation-table-cell-{i}-switch",
                        ),
                    ],
                    key=f"validation-table-row-{i}",
                )
                for i in range(1, rows_number + 1)
            ]
        )
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Div(
                        html.B(
                            (
                                f"Nombre d'agents de l'équipe '{team}' ayant déclaré :"
                                f" {len(selected_declarations)} (agents validés={validated_number}"
                                f"{hito_missing_msg}"
                                f", déclarations validées/totales="
                                f"{validated_declarations_num}/{len(project_declarations)})"
                            ),
                            className="agent_count",
                        )
                    ),
                    html.Div(
                        html.Em(
                            (
                                f"Temps déclarés de l'équipe / total ="
                                f" {round(selected_declarations['percent_global'].mean(),1)}%"
                                f" (100%={SEMESTER_WEEKS} semaines)"
                            )
                        )
                    ),
                ]
            ),
            html.P(),
            add_validation_declaration_selection_switch(declaration_set),
            dbc.Table(
                table_header + table_body,
                id={"type": TABLE_TYPE_TABLE, "id": TABLE_ID_VALIDATION},
                bordered=True,
                hover=True,
                striped=True,
                class_name="sortable",
            ),
        ]
    )


def build_missing_agents_table(team, team_selection_date, period_date: str):
    """
    Function to build a table listing all agents that have not declared yet their time on projects

    :param team: selected team
    :param team_selection_date: last time the team selection was changed
    :param period_date: a date that must be inside the declaration period
    :return: missing agent page
    """
    global_params = GlobalParams()
    column_names = global_params.columns
    declaration_options = global_params.declaration_options

    declarations = get_team_projects(team, team_selection_date, period_date)

    agents = get_agents(period_date)

    if team == TEAM_LIST_ALL_AGENTS:
        agent_list = agents
    else:
        agent_list = agents[agents.team.notna() & agents[column_names["team"]].str.match(team)]

    if declarations is None:
        missing_agents = agent_list
    else:
        missing_agents = build_missing_agents(declarations, agent_list)

    rows_number = len(missing_agents)
    table_columns = ["fullname", "team"]

    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(
                        [
                            html.I(f"{global_params.column_titles[c]} "),
                        ]
                    )
                    for c in table_columns
                ],
            )
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(
                            missing_agents.iloc[i][column_names[c]],
                            className="align-middle",
                        )
                        for c in table_columns
                    ]
                )
                for i in range(rows_number)
            ]
        )
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Div(
                        html.B(
                            (
                                f"Nombre d'agents de l'équipe '{team}' sans déclaration :"
                                f" {len(missing_agents)}"
                            )
                        )
                    ),
                    html.Div(
                        html.Em(
                            (
                                f"Statuts non inclus :"
                                f" {', '.join(declaration_options['optional_statutes'])}"
                            )
                        )
                    ),
                    html.Div(
                        html.Em(
                            (
                                f"Equipes non incluses :"
                                f" {', '.join(declaration_options['optional_teams'])}"
                            )
                        )
                    ),
                ],
                class_name="agent_count",
            ),
            html.P(),
            dbc.Table(
                table_header + table_body,
                id={"type": TABLE_TYPE_TABLE, "id": TABLE_ID_MISSING_AGENTS},
                bordered=True,
                hover=True,
                striped=True,
                class_name="sortable",
            ),
        ]
    )


def build_statistics_table(team, team_selection_date, period_date: str):
    """
    Function to build a table listing the number of declarations and missing declarations per team

    :param team: selected team
    :param team_selection_date: last time the team selection was changed
    :param period_date: a date that must be inside the declaration period
    :return: missing agent page
    """
    global_params = GlobalParams()
    column_names = global_params.columns
    declaration_options = global_params.declaration_options

    try:
        session_data = global_params.get_session_data()
    except SessionDataMissing:
        return no_session_id_jumbotron()

    declarations = get_team_projects(team, team_selection_date, period_date)
    agents = get_agents(period_date)
    if team == TEAM_LIST_ALL_AGENTS:
        agent_list = agents
        # If the agent doesn't belong to a team, set team to an empty string rather than None
        agent_list.loc[agent_list.team.isna(), "team"] = ""
    else:
        agent_list = agents[agents.team.notna() & agents[column_names["team"]].str.match(team)]

    add_no_team_row = False
    if declarations is None:
        team_declarations = pd.DataFrame({"declarations_number": 0}, index=[team])
        team_declarations["missings_number"] = len(agent_list)
        missing_declarations = pd.DataFrame()
    else:
        team_agent_declarations = declarations.drop_duplicates(
            subset=[column_names["team"], column_names["fullname"]]
        )
        # If team is None, set it to empty string
        if len(team_agent_declarations.loc[team_agent_declarations.team.isna(), "team"]) > 0:
            team_agent_declarations.loc[team_agent_declarations.team.isna(), "team"] = ""
            add_no_team_row = True
        team_declarations = (
            team_agent_declarations[column_names["team"]]
            .value_counts()
            .to_frame(name="declarations_number")
        )

        missing_agents = build_missing_agents(declarations, agent_list)
        missing_declarations = (
            missing_agents[column_names["team"]].value_counts().to_frame(name="missings_number")
        )
        # If team is None, set it to empty string
        if len(missing_declarations.loc[missing_declarations.index == ""]) > 0:
            add_no_team_row = True

    team_list = pd.DataFrame(index=session_data.get_teams())
    if team == TEAM_LIST_ALL_AGENTS:
        team_list.drop(index=TEAM_LIST_ALL_AGENTS, inplace=True)
        if add_no_team_row:
            team_list = team_list.append(pd.DataFrame(index=[""]))
    else:
        team_list = team_list[team_list.index.str.match(team)]
    team_agents = agent_list[column_names["team"]].value_counts().to_frame(name="agents_number")
    team_declarations = pd.merge(
        team_declarations,
        team_list,
        how="outer",
        left_index=True,
        right_index=True,
        sort=True,
    ).fillna(0)
    team_declarations = pd.merge(team_declarations, team_agents, left_index=True, right_index=True)

    if len(missing_declarations):
        team_declarations = pd.merge(
            team_declarations,
            missing_declarations,
            how="outer",
            left_index=True,
            right_index=True,
            sort=True,
        ).fillna(0)
    else:
        team_declarations["missings_number"] = 0

    declarations_total = int(sum(team_declarations["declarations_number"]))
    missings_total = int(sum(team_declarations["missings_number"]))

    data_columns = ["declarations_number", "missings_number"]

    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(
                        [
                            html.I(f"{global_params.column_titles['team']} "),
                        ]
                    ),
                    *[
                        html.Th(
                            html.Div(
                                [
                                    html.I(f"{global_params.column_titles[c]} "),
                                ]
                            ),
                            className="text-center",
                        )
                        for c in data_columns
                    ],
                ],
            )
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(i),
                        *[
                            html.Td(
                                team_declarations.loc[i, column_names[c]],
                                className="text-center",
                            )
                            for c in data_columns
                        ],
                    ]
                )
                for i in team_declarations.index.values
            ]
        )
    ]

    return html.Div(
        [
            dbc.Alert(
                [
                    html.Div(
                        html.B(
                            (
                                f"Statistiques des déclarations pour l'équipe '{team}' :"
                                f" effectuées={declarations_total}, manquantes={missings_total}"
                            )
                        )
                    ),
                    html.Div(
                        html.Em(
                            (
                                f"Statuts non inclus dans les déclarations manquantes :"
                                f" {', '.join(declaration_options['optional_statutes'])}"
                            )
                        )
                    ),
                    html.Div(
                        html.Em(
                            (
                                f"Equipes non incluses dans les déclarations manquantes :"
                                f" {', '.join(declaration_options['optional_teams'])}"
                            )
                        )
                    ),
                ],
                class_name="agent_count",
            ),
            html.P(),
            dbc.Table(
                table_header + table_body,
                id={"type": TABLE_TYPE_TABLE, "id": TABLE_ID_DECLARATION_STATS},
                bordered=True,
                hover=True,
                striped=True,
                class_name="sortable",
            ),
        ]
    )


def build_missing_agents(declarations, agents, mandatory_only: bool = True):
    """
    Build the missing agents list and return it as a dataframe. It allows not toking into
    consideration the agent declarations for agents whose declaration is not mandatory
    (e.g. fellows).

    :param declarations: project declarations
    :param agents: list of agents who are supposed to do a declaration
    :param mandatory_only: ignore agents whose declaration is optional
    :return: missing agents dataframe
    """

    global_params = GlobalParams()
    column_names = global_params.columns

    declared_agents = pd.DataFrame(
        {column_names["agent_id"]: declarations[column_names["agent_id"]].unique()}
    )
    if mandatory_only:
        agent_list = agents[~agents.optional]
    else:
        agent_list = agents
    missing_agents = pd.merge(
        agent_list,
        declared_agents,
        on=column_names["agent_id"],
        how="outer",
        indicator=True,
    )
    missing_agents = missing_agents[missing_agents._merge == "left_only"].sort_values(
        by=column_names["fullname"]
    )

    return missing_agents


def activity_time_cell(row, column, row_index):
    """
    Build the cell content for an activity time, adding the appropriate class and in case of
    inconsistencies between the Hito declared time and the validated time, add a tooltip
    to display both values.

    :param row: declaration row
    :param column: column name for the cell to build
    :param row_index: row index of the current row
    :return: html.Td
    """

    global_params = GlobalParams()

    classes = "text-center align-middle"
    cell_value = int(round(row[column]))
    cell_id = f"validation-table-value-{row_index}-{column}"

    if column == "percent_global":
        thresholds = global_params.declaration_options["thresholds"]
        percent = round(row["percent_global"], 1)
        if percent <= thresholds["low"]:
            percent_class = "table-danger"
            tooltip_txt = f"Percentage low (<={thresholds['low']}%)"
        elif percent <= thresholds["suspect"]:
            percent_class = "table-warning"
            tooltip_txt = (
                f"Percentage suspect (>{thresholds['low']}% and" f" <={thresholds['suspect']}%)"
            )
        elif percent > thresholds["good"]:
            percent_class = "table-info"
            tooltip_txt = f"Percentage too high (>{thresholds['good']}%)"
        else:
            percent_class = "table-success"

        contents = [html.Div(percent, id=cell_id)]
        if percent_class != "table-success":
            contents.append(dbc.Tooltip(html.Div(tooltip_txt), target=cell_id))

        classes += f" {percent_class}"

    elif (
        (column != "enseignement" or not global_params.teaching_ratio)
        and time_unit(column) == TIME_UNIT_HOURS_EN
        and row[column] > global_params.declaration_options["max_hours"]
    ):
        contents = [
            html.Div(cell_value, id=cell_id),
            dbc.Tooltip(
                html.Div(
                    (
                        f"Déclaration supérieure au maximum"
                        f" ({global_params.declaration_options['max_hours']} heures)"
                    )
                ),
                target=cell_id,
            ),
        ]
        classes += " table-danger"

    elif row.hito_missing:
        validated_column = f"{column}_val"
        contents = [
            html.Div(int(round(row[validated_column])), id=cell_id),
            dbc.Tooltip(
                [
                    html.Div(f"Déclaration validée: {round(row[validated_column], 3)}"),
                    html.Div("Déclaration Hito correspondante supprimée"),
                ],
                target=cell_id,
            ),
        ]
        classes += " validated_hito_missing"

    elif row.validated and not row[f"{column}_time_ok"]:
        validated_column = f"{column}_val"
        contents = [
            html.Div(cell_value, id=cell_id),
            dbc.Tooltip(
                [
                    html.Div(f"Dernière déclaration: {round(row[column], 3)}"),
                    html.Div(f"Déclaration validée: {round(row[validated_column], 3)}"),
                ],
                target=cell_id,
            ),
        ]
        classes += " table-warning"

    else:
        contents = [html.Div(cell_value, id=cell_id)]
        if row.suspect:
            contents.append(
                dbc.Tooltip(
                    [
                        html.Div("Déclaration suspecte: vérifier les quotités déclarées"),
                    ],
                    target=cell_id,
                )
            )
            classes += " table-warning"

    return html.Td(contents, className=classes, key=f"validation-table-cell-{row}-{column}")


def agent_tooltip_txt(agent_data, data_columns):
    """
    Build the tooltip text associated with an agent.

    :param agent_data: the dataframe row corresponding to the agent
    :param data_columns: the list of columns to use to compute the total time
    :return: list of html elements
    """

    global_params = GlobalParams()

    if agent_data["hito_missing"]:
        tooltip_detail = "Déclarations validées supprimées de Hito"
    else:
        tooltip_detail = f"Total (semaines) : {total_time(agent_data, data_columns)}"
    tooltip_txt = [
        html.Div(
            f"{global_params.column_titles['team']}: {agent_data[global_params.columns['team']]}"
        ),
        html.Div(tooltip_detail),
    ]

    return tooltip_txt


def add_validation_declaration_selection_switch(current_set):
    """
    Add a dbc.RadioItems to select whether to show all declaration or only a subset.

    :param current_set: currently selected declaration set
    :return: dbc.RadioItems
    """

    return dbc.Row(
        [
            dbc.RadioItems(
                options=[
                    {
                        "label": "Toutes les déclarations",
                        "value": VALIDATION_DECLARATIONS_SELECT_ALL,
                    },
                    {
                        "label": "Déclarations non validées uniquement",
                        "value": VALIDATION_DECLARATIONS_SELECT_NOT_VALIDATED,
                    },
                    {
                        "label": "Déclarations validées uniquement",
                        "value": VALIDATION_DECLARATIONS_SELECT_VALIDATED,
                    },
                ],
                value=current_set,
                id=VALIDATION_DECLARATIONS_SWITCH_ID,
                inline=True,
            ),
        ],
        justify="center",
    )


def agent_list(dataframe: pd.DataFrame) -> pd.DataFrame:
    global_params = GlobalParams()
    fullname_df = pd.DataFrame()
    fullname_df[global_params.columns["fullname"]] = dataframe[
        global_params.columns["fullname"]
    ].drop_duplicates()
    return fullname_df


def total_time(row, categories, rounded=True) -> int:
    """
    Compute total time declared by an agent in weeks

    :param row: dataframe row for an agent
    :param categories: list of categories to sum up
    :param rounded: if true, returns the rounded value
    :return: number of weeks declared
    """

    global_params = GlobalParams()

    weeks_number = 0
    hours_number = 0
    for category in categories:
        if global_params.time_unit[category] == TIME_UNIT_WEEKS:
            weeks_number += row[category]
        elif global_params.time_unit[category] == TIME_UNIT_HOURS:
            hours_number += row[category]
        else:
            raise Exception(
                (
                    f"Unsupported time unit '{global_params.time_unit[category]}'"
                    f" for category {category}"
                )
            )

    weeks_number += hours_number / WEEK_HOURS

    if rounded:
        return int(round(weeks_number))
    else:
        return weeks_number


def category_time(dataframe, category) -> None:
    """
    Convert the number of hours into the time unit of the category. Keep track of the
    conversions done to prevent doing it twice.

    :param dataframe: dataframe to update
    :param category: category name
    :return: none, dataframe updated
    """

    global_params = GlobalParams()

    # Default time unit is hour
    unit_hour = True
    if category in global_params.time_unit:
        if global_params.time_unit[category] == TIME_UNIT_WEEKS:
            unit_hour = False
        elif global_params.time_unit[category] != TIME_UNIT_HOURS:
            raise Exception(
                (
                    f"Unsupported time unit '{global_params.time_unit[category]}'"
                    f" for category {category}"
                )
            )

    if not unit_hour:
        dataframe[category] = dataframe[category] / WEEK_HOURS

    return


def agent_project_time(agent: str) -> html.Div:
    """
    Return a HTML Div with the list of projects and the time spent on them

    :param agent: agent fullname
    :return: html.Div
    """

    global_params = GlobalParams()
    columns = global_params.columns

    try:
        session_data = global_params.get_session_data()
        df = session_data.project_declarations[
            session_data.project_declarations[global_params.columns["fullname"]] == agent
        ]

        return html.Div(
            [
                html.P(
                    (
                        f"{df.iloc[i][global_params.columns['activity']]}:"
                        f" {' '.join(project_time(df.iloc[i][columns['activity']], df.iloc[i][columns['hours']]))}"  # noqa: E501
                    )
                )
                for i in range(len(df))
            ]
        )

    except SessionDataMissing:
        return no_session_id_jumbotron()


def category_declarations(
    project_declarations: pd.DataFrame, use_cache: bool = True
) -> pd.DataFrame:
    """
    Process the project declarations (time per project) and convert it into declarations by
    category of projects.

    :param project_declarations: project declarations to consolidate
    :param use_cache: if True, use and update cache
    :return: dataframe
    """

    global_params = GlobalParams()
    columns = global_params.columns

    try:
        session_data = global_params.get_session_data()
    except SessionDataMissing:
        return no_session_id_jumbotron()

    # Check if there is a cached version
    if session_data.get_category_declarations() is not None and use_cache:
        return session_data.get_category_declarations()

    if project_declarations is not None:
        category_declarations = project_declarations.copy()
        categories = [CATEGORY_DEFAULT]
        categories.extend(global_params.project_categories.keys())
        for category in categories:
            category_declarations[category] = category_declarations.loc[
                category_declarations[columns["category"]] == category, columns["hours"]
            ]
        category_declarations.drop(columns=columns["hours"], inplace=True)
        category_declarations.fillna(0, inplace=True)

        agg_functions = {c: np.sum for c in categories}
        agg_functions["suspect"] = np.any
        category_declarations_pt = pd.pivot_table(
            category_declarations,
            index=[
                global_params.columns["fullname"],
                global_params.columns["team"],
                global_params.columns["agent_id"],
            ],
            values=[*categories, "suspect"],
            aggfunc=agg_functions,
        )
        category_declarations = pd.DataFrame(category_declarations_pt.to_records())

        category_declarations["total_hours"] = category_declarations[categories].sum(axis=1)
        category_declarations["percent_global"] = (
            category_declarations["total_hours"] / SEMESTER_HOURS * 100
        )

        # Convert category time into the appropriate unit
        for column_name in categories:
            category_time(category_declarations, column_name)

    else:
        raise Exception("Project declarations are not defined")

    if use_cache:
        session_data.set_category_declarations(category_declarations)

    return category_declarations


def get_validation_data(agent_id, period_date: str, session=None):
    """
    Return the validation data for an agent or None if there is no entry in the database for this
    agent_id.

    :param agent_id: agent_id of the agent to check
    :param session: DB session to use (default one if None)
    :param period_date: a date that must be inside the declaration period
    :return: an OSITAHValidation object or None
    """
    from utils.hito_db import OSITAHValidation, db

    if session is None:
        session = db.session

    validation_period = get_validation_period_data(period_date)
    return (
        session.query(OSITAHValidation)
        .filter_by(agent_id=agent_id, period_id=validation_period.id)
        .order_by(OSITAHValidation.timestamp.desc())
        .first()
    )


def get_validation_status(agent_id, period_date: str, session=None):
    """
    Return True if the agent entry has been validated, False otherwise (including if there is no
    validation entry for the agent)

    :param agent_id:  agent_id of the agent to check
    :param session: DB session to use
    :param period_date: a date that must be inside the declaration period
    :return: boolean
    """

    validation_data = get_validation_data(agent_id, period_date, session)
    if validation_data is None:
        return False
    else:
        return validation_data.validated


def get_all_validation_status(period_date: str):
    """
    Returns the list of agents whose declaration has been validated as a dataframe. It is intended
    to be used to build the validation table but should not be used when updating the status, as
    it may have been updated by somebody else.

    :param period_date: a date that must be inside the declaration period
    :return: dataframe
    """

    from utils.hito_db import OSITAHValidation, db

    validation_period = get_validation_period_data(period_date)
    # By design, only one entry in the declaration period can be with the status validated,
    # except if the database has been messed up...
    validation_query = OSITAHValidation.query.filter(
        OSITAHValidation.period_id == validation_period.id,
        OSITAHValidation.validated,
    )
    validation_data = pd.read_sql(validation_query.statement, con=db.engine)
    if validation_data is None:
        validation_data = pd.DataFrame()
    else:
        validation_data.set_index("agent_id", inplace=True)

    return validation_data


def validation_started(period_date: str):
    """
    Compare the current date with the validation start date (validation_date) and return True
    if the validation has started, False otherwise.

    :param period_date: date included in the declaration period
    :return: boolean
    """

    current_date = datetime.now()
    period_params = get_validation_period_data(period_date)
    if current_date >= period_params.validation_date:
        return True
    else:
        return False


def project_declaration_snapshot(
    agent_id,
    validation_id,
    team,
    team_selection_date,
    period_date,
    db_session=None,
    commit=False,
):
    """
    Save into table ositah_validation_project_declaration the validated project declarations
    for an agent.

    :param agent_id: agent (ID) whose project declarations must be saved
    :param validation_id: validation ID associated with the declarations snapshot
    :param db_session: session for the current transaction. If None, use the default one.
    :param commit: if false, do not commit added rows
    :return: None
    """

    from utils.hito_db import OSITAHProjectDeclaration, db

    global_params = GlobalParams()
    columns = global_params.columns
    try:
        session_data = global_params.get_session_data()
    except SessionDataMissing:
        return no_session_id_jumbotron()

    if db_session:
        session = db_session
    else:
        session = db.session

    # The cache cannot be used directly as the callback may run on a server where the session
    # cache for the current user doesn't exist yet
    project_declarations = get_team_projects(
        team, team_selection_date, period_date, DATA_SOURCE_HITO
    )
    agent_projects = project_declarations[project_declarations[columns["agent_id"]] == agent_id]
    if agent_projects is None:
        print(f"ERROR: no declaration found for agent ID '{agent_id}' (internal error)")
    else:
        for _, project in agent_projects.iterrows():
            declaration = OSITAHProjectDeclaration(
                projet=project[columns["project"]],
                masterprojet=project[columns["masterproject"]],
                category=project[columns["category"]],
                hours=project[columns["hours"]],
                quotite=project[columns["quotite"]],
                validation_id=validation_id,
                hito_project_id=project[columns["activity_id"]],
            )
            try:
                session.add(declaration)
            except Exception:
                # If the default session is used, let the caller process the exception and
                # eventually do the rollback
                if db_session:
                    session.rollback()
                raise

        # Reset the cache of validated declarations if a modification occured
        session_data.reset_validated_declarations_cache()

        if commit:
            session.commit


def validation_submenus():
    """
    Build the tabs menus of the validation subapplication

    :return: DBC Tabs
    """

    return dbc.Tabs(
        [
            dbc.Tab(
                id=TAB_ID_DECLARATION_STATS,
                tab_id=TAB_ID_DECLARATION_STATS,
                label="Statistiques",
            ),
            dbc.Tab(
                id=TAB_ID_VALIDATION,
                tab_id=TAB_ID_VALIDATION,
                label="Déclarations Effectuées",
            ),
            dbc.Tab(
                id=TAB_ID_MISSING_AGENTS,
                tab_id=TAB_ID_MISSING_AGENTS,
                label="Déclarations Manquantes",
            ),
        ],
        id=VALIDATION_TAB_MENU_ID,
    )


def validation_layout():
    """
    Build the layout for this application, after reading the data if necessary.

    :return: application layout
    """

    from utils.hito_db import OSITAHProjectDeclaration, OSITAHValidation, OSITAHValidationPeriod, db

    OSITAHValidationPeriod.__table__.create(db.session.bind, checkfirst=True)
    OSITAHValidation.__table__.create(db.session.bind, checkfirst=True)
    OSITAHProjectDeclaration.__table__.create(db.session.bind, checkfirst=True)

    return html.Div(
        [
            html.H1("Affichage et validation des déclarations"),
            team_list_dropdown(),
            dcc.Store(id=DATA_SELECTED_SOURCE_ID, data=DATA_SOURCE_HITO),
            html.Div(
                validation_submenus(),
                id="validation-submenus",
                style={"margin-top": "3em"},
            ),
            dcc.Store(id=VALIDATION_LOAD_INDICATOR_ID, data=0),
            dcc.Store(id=VALIDATION_SAVED_INDICATOR_ID, data=0),
            dcc.Store(
                id=VALIDATION_DECLARATIONS_SELECTED_ID,
                data=VALIDATION_DECLARATIONS_SELECT_ALL,
            ),
            dcc.Store(id=VALIDATION_SAVED_ACTIVE_TAB_ID, data=""),
            # The following dcc.Store coupled with tables must be created in the layout for
            # the callback to work
            dcc.Store(id={"type": TABLE_TYPE_DUMMY_STORE, "id": TABLE_ID_VALIDATION}, data=0),
            dcc.Store(
                id={"type": TABLE_TYPE_DUMMY_STORE, "id": TABLE_ID_MISSING_AGENTS},
                data=0,
            ),
            dcc.Store(
                id={"type": TABLE_TYPE_DUMMY_STORE, "id": TABLE_ID_DECLARATION_STATS},
                data=0,
            ),
        ]
    )


@app.callback(
    [
        Output(TAB_ID_DECLARATION_STATS, "children"),
        Output(TAB_ID_VALIDATION, "children"),
        Output(TAB_ID_MISSING_AGENTS, "children"),
        Output(VALIDATION_SAVED_INDICATOR_ID, "data"),
        Output(VALIDATION_SAVED_ACTIVE_TAB_ID, "data"),
    ],
    [
        Input(VALIDATION_LOAD_INDICATOR_ID, "data"),
        Input(VALIDATION_TAB_MENU_ID, "active_tab"),
        Input(TEAM_SELECTED_VALUE_ID, "data"),
        Input(VALIDATION_DECLARATIONS_SELECTED_ID, "data"),
    ],
    [
        State(TEAM_SELECTION_DATE_ID, "data"),
        State(VALIDATION_SAVED_INDICATOR_ID, "data"),
        State(VALIDATION_PERIOD_SELECTED_ID, "data"),
        State(VALIDATION_SAVED_ACTIVE_TAB_ID, "data"),
    ],
    prevent_initial_call=True,
)
def display_validation_tables(
    load_in_progress,
    active_tab: str,
    team: str,
    declaration_set: int,
    team_selection_date,
    previous_load_in_progress,
    period_date: str,
    previous_active_tab: str,
):
    """
    Display active tab contents after a team or an active tab change. Exact action depends on
    the value of the load in progress indicator. If it is equal to the previous value, it means
    this is the start of the update process: progress bar is displayed and a dcc.Interval is
    created to schedule again this callback after incrementing the load in progress indicator.
    This causes the callback to be reentered and this time it triggers the real processing for
    the tab resulting in the final update of the active tab contents. An empty content is
    returned for inactive tabs.

    :param load_in_progress: load in progress indicator
    :param tab: select tab name
    :param team: selected team
    :param declaration_set: selected declaration set (all, validated or non-validated ones)
    :param team_selection_date: last time the team selection was changed
    :param previous_load_in_progress: previous value of the load_in_progress indicator
    :param period_date: a date that must be inside the declaration period
    :param previous_active_tab: previously active tab
    :return: tab content (empty if the tab is not active)
    """

    tab_contents = []

    # Be sure to fill the return values in the same order as Output are declared
    tab_list = [TAB_ID_DECLARATION_STATS, TAB_ID_VALIDATION, TAB_ID_MISSING_AGENTS]
    for tab in tab_list:
        if team and len(team) > 0 and tab == active_tab:
            if load_in_progress > previous_load_in_progress and active_tab == previous_active_tab:
                if active_tab == TAB_ID_DECLARATION_STATS:
                    tab_contents.append(
                        build_statistics_table(team, team_selection_date, period_date)
                    )
                elif active_tab == TAB_ID_VALIDATION:
                    tab_contents.append(
                        build_validation_table(
                            team, team_selection_date, declaration_set, period_date
                        )
                    )
                elif active_tab == TAB_ID_MISSING_AGENTS:
                    tab_contents.append(
                        build_missing_agents_table(team, team_selection_date, period_date)
                    )
                else:
                    tab_contents.append(
                        dbc.Alert("Erreur interne: tab non supporté"), color="warning"
                    )
                previous_load_in_progress += 1
            else:
                component = html.Div(
                    [
                        create_progress_bar(team),
                        dcc.Interval(
                            id=VALIDATION_DISPLAY_INTERVAL_ID,
                            n_intervals=0,
                            max_intervals=1,
                            interval=500,
                        ),
                    ]
                )
                tab_contents.append(component)
        else:
            tab_contents.append("")

    tab_contents.extend([previous_load_in_progress, active_tab])

    return tab_contents


@app.callback(
    Output(VALIDATION_LOAD_INDICATOR_ID, "data"),
    Input(VALIDATION_DISPLAY_INTERVAL_ID, "n_intervals"),
    State(VALIDATION_SAVED_INDICATOR_ID, "data"),
    prevent_initial_call=True,
)
def display_validation_tables_trigger(n, previous_load_indicator):
    """
    Increment (change) of the input of display_validation_tables callback to get it fired a
    second time after displaying the progress bar. The output component must be updated each
    time the callback is entered to trigger the execution of the other callback, thus the
    choice of incrementing it at each call.

    :param n: n_interval property of the dcc.Interval (0 or 1)
    :return: 1 increment to previous value
    """

    return previous_load_indicator + 1


@app.callback(
    Output({"type": "validation-switch", "id": MATCH}, "value"),
    Input({"type": "validation-switch", "id": MATCH}, "value"),
    State({"type": "validation-agent-id", "id": MATCH}, "data"),
    State(TEAM_SELECTED_VALUE_ID, "data"),
    State(TEAM_SELECTION_DATE_ID, "data"),
    State(VALIDATION_PERIOD_SELECTED_ID, "data"),
    prevent_initial_call=True,
)
def validation_button_callback(value, agent_id, team, team_selection_date, period_date: str):
    """
    Function called as a callback for the validation button. It adds a validation entry for
    the selected agent with a timestamp allowing to get the validation history. Doesn't add an
    entry if the validation status is unchanged (should not happen).

    :param value: a list with of values with last one equals 1 if the switch is on, an empty
                  list or a list with 1 value (0) if the switch is off
    :param agent_id: the agent ID of the selected agent
    :param team: selected team
    :param team_selection_date: last time the team selection was changed
    :param period_date: a date that must be inside the declaration period
    :return: None
    """

    from utils.hito_db import OSITAHValidation, db

    session = db.session

    validation_data = get_validation_data(agent_id, period_date, session)

    # If the validation switch is on, add a new validation entry for the agent (except if there
    # is an existing validated entry but it should not happen) and save the associated project
    # declarations. If the switch is off and a validated entry exists, update the "validated"
    # attribute to false and do not add a new project declarations.
    switch_on = len(value) > 0 and value[len(value) - 1] > 0
    if switch_on:
        if validation_data is None or validation_data.validated != switch_on:
            validation_id = str(uuid4())
            validation_data = OSITAHValidation(
                id=validation_id,
                validated=switch_on,
                timestamp=datetime.now(),
                agent_id=agent_id,
                period_id=get_validation_period_id(period_date),
            )
            try:
                session.add(validation_data)
                # A flush() is required before calling project_declaration_snapshot() else the
                # first insert is lost
                session.flush()
                project_declaration_snapshot(
                    agent_id,
                    validation_id,
                    team,
                    team_selection_date,
                    period_date,
                    session,
                )
                session.commit()
            except:  # noqa: E722
                session.rollback()
                raise

    elif validation_data.validated:
        validation_data.validated = switch_on
        # Keep track of the original timestamp
        validation_data.initial_timestamp = validation_data.timestamp
        validation_data.timestamp = datetime.now()
        session.commit()

    return value


@app.callback(
    Output(VALIDATION_DECLARATIONS_SELECTED_ID, "data"),
    Input(VALIDATION_DECLARATIONS_SWITCH_ID, "value"),
    prevent_initial_call=True,
)
def select_declarations_set(new_set):
    """
    This callback is used to forward to the validation table callback the selected declarations
    set through a dcc.Store that exists permanently in the page.

    :param new_set: selected declarations set
    :return: same value
    """

    return new_set
