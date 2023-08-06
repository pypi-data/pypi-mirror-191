import json

def get_omnious_tag(omnious_category_name, data):
    response_body = json.loads(data)
    omnious_tag_dict = {}
    if response_body is not None:
        objects = response_body.get('objects', None)
        if objects is not None:
            tag_data = None
            for object in objects:
                if object.get('tags') is not None:
                    for tag in object.get('tags'):
                        category_name = tag['category']['name']
                        if omnious_category_name == category_name:
                            tag_data = tag
                            break

            if tag_data is not None:
                if tag_data.get('colors') is not None and len(tag_data.get('colors')) > 0:
                    omnious_tag_dict['color'] = tag_data['colors'][0].get('name', '')
                if tag_data.get('textures') is not None and len(tag_data.get('textures')) > 0:
                    omnious_tag_dict['texture'] = tag_data['textures'][0].get('name', '')
                if tag_data.get('looks') is not None and len(tag_data.get('looks')) > 0:
                    omnious_tag_dict['look'] = tag_data['looks'][0].get('name', '')
                if tag_data.get('fit') is not None:
                    omnious_tag_dict['fit'] = tag_data['fit'].get('name', '')

    return omnious_tag_dict
