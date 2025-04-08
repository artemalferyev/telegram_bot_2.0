ongoing_conversations = {}

def add_conversation(client_id, manager_id):
    ongoing_conversations[client_id] = {
        'manager_id': manager_id,
        'client_id': client_id,
        'active': True
    }
def get_manager_for_client(client_id):
    return ongoing_conversations.get(client_id, {}).get('manager_id')

def set_client_to_forward(manager_id, client_id):
    ongoing_conversations[manager_id] = {
        'client_to_forward': client_id
    }

def get_client_to_forward(manager_id):
    return ongoing_conversations.get(manager_id, {}).get('client_to_forward')

def clear_client_to_forward(manager_id):
    if manager_id in ongoing_conversations:
        ongoing_conversations[manager_id].pop('client_to_forward', None)

def has_active_conversations():
    return bool(ongoing_conversations)


