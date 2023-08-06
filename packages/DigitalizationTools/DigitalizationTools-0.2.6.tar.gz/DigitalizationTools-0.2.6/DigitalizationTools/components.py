import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from typing import Optional, Union
import pandas as pd

card_style = {'width':"100%", 'textAlign':'center'}

menu_font1 = {"color":"#FFFFFF", "fontWeight":"bold", 'font-size':'20px'}
menu_font2 = {"color":"#FFFFFF", 'font-size':'16px'}

card_title = {"color":"#080808", "fontWeight":"bold", 'font-size':'20px'}

left_column_style = {'margin-left': '0.0em','margin-right': '0.0em',}

notification_style = {"position": "fixed", "top": 30, "right": 10, "width": 350}

html_section_style = {"color":"#110ecc", 'textAlign':'center', "fontWeight":"bold", 
                    'font-size':'20px', 'margin-top': '1em', 'margin-bottom': '1em'}

input_style  = {'width':"100%", 'textAlign':'center'}

button_style0 = {'width':'100%', 'margin-bottom': '0.5em', 
                 'margin-top': '0.5em'}
radio_style = {'width':'100%', 'textAlign':'right', 'margin-top':'8px'}

dbc_color = {"blue": "primary", "grey": "secondary", "green": "success", "orange": "warning", 
            "red": "danger", "light blue": "info", "white": "light", "black": "dark"}


# define multiple rows
def rows(rowContents:list):
    '''
    rowContents: list of dash components
    '''
    layout = dbc.Row(children=rowContents, style=left_column_style)
    return layout

# define multiple columns
def row_with_columns(columnContents:list, columnWidth:list):
    '''
    columnWidth: list of int (max. sum = 12)
    columnContents: list of dash components
    '''
    colInfo = []
    columnNumbers = len(columnContents)
    for i in range(columnNumbers):
        colInfo.append(dbc.Col(columnContents[i], width=columnWidth[i]))

    layout = dbc.Row(children=colInfo)  
    return layout


def button(buttonName:str, buttonID:str, buttonColor:str, outline:Optional[bool]=False):
    botton_layout = dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Button(
                                    buttonName, 
                                    id=buttonID, 
                                    n_clicks=0,
                                    outline=outline,
                                    color=dbc_color[buttonColor], 
                                    style=button_style0
                                ), 
                            width=12),
                        ], 
                    style=left_column_style)
    return botton_layout



def label_input_text(labelName:str, labelWidth:int, inputWidth:int, inputID:str,
                    defaultInputValue:Optional[str]=None):
    return dbc.Row(children=[
            dbc.Label(labelName, width=labelWidth),
            dbc.Col(
                dbc.Input(
                    type="text", 
                    id=inputID, 
                    value=defaultInputValue, 
                    style=card_style
                ), 
            width=inputWidth)
        ], style=left_column_style)



def label_input_number(labelName:str, labelWidth:int, inputWidth:int, inputID:str,
                    miniValue:Optional[Union[float, int]]=None, 
                    maxValue:Optional[Union[float, int]]=None,
                    stepValue:Optional[Union[float, int]]=0.001,
                    defaultInputValue:Optional[Union[float, int]]=None):
    return dbc.Row(children=[
            dbc.Label(labelName, width=labelWidth),
            dbc.Col(
                dbc.Input(
                    type="number", 
                    id=inputID, 
                    value=defaultInputValue,
                    min=miniValue,
                    max=maxValue,
                    step=stepValue,
                    style=card_style
                ), 
            width=inputWidth)
        ], style=left_column_style)


def label_Textarea(labelName:str, inputID:str, defaultInputValue:Optional[str]=None):

    layout = dbc.Row(children=[
                dbc.Label(labelName, width=12),
                dbc.Col(dbc.Textarea(id=inputID), width=12, ),
            ], style=left_column_style)
    return layout




def card(cardHeader: str, content: list ):
    content_layout = []
    for i in content:
        content_layout.append(i)
    return dbc.Card([
                dbc.CardHeader(cardHeader, 
                    style={'font-weight': 'bold', 
                    'font-size':'20px'}),
                dbc.CardBody(content_layout),
            ], )


def table(columnName:list, columnType:list, tableID:str, 
        editable:Optional[bool]=True,
        row_deletable:Optional[bool]=True, 
        row_selectable:Optional[Union[str, bool]]=False, 
        data:Optional[list]=[], 
        hideColumn:Optional[list]=[],
        heightTable:Optional[Union[str, int]]="auto",
        dropdownContent:Optional[dict]={}):
    '''
    columnName = ["class", "age", "id"]
    columnType = ["text", "numeric", "text"]
    dropdownName = ["class"]
    dropdownContent = 
        {}: no dropdown
        {'class': ["A", "B", "C"]}: with known dropdown 
        {'class': []}: without known dropdown
    data: [["A", "B", "C"], [23, 22, 25]]
    hideColumn: ["id"]
    '''
    
    # define dropdown cell and column names
    if dropdownContent == {}: # if dropdownContent is not defined
        dropdown = {}
        # define columns without dropdown
        columns = []
        for i in range(len(columnName)):
            columns.append({'id':columnName[i],'name':columnName[i], 'type': columnType[i]})
    else: # dropdownContent is defined
        dropdownName = list(dropdownContent.keys())

        # check if name in dropdownContent is defined in columnName
        for i in range(len(dropdownName)):
            if dropdownName[i] not in columnName:
                return "dropdown colume name is not defined correctly."

        # define dropdown
        dropdown = {}
        for i in range(len(dropdownName)):
            if dropdownContent[dropdownName[i]] == []:
                dropdown[dropdownName[i]] = {'options': []} 
            else:
                dropdown[dropdownName[i]] = {'options': [{'label': i, 'value': i} for i in set(dropdownContent[dropdownName[i]])]} 
        
        # define columns with dropdown
        columns = []
        for i in range(len(columnName)):
            if columnName[i] in dropdownName:
                columns.append({'id':columnName[i],'name':columnName[i], 'type': columnType[i], 'presentation': 'dropdown'}) # 'presentation': 'dropdown'
            else:
                columns.append({'id':columnName[i],'name':columnName[i], 'type': columnType[i]})
        
    # define conditional styles
    hide_conditional = []
    for hide in hideColumn:
        if hide in columnName:
            hide_conditional.append({'if':{'column_id': hide,},'display':'None',})
    
    style_cell_conditional = hide_conditional
    for c in range(len(columns)):
        style_cell_conditional.append({'if': {'column_id': columns[c]["id"]}, 'textAlign': 'left'} )
    
    style_data_conditional = [{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(240,255,255)'}]

    # define data
    if data == []:
        data_tuple = None
    else:
        dicty = {}
        length_data = len(data)
        max_rows = max([len(data[i]) for i in range(length_data)])
        for i in range(length_data):
            if data[i] == []:
                dicty[columnName[i]] = ['' for _ in range(max_rows)]
            else:
                dicty[columnName[i]] = data[i]
        data_tuple = pd.DataFrame(dicty).to_dict('records')

    # define table height
    if type(heightTable) == int:
        height = f"{heightTable}px"
    else:
        height = heightTable

    table_layout =  dash_table.DataTable(
                        id=tableID,
                        data= data_tuple,
                        sort_action='native',
                        filter_action='native',
                        editable=editable,
                        row_deletable=row_deletable,
                        row_selectable=row_selectable,
                        columns=columns,
                        css = [{"selector":".dropdown", "rule": "position: static"}],
                        style_cell_conditional= style_cell_conditional,
                        style_data_conditional= style_data_conditional,
                        style_header_conditional= hide_conditional,
                        style_header={
                            'backgroundColor': 'rgb(192,192,192)',
                            'fontWeight': 'bold',
                            'font-size': '15px',
                        },
                        style_cell={
                            'font-size': '13px',
                            'minWidth': 95, 
                            # 'maxWidth': 95, 
                            # 'width': 95
                        },
                        style_table={
                            'overflowY': 'auto',
                            'overflowX': 'auto',
                            'margin-top': '0.5em',
                            'padding-bottom': '0.5em',
                            'height': height,
                        },
                        dropdown=dropdown,
                    )
    return table_layout


def dropdownMenu(dropdownName:str, dropdownID:str, labelWidth:int, dropdownWidth:int,
                options:Optional[list]=[]):
    dropdown_layout = dbc.Row(children=[
                            dbc.Label(dropdownName, width=labelWidth),
                            dbc.Col(dcc.Dropdown(id=dropdownID, options=options, value=None, 
                                    optionHeight=50, style=card_style), width=dropdownWidth),
                        ], style=left_column_style)
    return dropdown_layout


def upload(uploadID:str):
    upload_field = dbc.Row(children=[
                    dcc.Upload(id=uploadID,
                        children=html.Div(['Drag and drop or select a ',
                                            html.A('file')]),
                        style={'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '1px',
                                'margin-bottom': '15px', },
                        multiple=False, )
                    ], style=left_column_style)
    
    return upload_field


def notification(noticeText:str, headerText:str, iconType:str, duration:int, dismissable:bool):
    notice = dbc.Toast(noticeText, header=headerText, icon=iconType, duration=duration, dismissable=dismissable, style=notification_style,)
    return notice


def spinner(htmlID:str):
    spinner_layout = dbc.Row(children=[
                        dbc.Spinner(html.Div(id=htmlID))
                    ], style=left_column_style)
    return spinner_layout


def multi_tabs(tabLayout:list, labelList:list):
    tabs = [dcc.Tab(tabLayout[i], label=labelList[i]) for i in range(len(labelList))]
    layout = html.Div([dcc.Tabs(tabs)])
    return layout

def radio_select(radioLabel:str, radioID:str, radioItemsLabel:list, radioItemsValue:list,  labelWidth:int, radioWidth:int):
    options = []
    for i in range(len(radioItemsValue)):
        options.append({'label': radioItemsLabel[i], 'value': radioItemsValue[i]})

    layout = dbc.Row(children=[
                dbc.Label(radioLabel, width=labelWidth),
                dbc.Col(dbc.RadioItems(
                            options=options,
                            value=radioItemsValue[0],
                            id=radioID,
                            labelCheckedStyle={
                                'color': 'green',
                                'width': '100%'
                            },
                            inline=True,
                            style=radio_style,
                            ), width=radioWidth,),
            ], style=left_column_style)
    return layout


def insert_image(app, imgLocation:str, height:int):
    layout  =   dbc.Row(
                    children=[
                        html.Img(
                            src=app.get_asset_url(imgLocation), 
                            style={'height': f'{height}px', 'object-fit': 'scale-down', 'Align': 'center'}),
                    ]
                )
    return layout

def app_layout(contents:list, navigationBarColor:Optional[str]="green"):

    """
    app includes two rows: 1. navigation header, 2. contents of different pages
    """
    children_contents = []
    for i in contents:
        children_contents.append(i)

    layout = html.Div(children=[
                # Menu
                dbc.Row(children=[
                    dbc.Navbar([
                        dbc.Row(
                            children=children_contents, align="center")
                    ], color=dbc_color[navigationBarColor],),
                ], style=left_column_style), 
                
                # pages
                dbc.Row(children=[
                    dcc.Location(id='url'), 
                    html.Div(id='content')
                ], style=left_column_style)
            ], style=left_column_style)
    return layout


def navigationImage(imageLocation:str, imageHeight:Optional[str]="65px"):
    layout = dbc.Col(
                html.Img(src=imageLocation, height=imageHeight, style={"margin-left":"20px"}), 
            width="auto")
    return layout

def navigationBrand(brandName:Optional[str]=""):
    layout = dbc.Col(dbc.NavbarBrand(brandName, className="ml-2", style=menu_font1), width="auto")
    return layout

def navigationLink(linkName:str, hrefName:str):
    layout = dbc.Col(dbc.NavLink(linkName,  href=hrefName, active="exact", style=menu_font2), width="auto")
    return layout


def navigationDropdownMedu(menuName:str, menuItemName:list, menuItemHref:list, menuColor:Optional[str]="green"):
    menuItems = []
    for i in range(len(menuItemName)):
        menuItems.append(dbc.DropdownMenuItem(menuItemName[i], href=menuItemHref[i]))
        
    layout = dbc.Col(
                dbc.DropdownMenu(
                    menuItems, 
                    label=menuName, 
                    color=dbc_color[menuColor], 
                    style=menu_font2
                ),
            width="auto")
    return layout