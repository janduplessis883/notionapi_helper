import streamlit as st
import json
import streamlit_shadcn_ui as ui

PROPERTY_TYPES = {
    "Title": "title",
    "Rich Text": "rich_text",
    "Number": "number",
    "Select": "select",
    "Multi-select": "multi_select",
    "Date": "date",
    "Checkbox": "checkbox",
    "URL": "url",
    "Email": "email",
    "Phone Number": "phone_number",
    "Files": "files",
    "People": "people",
    "Status": "status",
    "Formula": "formula",
    "Relation": "relation",
    "Rollup": "rollup",
    "Unique ID": "unique_id",
    "Created By": "created_by",
    "Created Time": "created_time",
    "Last Edited By": "last_edited_by",
    "Last Edited Time": "last_edited_time",
    "Button": "button",
    "Location": "location",
    "Verification": "verification",
    "Last Visited Time": "last_visited_time",
    "Place": "place",
}

EMPTY_SCHEMA_TYPES = {
    "title",
    "rich_text",
    "date",
    "checkbox",
    "url",
    "email",
    "phone_number",
    "files",
    "people",
    "created_by",
    "created_time",
    "last_edited_by",
    "last_edited_time",
    "button",
    "location",
    "verification",
    "last_visited_time",
    "place",
}

NUMBER_FORMATS = [
    "number", "number_with_commas", "percent", "dollar", "euro", "pound", "yen",
    "yuan", "won", "ruble", "rupee", "franc", "real", "lira", "krona",
    "ringgit", "baht", "rupiah", "peso", "rand", "new_zealand_dollar",
    "danish_krone", "norwegian_krone", "swedish_krona", "singapore_dollar",
    "hong_kong_dollar", "australian_dollar", "canadian_dollar",
]

NOTION_COLORS = [
    "default", "gray", "brown", "orange", "yellow", "green", "blue",
    "purple", "pink", "red",
]

STATUS_GROUPS = ["To-do", "In progress", "Complete"]

ROLLUP_FUNCTIONS = [
    "average", "checked", "count", "count_values", "date_range",
    "earliest_date", "empty", "latest_date", "max", "median", "min",
    "not_empty", "percent_checked", "percent_empty", "percent_not_empty",
    "percent_unchecked", "range", "show_original", "show_unique", "sum",
    "unchecked", "unique",
]


def parse_options(raw_options, include_status_groups=False):
    options = []
    for raw_option in raw_options.splitlines():
        parts = [part.strip() for part in raw_option.split("|")]
        name = parts[0] if parts else ""
        if not name:
            continue

        option = {"name": name}
        if len(parts) > 1 and parts[1] in NOTION_COLORS:
            option["color"] = parts[1]
        if include_status_groups and len(parts) > 2 and parts[2] in STATUS_GROUPS:
            option["group"] = parts[2]
        options.append(option)
    return options


def build_property_schema(prop_type, idx):
    notion_type = PROPERTY_TYPES[prop_type]

    if notion_type in EMPTY_SCHEMA_TYPES:
        return {notion_type: {}}

    if notion_type == "number":
        number_format = st.session_state.get(f"number_format_{idx}", "number")
        return {"number": {"format": number_format}}

    if notion_type in {"select", "multi_select"}:
        options = parse_options(st.session_state.get(f"{notion_type}_options_{idx}", ""))
        return {notion_type: {"options": options} if options else {}}

    if notion_type == "status":
        options = parse_options(st.session_state.get(f"status_options_{idx}", ""), include_status_groups=True)
        return {"status": {"options": options} if options else {}}

    if notion_type == "formula":
        expression = st.session_state.get(f"formula_expression_{idx}", "").strip()
        return {"formula": {"expression": expression} if expression else {}}

    if notion_type == "relation":
        data_source_id = st.session_state.get(f"relation_data_source_id_{idx}", "").strip()
        if data_source_id:
            return {"relation": {"data_source_id": data_source_id}}
        return {"relation": {}}

    if notion_type == "rollup":
        rollup = {}
        for field in [
            "relation_property_name",
            "relation_property_id",
            "rollup_property_name",
            "rollup_property_id",
        ]:
            value = st.session_state.get(f"rollup_{field}_{idx}", "").strip()
            if value:
                rollup[field] = value
        rollup["function"] = st.session_state.get(f"rollup_function_{idx}", "count")
        return {"rollup": rollup}

    if notion_type == "unique_id":
        prefix = st.session_state.get(f"unique_id_prefix_{idx}", "").strip()
        return {"unique_id": {"prefix": prefix} if prefix else {}}

    return {notion_type: {}}
st.set_page_config(
    page_title="Notion API - JSON Builder",
    page_icon=":orange_heart:"
)

st.image("title.png")
st.logo('icon.png')

pages = ui.tabs(
    options=[
        "About",
        "Configure Database Properties",
        "Construct Notion Blocks",
    ],
    default_value="About",
    key="mainnav",
)

if pages == "About":
    st.header(":material/info: About")
    st.write("Welcome to the **Notion API JSON Builder!**")
    st.write("This humble little app is here to help you tackle one of the trickiest parts of working with the Notion API—constructing complex JSON structures. Whether you’re configuring properties for your Notion databases or building dynamic blocks to append to your pages, this app simplifies the process.")
    st.write("With a user-friendly interface, you can easily set up properties like titles, text, numbers, and more, or generate blocks like headings, lists, and to-dos. No more guesswork when building JSON for Notion!")
    st.write("Our goal is to make your life easier when working with Notion, whether you’re creating dynamic dashboards or detailed documents. If you’re juggling database properties or adding rich blocks of content, this app will save you time and energy.")
    st.write("Give it a try, and happy building!")



elif pages == "Configure Database Properties":

    st.header(":material/check_box: Configure Database Properties")
    st.caption(
        "Build the `properties` object for a Notion data source or database schema. "
        "Page values belong in the `properties` object when creating pages, not here. "
        "Notion's latest documented API version is `2026-03-11`."
    )

    # Initialize property list in session state
    if 'property_list' not in st.session_state:
        st.session_state['property_list'] = []

    # Button to add a new property
    st.sidebar.subheader(("Database Properties"))
    st.sidebar.caption("Add and configure properties for your Notion database. JSON is updated every time you press 'Add Property'")
    if st.sidebar.button("Add Property", type="primary"):
        st.session_state['property_list'].append({'type': None, 'name': None})

    # Display property inputs
    if st.session_state['property_list']:
        for idx, prop in enumerate(st.session_state['property_list']):
            st.subheader(f"Property {idx + 1}")
            prop_type_key = f"prop_type_{idx}"
            prop_name_key = f"prop_name_{idx}"

            # Select property type
            prop_type = st.selectbox("Select property type", list(PROPERTY_TYPES.keys()), key=prop_type_key)
            prop_name = st.text_input(f"Enter the property name for {prop_type}", key=prop_name_key)

            # Based on property type, display appropriate inputs
            notion_type = PROPERTY_TYPES[prop_type]
            if notion_type in EMPTY_SCHEMA_TYPES:
                st.caption("No schema configuration is required for this property type.")
            elif prop_type == 'Number':
                st.selectbox("Number format", NUMBER_FORMATS, key=f"number_format_{idx}")
            elif prop_type in {'Select', 'Multi-select'}:
                st.text_area(
                    "Options (one per line, optionally `Name | color`)",
                    key=f"{notion_type}_options_{idx}",
                    placeholder="Priority | red\nWaiting | yellow\nDone | green",
                )
            elif prop_type == 'Status':
                st.text_area(
                    "Status options (one per line, optionally `Name | color | group`)",
                    key=f"status_options_{idx}",
                    placeholder="Not started | gray | To-do\nIn review | yellow | In progress\nDone | green | Complete",
                )
            elif prop_type == 'Formula':
                st.text_input(
                    "Formula expression",
                    key=f"formula_expression_{idx}",
                    placeholder='prop("Price") * prop("Quantity")',
                )
            elif prop_type == 'Relation':
                st.text_input(
                    "Related data source ID",
                    key=f"relation_data_source_id_{idx}",
                    placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                )
            elif prop_type == 'Rollup':
                st.text_input("Relation property name", key=f"rollup_relation_property_name_{idx}")
                st.text_input("Relation property ID", key=f"rollup_relation_property_id_{idx}")
                st.text_input("Rollup property name", key=f"rollup_rollup_property_name_{idx}")
                st.text_input("Rollup property ID", key=f"rollup_rollup_property_id_{idx}")
                st.selectbox("Rollup function", ROLLUP_FUNCTIONS, key=f"rollup_function_{idx}")
            elif prop_type == 'Unique ID':
                st.text_input("Prefix", key=f"unique_id_prefix_{idx}", placeholder="TASK")

    # Generate the properties JSON automatically
    properties_json = {}
    for idx, prop in enumerate(st.session_state['property_list']):
        prop_type_key = f"prop_type_{idx}"
        prop_name_key = f"prop_name_{idx}"
        prop_type = st.session_state.get(prop_type_key)
        prop_name = st.session_state.get(prop_name_key)

        if prop_name and prop_type:
            properties_json[prop_name] = build_property_schema(prop_type, idx)
    st.divider()
    st.subheader(":material/code_blocks: Generated Properties JSON")
    with st.container(height=300, border=True):
        st.json(properties_json)

    st.write("**Code** for easy copy")
    st.code(json.dumps(properties_json, indent=2), language='json', line_numbers=True, wrap_lines=True)

elif pages == "Construct Notion Blocks":
    st.header(":material/check_box: Construct Notion Blocks")

    block_types = [
        'Paragraph', 'Heading 1', 'Heading 2', 'Heading 3', 'Bulleted List',
        'Numbered List', 'To-do', 'Toggle', 'Code'
    ]

    # Initialize block list in session state
    if 'block_list' not in st.session_state:
        st.session_state['block_list'] = []

    # Button to add a new block
    st.sidebar.subheader(("Page Blocks"))
    st.sidebar.caption("Add and configure blocks for your Notion Pages. JSON is updated every time you press 'Add Block'")
    if st.sidebar.button("Add Block", type="primary"):
        st.session_state['block_list'].append({'type': None, 'content': None})

    # Display block inputs
    if st.session_state['block_list']:
        for idx, block in enumerate(st.session_state['block_list']):
            st.subheader(f"Block {idx + 1}")
            block_type_key = f"block_type_{idx}"
            content_key = f"block_content_{idx}"
            st.selectbox("Select block type", block_types, key=block_type_key)
            st.text_area("Enter content (use new lines for lists)", key=content_key)

            # Toggle options for annotations
            bold_key = f"bold_{idx}"
            italic_key = f"italic_{idx}"
            strikethrough_key = f"strikethrough_{idx}"
            underline_key = f"underline_{idx}"
            code_key = f"code_{idx}"
            st.checkbox("Bold", key=bold_key)
            st.checkbox("Italic", key=italic_key)
            st.checkbox("Strikethrough", key=strikethrough_key)
            st.checkbox("Underline", key=underline_key)
            st.checkbox("Code", key=code_key)

            # Dropdown for color selection
            color_key = f"color_{idx}"
            st.selectbox("Select text color", NOTION_COLORS, key=color_key)

    # Generate blocks JSON automatically
    blocks = []
    for idx, block in enumerate(st.session_state['block_list']):
        block_type_key = f"block_type_{idx}"
        content_key = f"block_content_{idx}"
        block_type = st.session_state.get(block_type_key)
        content = st.session_state.get(content_key)

        if content:
            annotations = {
                'bold': st.session_state.get(f"bold_{idx}", False),
                'italic': st.session_state.get(f"italic_{idx}", False),
                'strikethrough': st.session_state.get(f"strikethrough_{idx}", False),
                'underline': st.session_state.get(f"underline_{idx}", False),
                'code': st.session_state.get(f"code_{idx}", False),
                'color': st.session_state.get(f"color_{idx}", 'default')
            }

            if block_type == 'Paragraph':
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": content
                            },
                            'annotations': annotations
                        }]
                    }
                })
            elif block_type.startswith('Heading'):
                heading_level = int(block_type[-1])
                heading_type = f"heading_{heading_level}"
                blocks.append({
                    "object": "block",
                    "type": heading_type,
                    heading_type: {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": content
                            },
                            'annotations': annotations
                        }]
                    }
                })
            elif block_type == 'Bulleted List':
                items = [item.strip() for item in content.split('\n') if item.strip()]
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                },
                                'annotations': annotations
                            }]
                        }
                    })
            elif block_type == 'Numbered List':
                items = [item.strip() for item in content.split('\n') if item.strip()]
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "numbered_list_item",
                        "numbered_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                },
                                'annotations': annotations
                            }]
                        }
                    })
            elif block_type == 'To-do':
                items = [item.strip() for item in content.split('\n') if item.strip()]
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                },
                                'annotations': annotations
                            }],
                            "checked": False  # Modify as needed
                        }
                    })
            elif block_type == 'Toggle':
                blocks.append({
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": content
                            },
                            'annotations': annotations
                        }],
                        "children": [
                            {
                                "object": "block",
                                "type": "paragraph",
                                "paragraph": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {"content": "Text Body Here"},
                                            'annotations': annotations
                                        }
                                    ]
                                },
                            }
                        ],  # Add nested blocks if needed
                    }
                })
            elif block_type == 'Code':
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "caption": [],
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }],
                        "language": "python"
                    }
                })
            # Implement other block types as needed
    st.divider()
    st.subheader(":material/code_blocks: Generated Blocks JSON")
    with st.container(height=300, border=True):
        st.json(blocks)
    st.write("**Code** for easy copy")
    st.code(json.dumps(blocks, indent=2), language='json', line_numbers=True, wrap_lines=True)
