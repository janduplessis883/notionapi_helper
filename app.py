import streamlit as st
import datetime
import streamlit_shadcn_ui as ui

# Define possible property types
property_types = [
    'Title', 'Rich Text', 'Number', 'Select', 'Multi-select', 'Date', 'Checkbox',
    'URL', 'Email', 'Phone Number'
]
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
    st.header("About")
    st.write("Welcome to the **Notion API JSON Builder!**")
    st.write("This humble little app is here to help you tackle one of the trickiest parts of working with the Notion API—constructing complex JSON structures. Whether you’re configuring properties for your Notion databases or building dynamic blocks to append to your pages, this app simplifies the process.")
    st.write("With a user-friendly interface, you can easily set up properties like titles, text, numbers, and more, or generate blocks like headings, lists, and to-dos. No more guesswork when building JSON for Notion!")
    st.write("Our goal is to make your life easier when working with Notion, whether you’re creating dynamic dashboards or detailed documents. If you’re juggling database properties or adding rich blocks of content, this app will save you time and energy.")
    st.write("Give it a try, and happy building!")



elif pages == "Configure Database Properties":

    st.header("Configure Database Properties")

    # Initialize property list in session state
    if 'property_list' not in st.session_state:
        st.session_state['property_list'] = []

    # Button to add a new property
    if st.button("Add Property"):
        st.session_state['property_list'].append({'type': None, 'name': None})

    # Display property inputs
    if st.session_state['property_list']:
        for idx, prop in enumerate(st.session_state['property_list']):
            st.subheader(f"Property {idx + 1}")
            prop_type_key = f"prop_type_{idx}"
            prop_name_key = f"prop_name_{idx}"

            # Select property type
            prop_type = st.selectbox("Select property type", property_types, key=prop_type_key)
            prop_name = st.text_input(f"Enter the property name for {prop_type}", key=prop_name_key)

            # Based on property type, display appropriate inputs
            if prop_type == 'Title':
                title_content_key = f"title_content_{idx}"
                st.text_input("Enter the title content", key=title_content_key)
            elif prop_type == 'Rich Text':
                rich_text_content_key = f"rich_text_content_{idx}"
                st.text_input("Enter the rich text content", key=rich_text_content_key)
            elif prop_type == 'Number':
                number_value_key = f"number_value_{idx}"
                st.number_input("Enter the number value", key=number_value_key)
            elif prop_type == 'Select':
                option_name_key = f"select_option_{idx}"
                st.text_input("Enter the option name", key=option_name_key)
            elif prop_type == 'Multi-select':
                options_key = f"multi_select_options_{idx}"
                st.text_input("Enter options separated by commas", key=options_key)
            elif prop_type == 'Date':
                start_date_key = f"start_date_{idx}"
                include_time_key = f"include_time_{idx}"
                include_end_date_key = f"include_end_date_{idx}"
                end_date_key = f"end_date_{idx}"
                start_time_key = f"start_time_{idx}"
                end_time_key = f"end_time_{idx}"

                st.date_input("Select start date", key=start_date_key)
                st.checkbox("Include time?", key=include_time_key)
                if st.session_state.get(include_time_key):
                    st.time_input("Select start time", key=start_time_key)
                st.checkbox("Include end date?", key=include_end_date_key)
                if st.session_state.get(include_end_date_key):
                    st.date_input("Select end date", key=end_date_key)
                    if st.session_state.get(include_time_key):
                        st.time_input("Select end time", key=end_time_key)
            elif prop_type == 'Checkbox':
                checkbox_value_key = f"checkbox_value_{idx}"
                st.checkbox("Check if true", key=checkbox_value_key)
            elif prop_type == 'URL':
                url_value_key = f"url_value_{idx}"
                st.text_input("Enter the URL", key=url_value_key)
            elif prop_type == 'Email':
                email_value_key = f"email_value_{idx}"
                st.text_input("Enter the email", key=email_value_key)
            elif prop_type == 'Phone Number':
                phone_value_key = f"phone_value_{idx}"
                st.text_input("Enter the phone number", key=phone_value_key)
            # Add other property types as needed

    # Generate the properties JSON automatically
    properties_json = {}
    for idx, prop in enumerate(st.session_state['property_list']):
        prop_type_key = f"prop_type_{idx}"
        prop_name_key = f"prop_name_{idx}"
        prop_type = st.session_state.get(prop_type_key)
        prop_name = st.session_state.get(prop_name_key)

        if prop_name and prop_type:
            if prop_type == 'Title':
                title_content_key = f"title_content_{idx}"
                title_content = st.session_state.get(title_content_key, '')
                if title_content:
                    properties_json[prop_name] = {
                        "title": [
                            {
                                "text": {
                                    "content": title_content
                                }
                            }
                        ]
                    }
            elif prop_type == 'Rich Text':
                rich_text_content_key = f"rich_text_content_{idx}"
                rich_text_content = st.session_state.get(rich_text_content_key, '')
                if rich_text_content:
                    properties_json[prop_name] = {
                        "rich_text": [
                            {
                                "text": {
                                    "content": rich_text_content
                                }
                            }
                        ]
                    }
            elif prop_type == 'Number':
                number_value_key = f"number_value_{idx}"
                number_value = st.session_state.get(number_value_key)
                if number_value is not None:
                    properties_json[prop_name] = {
                        "number": number_value
                    }
            elif prop_type == 'Select':
                option_name_key = f"select_option_{idx}"
                option_name = st.session_state.get(option_name_key, '')
                if option_name:
                    properties_json[prop_name] = {
                        "select": {
                            "name": option_name
                        }
                    }
            elif prop_type == 'Multi-select':
                options_key = f"multi_select_options_{idx}"
                options = st.session_state.get(options_key, '')
                if options:
                    options_list = [opt.strip() for opt in options.split(',')]
                    properties_json[prop_name] = {
                        "multi_select": [{"name": opt} for opt in options_list]
                    }
            elif prop_type == 'Date':
                start_date_key = f"start_date_{idx}"
                include_time_key = f"include_time_{idx}"
                include_end_date_key = f"include_end_date_{idx}"
                end_date_key = f"end_date_{idx}"
                start_time_key = f"start_time_{idx}"
                end_time_key = f"end_time_{idx}"

                start_date = st.session_state.get(start_date_key)
                include_time = st.session_state.get(include_time_key)
                include_end_date = st.session_state.get(include_end_date_key)
                date_value = {}

                if start_date:
                    if include_time:
                        start_time = st.session_state.get(start_time_key)
                        if start_time:
                            date_value["start"] = datetime.datetime.combine(start_date, start_time).isoformat()
                        else:
                            date_value["start"] = start_date.isoformat()
                    else:
                        date_value["start"] = start_date.isoformat()
                    if include_end_date:
                        end_date = st.session_state.get(end_date_key)
                        if end_date:
                            if include_time:
                                end_time = st.session_state.get(end_time_key)
                                if end_time:
                                    date_value["end"] = datetime.datetime.combine(end_date, end_time).isoformat()
                                else:
                                    date_value["end"] = end_date.isoformat()
                            else:
                                date_value["end"] = end_date.isoformat()
                    properties_json[prop_name] = {
                        "date": date_value
                    }
            elif prop_type == 'Checkbox':
                checkbox_value_key = f"checkbox_value_{idx}"
                checkbox_value = st.session_state.get(checkbox_value_key, False)
                properties_json[prop_name] = {
                    "checkbox": checkbox_value
                }
            elif prop_type == 'URL':
                url_value_key = f"url_value_{idx}"
                url_value = st.session_state.get(url_value_key, '')
                if url_value:
                    properties_json[prop_name] = {
                        "url": url_value
                    }
            elif prop_type == 'Email':
                email_value_key = f"email_value_{idx}"
                email_value = st.session_state.get(email_value_key, '')
                if email_value:
                    properties_json[prop_name] = {
                        "email": email_value
                    }
            elif prop_type == 'Phone Number':
                phone_value_key = f"phone_value_{idx}"
                phone_value = st.session_state.get(phone_value_key, '')
                if phone_value:
                    properties_json[prop_name] = {
                        "phone_number": phone_value
                    }

    st.subheader("Generated Properties JSON")
    st.json(properties_json)

elif pages == "Construct Notion Blocks":
    st.header("Construct Notion Blocks")

    block_types = [
        'Paragraph', 'Heading 1', 'Heading 2', 'Heading 3', 'Bulleted List',
        'Numbered List', 'To-do', 'Toggle', 'Code'
    ]

    # Initialize block list in session state
    if 'block_list' not in st.session_state:
        st.session_state['block_list'] = []

    # Button to add a new block
    if st.button("Add Block"):
        st.session_state['block_list'].append({'type': None, 'content': None})

    # Display block inputs
    if st.session_state['block_list']:
        for idx, block in enumerate(st.session_state['block_list']):
            st.subheader(f"Block {idx + 1}")
            block_type_key = f"block_type_{idx}"
            content_key = f"block_content_{idx}"
            st.selectbox("Select block type", block_types, key=block_type_key)
            st.text_area("Enter content (use new lines for lists)", key=content_key)

    # Generate blocks JSON automatically
    blocks = []
    for idx, block in enumerate(st.session_state['block_list']):
        block_type_key = f"block_type_{idx}"
        content_key = f"block_content_{idx}"
        block_type = st.session_state.get(block_type_key)
        content = st.session_state.get(content_key)

        if content:
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
                                'annotations': {'bold': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'},
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
                            'annotations': {'bold': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'},
                        }]
                    }
                })
            elif block_type == 'Bulleted List':
                items = content.split('\n')
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                }
                            }]
                        }
                    })
            elif block_type == 'Numbered List':
                items = content.split('\n')
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "numbered_list_item",
                        "numbered_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                }
                            }]
                        }
                    })
            elif block_type == 'To-do':
                items = content.split('\n')
                for item in items:
                    blocks.append({
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": item
                                }
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
                            }
                        }],
                        "children": [
                                        {
                                            "type": "paragraph",
                                            "paragraph": {
                                                "rich_text": [
                                                    {
                                                        "type": "text",
                                                        "text": {"content": "Text Body Here"},
                                                    }
                                                ]
                                            },
                                        }
                                    ],  # Add nested blocks if needed
                    }
                })
            elif block_type == 'Code':
                blocks.append({
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



    st.subheader("Generated Blocks JSON")
    st.json(blocks)
