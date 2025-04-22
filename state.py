ongoing_conversations = {}

def add_conversation(client_id, manager_id):
    ongoing_conversations[client_id] = {
        'manager_id': manager_id,
        'client_id': client_id,
        'active': True
    }
    print(f"Added conversation: {ongoing_conversations}")


def set_client_to_forward(manager_id, client_id):
    if manager_id not in ongoing_conversations:
        ongoing_conversations[manager_id] = {'active': True}

    if 'client_to_forward' not in ongoing_conversations[manager_id]:
        ongoing_conversations[manager_id]['client_to_forward'] = client_id
        print(f"Set client {client_id} to forward for manager {manager_id}: {ongoing_conversations[manager_id]}")
    else:
        print(
            f"Manager {manager_id} already has a client to forward: {ongoing_conversations[manager_id]['client_to_forward']}")

    ongoing_conversations[manager_id]['client_to_forward'] = client_id
    print(f"Set client {client_id} to forward for manager {manager_id}: {ongoing_conversations[manager_id]}")

def get_manager_for_client(client_id):
    return ongoing_conversations.get(client_id, {}).get('manager_id')

def get_client_to_forward(manager_id):
    client_to_forward = ongoing_conversations.get(manager_id, {}).get('client_to_forward')
    print(f"Client to forward for manager {manager_id}: {client_to_forward}")
    return client_to_forward

def clear_client_to_forward(manager_id):
    if manager_id in ongoing_conversations:
        ongoing_conversations[manager_id].pop('client_to_forward', None)

def has_active_conversations(manager_id):
    active_convos = [
        convo for convo in ongoing_conversations.values()
        if convo.get('manager_id') == manager_id and convo.get('active', False)
    ]
    print(f"Active conversations for manager {manager_id}: {active_convos}")
    return bool(active_convos)

