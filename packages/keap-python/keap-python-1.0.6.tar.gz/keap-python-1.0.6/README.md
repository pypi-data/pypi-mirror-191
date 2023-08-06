# README #

This library makes it easy to set up a Keap authorization without needing a frontend client using CLI utilities.

## What do I need to get set up? ##

* A [Keap Sandbox App](https://developer.infusionsoft.com/resources/sandbox-application/)
* A [Keap Developer App](https://keys.developer.keap.com/)

## Setting up Keap Developer App ##

* Once you are signed in to the Keap Developer Portal, visit [your apps page](https://keys.developer.keap.com/my-apps)
* Click "+New App" in the top right corner
* Give your app a name and description
* Click "Enable" next to the API listed at the bottom of the page
* Click "Save"

## Setting up Keap SDK in a project ##

* Run `pip install keap-python`
* If using in Django:
    * Configure KEAP dictionary in your settings file
        * The only requirements are CLIENT_ID and CLIENT_SECRET, everything else works out of the box
* Activate your python VENV
* If using virtual environment
    * Activate your virtual environment
    * `${sript_prefix} = python venv/bin/keap`
* If you are using Docker
    * `${sript_prefix} = docker compose -f local.yml exec django keap`
* Run `${sript_prefix} generate-client-config`
    * It will ask you for information obtained above: You can use all the defaults
        * Client ID
        * Client Secret
        * Redirect URL
        * App Name
        * Allow None
        * Use Datetime
        * Storage Class
        * If you want to save to file
            * Provide a valid path for keap-credentials.json
        * else the credentials will be echoed out
    * To confirm, check the keap credentials path you entered, or the default, and there should be a json file with all
      the info you entered. Verify the details.
* Run `${sript_prefix} get-access-token`
    * Use the defaults or repeat the info used above for
        * Path to Keap Credentials
    * Confirm the app name to be refreshed, if single app, just use default
    * It will generate a URL, copy and visit this url and complete the signin flow. You will end up at the Redirect URL
      used above, copy this value from the browser.
        * e.g. `https://theapiguys.com/?code=GdRGbcuo&scope=full%7Chl214.infusionsoft.com&state=hl214`
    * Paste this url back into the terminal.
    * To confirm, view the file where you said to save token, it should be a json object with your {client_name|default}
      as a key with and related info in another object.
      ```json
          {
              "default": {
                  "access_token": "xxxxxxxxxxxxxxxxxxxxx",
                  "refresh_token": "xxxxxxxxxxxxxxxxxxxx",
                  "expires_in": 86399,
                  "end_of_life": 1661361510,
                  "scope": "full|hl214.infusionsoft.com"
              }
          }```
* That's it! You should now have a valid token to use with the Keap API.

## Usage ##

It is pretty simple to get started using the SDK once you have a valid token.

### Setup Keap ##

```python
# Set up Keap Option 1
from keap import Keap 
ROOT_DIR = Path(__file__).resolve().parent
keap = Keap(config_file=ROOT_DIR / 'keap_credentials.json')

# Set up Keap Option 2
from keap import Keap
KEAP = {
    'CLIENT_ID': "xxxxxxxxxxxxxxxxx",
    'CLIENT_SECRET': "xxxxxxxxxxxxxxx",
    'STORAGE_PATH': ROOT_DIR / 'keap-tokens.json',
}
keap = Keap(config=KEAP)

# Setup Keap in Django
Define KEAP config in settings.py 
KEAP = {
    'CLIENT_ID': "xxxxxxxxxxxxxxxxx",
    'CLIENT_SECRET': "xxxxxxxxxxxxxxx",
    'STORAGE_PATH': ROOT_DIR / 'keap-tokens.json',
}
#In your app
from keap import Keap
keap = Keap()

# Multi-app usage is possible. If you want to swap from the default app all you have to do is
keap.change_app("NEW_APP_NAME")

# Refresh Active Token
keap.refresh_access_token()  # This will also save the newly refreshed token
```

### XML Contact Service

```python
from keap import Keap

keap = Keap()
# Add a contact using ContactService
contact = {'FirstName': 'John', 'LastName': 'Doe', 'Email': 'johndoe@email.com'}
contact = keap.XML.ContactService.add(contact)
print(contact)  # 1552

# Query a contact  using DataService
contact = keap.XML.DataService.query("Contact", 1000, 0, {'Id': 1263}, ['FirstName', 'LastName', "Id"], 'Id', True)
print(contact)  # [{'FirstName': 'Johnny', 'LastName': 'Consumer', 'Id': 1263}]

# Load a Contact using DataService
contact = keap.XML.DataService.load("Contact", 1552, ['FirstName', 'LastName', "Id"])
print(contact)  # {'FirstName': 'Johnny', 'LastName': 'Consumer', 'Id': 1263}

# Load a contact using ContactService
contact = keap.XML.ContactService.load(1552, ['FirstName', 'LastName', "Id"])
print(contact)  # {'FirstName': 'Johnny', 'LastName': 'Consumer', 'Id': 1263}

```

### Working API Example using Tag and Contact Services

```python
from keap import Keap
from keap.REST.models import CustomFieldType, EmailAddress, DuplicateOption, CustomField, BillingAddress, \
    ShippingAddress, OtherAddress, PhoneNumber, FaxNumber, SocialAccount
from datetime import datetime
keap = Keap()
keap.refresh_access_token()  # This will also save the newly refreshed token

contact_service = keap.REST_V1.ContactService
tag_service = keap.REST_V1.TagService
since = datetime.now()
email_address = "johnny5@consumer.com"
field_name = "SomeDateCustomField"

# Load Contact Model
contact_model = contact_service.model()
print(contact_model)
'''
{'custom_fields': [
    {
        'id': 182,
        'label': 'Some Date Custom Field',
        'options': [],
        'record_type': 'CONTACT',
        'field_type': 'Text',
        'field_name': 'SomeDateCustomField'
    }
],
'optional_properties': [
    'birthday', 'opt_in_reason', 'preferred_locale', 'website', 'notes', 'custom_fields', 'prefix', 'origin',
    'source_type', 'time_zone', 'suffix', 'lead_source_id', 'social_accounts', 'fax_numbers', 'relationships',
    'spouse_name', 'contact_type', 'company_name', 'job_title', 'anniversary', 'preferred_name'
]
}
'''
custom_field = next(filter(lambda x: x.get('field_name') == field_name, contact_model.get('custom_fields', [])),
                    None)
print(custom_field)
# {'id': 182, 'label': 'Some Date Custom Field', 'options': [], 'record_type': 'CONTACT', 'field_type': 'Text', 'field_name': 'SomeDateCustomField'}

print(custom_field.get('id'))
# 182

# Create a custom field
if not custom_field.get('id'):
    custom_field = contact_service.create_custom_field(CustomFieldType.TEXT, field_name)
    print(custom_field)
    # {'id': 182, 'label': 'Some Date Custom Field', 'options': [], 'record_type': 'CONTACT', 'field_type': 'Text', 'field_name': 'SomeDateCustomField'}

# Set Custom Field
some_custom_field = CustomField(custom_field.get('id'), "Some Text In a Custom Field")

# Create/Update a contact
address = BillingAddress()
address.line1 = "3619 Muskie Lane"
address.line2 = "Suite A"
address.locality = "Gainesville"
address.region = "Georgia"
address.country_code = "USA"
address.zip_code = "30507"
address.zip_four = "1234"

address2 = ShippingAddress()
address2.line1 = "3619 Muskie Lane"
address2.line2 = "Suite B"
address2.locality = "Gainesville"
address2.region = "Georgia"
address2.country_code = "USA"
address2.zip_code = "30507"
address2.zip_four = "1234"

address3 = OtherAddress()
address3.line1 = "3619 Muskie Lane"
address3.line2 = "Suite C"
address3.locality = "Gainesville"
address3.region = "Georgia"
address3.country_code = "USA"
address3.zip_code = "30507"
address3.zip_four = "1234"

phone = PhoneNumber(1)
phone.number = "770 718 1111"
phone.extension = "123"
phone2 = PhoneNumber(2)
phone2.number = "770 718 2222"
phone2.extension = "222"
phone3 = PhoneNumber(3)
phone3.number = "770 718 3333"
phone3.extension = "333"
phone4 = PhoneNumber(4)
phone4.number = "770 718 4444"
phone4.extension = "444"
phone5 = PhoneNumber(5)
phone5.number = "770 718 5555"
phone5.extension = "555"

fax = FaxNumber(1)
fax.number = "(777) 888 1111"
fax2 = FaxNumber(2)
fax2.number = "(777) 888 2222"

facebook = SocialAccount("Facebook")
facebook.name = "https://facebook.com"

email = EmailAddress(1)
email.email = email_address

contact = contact_service.create(
    addresses=[address, address2, address3],
    opt_in_reason="your reason for opt-in",
    given_name="Johnny",
    family_name="Consumer",
    phone_numbers=[phone, phone2, phone3, phone4, phone5],
    fax_numbers=[fax, fax2],
    source_type="OTHER",
    custom_fields=[some_custom_field],
    email_addresses=[email],
    social_accounts=[facebook],
    duplicate_option=DuplicateOption.EMAIL_AND_NAME  # Remove this to always create
)
print(contact)
'''
{'email_addresses': [{'email': 'johnny5@consumer.com', 'field': 'EMAIL1'}], 'email_opted_in': False, 'addresses': [], 'last_updated': '2022-09-29T00:32:12.000+0000', 'tag_ids': [], 'owner_id': None, 'date_created': '2022-09-28T19:21:25.000+0000', 'middle_name': None, 'given_name': 'Johnny', 'ScoreValue': None, 'email_status': 'NonMarketable', 'phone_numbers': [], 'last_updated_utc_millis': 1664411531590, 'company': None, 'id': 1570, 'family_name': 'Consumer'}
'''
contact_id = contact.get('id')

# Partial update a contact. This will only update family_name
update = contact_service.update(contact_id, family_name="DataWillChange", given_name="DataWontChange",
                                update_mask=['family_name'], custom_fields=[some_custom_field])
print(update)
'''
{'email_addresses': [{'email': 'johnny5@consumer.com', 'field': 'EMAIL1'}], 'email_opted_in': False, 'addresses': [], 'last_updated': '2022-09-29T00:34:25.843+0000', 'tag_ids': [], 'owner_id': None, 'date_created': '2022-09-28T19:21:25.000+0000', 'middle_name': None, 'given_name': 'JohnnyUpdate', 'ScoreValue': '0', 'email_status': 'NonMarketable', 'phone_numbers': [], 'last_updated_utc_millis': 1664411665843, 'company': None, 'id': 1570, 'family_name': 'DataWillChange'}
'''

find_result = contact_service.get(contact_id)
print(find_result)
'''
{'email_addresses': [{'email': 'johnny5@consumer.com', 'field': 'EMAIL1'}], 'email_opted_in': False, 'addresses': [], 'last_updated': '2022-09-29T00:41:38.000+0000', 'tag_ids': [], 'owner_id': None, 'date_created': '2022-09-29T00:41:37.000+0000', 'middle_name': None, 'given_name': 'JohnnyUpdate', 'ScoreValue': '0', 'email_status': 'NonMarketable', 'phone_numbers': [], 'last_updated_utc_millis': 1664412098196, 'company': None, 'id': 1574, 'family_name': 'ConsumerUpdate'}

'''

# Update a contact
some_custom_field.content = "Some New Content Here"
update = contact_service.update(contact_id, family_name="ConsumerUpdate", given_name="JohnnyUpdate",
                                custom_fields=[some_custom_field])
print(update)
'''
{'email_addresses': [{'email': 'johnny5@consumer.com', 'field': 'EMAIL1'}], 'email_opted_in': False, 'addresses': [], 'last_updated': '2022-09-29T00:32:57.848+0000', 'tag_ids': [], 'owner_id': None, 'date_created': '2022-09-28T19:21:25.000+0000', 'middle_name': None, 'given_name': 'JohnnyUpdate', 'ScoreValue': '0', 'email_status': 'NonMarketable', 'phone_numbers': [], 'last_updated_utc_millis': 1664411577848, 'company': None, 'id': 1570, 'family_name': 'ConsumerUpdate'}
'''

# List Contacts
contacts = contact_service.list(since=since, optional_properties=['custom_fields', 'lead_source_id'])
print(contacts)
'''
{'contacts': [{'email_addresses': [{'email': 'johnny5@consumer.com', 'field': 'EMAIL1'}], 'email_opted_in': False, 'addresses': [], 'last_updated': '2022-09-29T00:42:42.000+0000', 'tag_ids': [], 'owner_id': None, 'date_created': '2022-09-29T00:42:39.000+0000', 'middle_name': None, 'given_name': 'JohnnyUpdate', 'ScoreValue': None, 'email_status': 'NonMarketable', 'phone_numbers': [], 'last_updated_utc_millis': 1664412162239, 'company': None, 'id': 1576, 'family_name': 'ConsumerUpdate', 'lead_source_id': None, 'custom_fields': [{'id': 182, 'content': 'Some New Content Here'}]}], 'count': 1, 'next': 'https://api.infusionsoft.com/crm/rest/v1/contacts/?limit=1&offset=1000&since=2022-09-29T00:42:38.087375Z&order=id', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/contacts/?limit=1000&offset=0&since=2022-09-29T00:42:38.087375Z&order=id'}
'''

# Tag a contact
tag_name = "Test Keap API Tag"
category_name = 'API Category'

category_results = keap.XML.DataService.find_by_field("ContactGroupCategory", 1, 0, 'CategoryName',
                                                      category_name, ['Id'])
category_id = category_results[0].get('Id') if category_results else None
print(category_id)  # 42

if not category_id:
    args = {
        'name': category_name,
        'description': 'Test adding a tag category using the REST TagService'
    }
    category = tag_service.create_category(**args)
    print(category)
    # {'id': 42, 'name': 'API Category', 'description': 'Test adding a tag category using the REST TagService'}
    category_id = category_id.get('id')

# List Tags
args = {
    'category': category_id,
    'name': tag_name
}
response = tag_service.list(**args)
print(response)
'''
{'tags': [{'id': 1304, 'name': 'Test Keap API Tag', 'description': 'Test adding a tag using the REST TagService', 'category': {'id': 42, 'name': 'API Category', 'description': None}}], 'count': 1, 'next': 'https://api.infusionsoft.com/crm/rest/v1/tags/?limit=1&offset=1000', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/tags/?limit=1000&offset=0'}
'''
tags = response.get('tags', [])
while len(tags) != response['count']:
    args['offset'] = len(tags)
    response = tag_service.list(**args)
    tags += response.get('tags', [])

print(tags)
'''
[
    {
        'id': 1304, 'name': 'Test Keap API Tag', 
        'description': 'Test adding a tag using the REST TagService', 
        'category': {'id': 42, 'name': 'API Category', 'description': None}
    }
]
'''
tag = next(filter(lambda x: x.get('name') == tag_name, tags), None)
print(tag)
'''
{'id': 1304, 'name': 'Test Keap API Tag', 'description': 'Test adding a tag using the REST TagService', 
'category': {'id': 42, 'name': 'API Category', 'description': None}
}
'''

if not tag:
    # Create Tag
    args = {
        'category': category_id,
        'name': tag_name,
        'description': 'Test adding a tag using the REST TagService'
    }
    tag = tag_service.create(**args)
    print(tag)
    # {'id': 1304, 'name': 'Test Keap API Tag', 'description': 'Test adding a tag using the REST TagService', 'category': {'id': 42, 'name': 'API Category', 'description': None}}

# Test getting tag by Id
tag = tag_service.get(tag.get('id'))
print(tag)
'''
{'id': 1304, 'name': 'Test Keap API Tag', 'description': 'Test adding a tag using the REST TagService',
 'category': {'id': 42, 'name': 'API Category', 'description': None}
 }
'''

# Test adding tag to contacts
tag_contacts = tag_service.add_contacts(tag.get('id'), [contact.get('id')])
print(tag_contacts)  # {'1586': 'SUCCESS'}

# Test removing tag from contacts
remove = tag_service.remove_contact(tag.get('id'), contact.get('id'))
print(remove)  # True

add = contact_service.add_tags(contact.get('id'), [tag.get('id')])
print(add)  # {'1304': 'SUCCESS'}

# Test removing tag from contacts
remove_contacts = tag_service.remove_contacts(tag.get('id'), [contact.get('id')])
print(remove_contacts)  # True

add = contact_service.add_tags(contact.get('id'), [tag.get('id')])
print(add)  # {'1304': 'SUCCESS'}

# Test getting contacts by tag by Id
tagged_contacts = tag_service.get_tagged_contacts(tag.get('id'))
print(tagged_contacts)
'''
{'contacts': [{'contact': {'id': 1586, 'email': 'johnny5@consumer.com', 'first_name': 'Johnny', 'last_name': 'Consumer'}, 'date_applied': '2022-09-29T01:17:19.000+0000'}], 'count': 1, 'next': 'https://api.infusionsoft.com/crm/rest/v1/tags/1304/contacts?limit=1&offset=1000', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/tags/1304/contacts?limit=1000&offset=0'}
'''

remove = contact_service.remove_tag(contact.get('id'), tag.get('id'))
print(remove)

# Delete Contact
delete = contact_service.delete(contact.get('id'))
print(delete)  # True

```

### Tag Service

```python
from keap import Keap

keap = Keap()

# List Tags 
args = {
    'category': 1,
}
response = keap.REST_V1.TagService.list(**args)
print(response)
# {'tags': [{'id': 385, 'name': 'Add a Tag', 'description': '', 'category': {'id': 1, 'name': 'Customer Tags', 'description': None}}], 'count': 4, 'next': 'https://api.infusionsoft.com/crm/rest/v1/tags/?limit=1&offset=1', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/tags/?limit=1&offset=0'}
tags = response['tags']

while len(tags) != response['count']:
    args['offset'] = len(tags)
    response = keap.REST_V1.TagService.list(**args)
    tags += response['tags']

# Create Tag
args = {
    'category': 1,
    'name': 'Test Tag Name',
    'description': 'Test adding a tag using the REST TagService'
}
tag_response = keap.REST_V1.TagService.create(**args)
print(tag_response)
# {'id': 1302, 'name': 'Test Tag Name', 'description': 'Test adding a tag using the REST TagService', 'category': {'id': 1, 'name': 'Customer Tags', 'description': None}}

# Create Category
args = {
    'name': 'API Category',
    'description': 'Test adding a tag category using the REST TagService'
}
response = keap.REST_V1.TagService.create_category(**args)
print(response)
# {'id': 42, 'name': 'API Category', 'description': 'Test adding a tag category using the REST TagService'}

# Test getting tag by Id
tag = keap.REST_V1.TagService.get(1302)
print(tag)
# {'id': 1302, 'name': 'Test Tag Name', 'description': 'Test adding a tag using the REST TagService', 'category': {'id': 1, 'name': 'Customer Tags', 'description': None}}

# Test getting companies by tag by Id
tagged_companies = keap.REST_V1.TagService.get_tagged_companies(385)
print(tagged_companies)
# {'companies': [{'company': {'id': 91, 'email': '', 'company_name': 'My Company'}, 'date_applied': '2022-09-28T17:03:16.000+0000'}], 'count': 1, 'next': 'https://api.infusionsoft.com/crm/rest/v1/tags/385/companies?limit=1&offset=1000', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/tags/385/companies?limit=1000&offset=0'}

# Test getting contacts by tag by Id
tagged_contacts = keap.REST_V1.TagService.get_tagged_contacts(385)
print(tagged_contacts)
# {'contacts': [{'contact': {'id': 1269, 'email': 'johnny@consumer.com', 'first_name': 'Johnny', 'last_name': ''}, 'date_applied': '2022-09-28T17:06:37.000+0000'}], 'count': 1, 'next': 'https://api.infusionsoft.com/crm/rest/v1/tags/385/contacts?limit=1&offset=1000', 'previous': 'https://api.infusionsoft.com/crm/rest/v1/tags/385/contacts?limit=1000&offset=0'}

# Test adding tag to contacts
tag_contacts = keap.REST_V1.TagService.add_contacts(385, [1251, 1269, 1271])
print(tag_contacts)  # {'1251': 'CONTACT_NOT_FOUND', '1269': 'DUPLICATE', '1271': 'SUCCESS'}

# Test removing tag from contacts
tag_contacts = keap.REST_V1.TagService.remove_contacts(385, [1251, 1269, 1271])
print(tag_contacts)  # True

# Test removing tag from contacts
remove = keap.REST_V1.TagService.remove_contact(385, 1269)
print(remove)
# True
```

### Helpful Documentation ###

* [XML RPC Docs](https://developer.infusionsoft.com/docs/xml-rpc/#contact-create-a-contact)
    * Although out of data on the Python side, they still provide mostly correct info on parameters and such.
* [Keap Table Schema](https://developer.infusionsoft.com/docs/table-schema/) Will help with any DataService queries
