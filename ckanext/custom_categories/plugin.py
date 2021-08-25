import ckan.plugins as p
import ckan.plugins.toolkit as tk

CATEGORIES_LIST = ["Science & Technology","Public Safety", "Manufactoring & Public Services","Agriculture, Food & Forests","Cities & Regions","Connectivity","Culture","Demography","Economy & Finance","Education","Environment & Energy","Government & Public Sector","Health","Housing & Public Services" ]


def all_categories():
    options_list = []
    for opt in CATEGORIES_LIST:
        dict1 = {'text':opt,'value':opt}
        options_list.append(dict1)
    
    return options_list

def valid_category(value):
    if value in CATEGORIES_LIST:
        return value
    else:
        raise tk.Invalid('Select a Valid Package Category')

class Custom_CategoriesPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    
    p.implements(p.IValidators)
    def get_validators(self):
        return {
            'custom_category_valid_category':valid_category
        }    
    
    p.implements(p.IFacets)
    def dataset_facets(self, facets_dict, package_type):
        #facets_dict['groups'] = tk._('custom_text')
        #facets_dict['custom_text'] = facets_dict.pop('groups')
        new_dict = {}
        for key in facets_dict:
            if key == 'groups':
                new_dict['category'] = tk._('Category')
            else:
                new_dict[key] = facets_dict[key]
        return new_dict


    p.implements(p.IDatasetForm) 
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        schema.update({
            'category': [#tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras'),
                            tk.get_validator('custom_category_valid_category')
                            ]
        })
        return schema

    def create_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema
    
    def show_package_schema(self):
        schema = super(Custom_CategoriesPlugin, self).show_package_schema()
        schema.update({
            'category': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
        })
        return schema
    
    # IConfigurer
    p.implements(p.IConfigurer)
    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        #toolkit.add_public_directory(config_, 'public')
        #toolkit.add_resource('fanstatic', 'custom_categories')
            
    p.implements(p.ITemplateHelpers)
    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'custom_categories_list': all_categories                
                }


