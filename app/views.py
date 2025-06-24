from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from urllib.parse import urlencode
import requests
import random,json

url = "https://services.leadconnectorhq.com/oauth/token"

#to get access token
def get_access_token(request):
    code = request.GET.get('code')
    if code:
        payload = {
            "client_id": settings.HIGHLEVEL_CLIENT_ID,
            "client_secret": settings.HIGHLEVEL_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.HIGHLEVEL_REDIRECT_URI
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        try:
            response = requests.post(url, data=payload, headers=headers)
            data = response.json()
            print(data)
            if "access_token" in data and 'refresh_token' in data and 'locationId' in data:
                request.session['access_token'] = data['access_token']
                request.session['refresh_token'] = data['refresh_token']
                request.session['locationId'] = data['locationId']
                return redirect(contact)
            else:
                return HttpResponse(f"Error: {data}", status=400)

        except Exception as e:
            return HttpResponse(f"Exception: {str(e)}", status=500)

    return render(request,'index.html')


    

#to get authorization code
def start_auth(request):
    base_url = "https://marketplace.gohighlevel.com/oauth/chooselocation"
    params = {
        "response_type": "code",
        "client_id": settings.HIGHLEVEL_CLIENT_ID,
        "redirect_uri": settings.HIGHLEVEL_REDIRECT_URI,  
        "scope": "contacts.readonly contacts.write locations/customFields.readonly"
    }

    full_url = f"{base_url}?{urlencode(params)}"
    return redirect(full_url)


def logout(request):
    request.session.flush()
    return redirect(get_access_token)

#to loading data updation page
def contact(request):
    if 'access_token' in request.session:
        return render(request,'contact.html')
    else:
        return redirect(get_access_token)
    
def get_and_udpate_contact(request):
    # Your credentials (get from session/settings)
    access_token = request.session.get('access_token')  
    location_id = request.session.get('locationId')   
    
    if not access_token or not location_id:
        return HttpResponse("Access token or location ID missing", status=400)
    
    try:
        # Get custom field ID for "DFS Booking Zoom Link"
        custom_fields_url = f"https://services.leadconnectorhq.com/locations/{location_id}/customFields"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Version": "2021-07-28",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        custom_fields_response = requests.get(custom_fields_url, headers=headers)
        if custom_fields_response.status_code != 200:
            return HttpResponse(f"Failed to get custom fields: {custom_fields_response.text}", 
                              status=custom_fields_response.status_code)
        
        custom_fields = custom_fields_response.json().get("customFields", [])
        field_id = next((f["id"] for f in custom_fields if f["name"] == "DFS Booking Zoom Link"), None)#getting the field id with the name DFS Booking Zoom Link

        if not field_id:
            return HttpResponse(f"Custom field 'DFS Booking Zoom Link not found", status=404)
        
        #Get a random contact
        contacts_url = f"https://services.leadconnectorhq.com/contacts?locationId={location_id}"
        contacts_response = requests.get(contacts_url, headers=headers)

        if contacts_response.status_code != 200:
            return HttpResponse(f"Failed to get contacts: {contacts_response.text}", 
                              status=contacts_response.status_code)
        contacts_data = contacts_response.json().get('contacts',[])
        if not contacts_data:
            return HttpResponse("No contacts found", status=404)
        contact_obj = random.choice(contacts_data) # get randome contact data
        contact_id = contact_obj.get('id')
        
        # Update contact custom field
        url_update_contact = f"https://services.leadconnectorhq.com/contacts/{contact_id}"
        
        # Set the custom field value
        field_value = "TEST"
        
        # Clear existing custom fields and add new one
        contact_obj['customFields'] = [
            {
                'id': field_id,
                'value': field_value
            }
        ]
        
        # Remove fields that shouldn't be sent in update
        fields_to_remove = [
            'id', 'dateAdded', 'dateUpdated', 'locationId', 'contactName', 
            'firstNameRaw', 'lastNameRaw', 'followers', 'attributions'
        ]
        for field in fields_to_remove:
            contact_obj.pop(field, None)
        
        # Make the API call
        print(f'updated contact detailes----------------\n{contact_obj}\n------------')
        contact_update_response = requests.put(
            url_update_contact, 
            json=contact_obj,
            headers=headers
        )
        
        if contact_update_response.status_code != 200:
            return HttpResponse(f"Update contact failed: {contact_update_response.text}", 
                              status=contact_update_response.status_code)
        
        # Get updated contact data
        updated_contact = contact_update_response.json().get('contact',None)
        #       
        # Prepare context for template
        context = {
            'contact_id': updated_contact.get('id'),
            'first_name': updated_contact.get('firstName', ''),
            'last_name': updated_contact.get('lastName', ''),
            'email': updated_contact.get('email', ''),
            'phone': updated_contact.get('phone', ''),
            'custom_field_id': field_id,
            'custom_field_value': 'TEST',
            'update_success': True
        }
        
        return render(request, 'contact.html', context)
        
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Network error: {str(e)}", status=500)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
