import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class SignalConsumer(AsyncJsonWebsocketConsumer):
    """
    WebRTC signaling relay for a single room.

    Each browser opens a websocket to /ws/room/<code>/. The consumer assigns a
    peer id, announces joins/leaves, and relays offer/answer/ICE messages
    between peers in the same room group. No media flows through the server —
    only signaling. The call lasts exactly as long as peers stay connected.
    """

    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.group = f'room_{self.code}'
        self.peer_id = self.channel_name  # unique per connection
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

        # Tell the newcomer who they are.
        await self.send_json({'type': 'welcome', 'peer_id': self.peer_id})
        # Tell everyone else a new peer arrived (they will initiate the offer).
        await self.channel_layer.group_send(self.group, {
            'type': 'peer.join',
            'peer_id': self.peer_id,
            'name': '',
            'sender': self.channel_name,
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(self.group, {
            'type': 'peer.leave',
            'peer_id': self.peer_id,
            'sender': self.channel_name,
        })
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content):
        msg_type = content.get('type')

        if msg_type == 'ready':
            # Peer has set its display name and is ready to negotiate.
            await self.name_broadcast(content.get('name', ''))
            return

        if msg_type in ('offer', 'answer', 'ice'):
            target = content.get('target')
            if not target:
                return
            await self.channel_layer.group_send(self.group, {
                'type': 'relay',
                'payload': content,
                'from_peer': self.peer_id,
                'name': content.get('name', ''),
                'target': target,
                'sender': self.channel_name,
            })
            return

        if msg_type == 'chat':
            await self.channel_layer.group_send(self.group, {
                'type': 'chat.message',
                'name': content.get('name', 'Guest'),
                'text': content.get('text', ''),
                'sender': self.channel_name,
            })

    # ── group event handlers ──────────────────────────────────────────────

    async def name_broadcast(self, name):
        self.display_name = name
        await self.channel_layer.group_send(self.group, {
            'type': 'peer.join',
            'peer_id': self.peer_id,
            'name': name,
            'sender': self.channel_name,
        })

    async def peer_join(self, event):
        if event['sender'] == self.channel_name:
            return
        await self.send_json({
            'type': 'peer-join',
            'peer_id': event['peer_id'],
            'name': event.get('name', ''),
        })

    async def peer_leave(self, event):
        if event['sender'] == self.channel_name:
            return
        await self.send_json({'type': 'peer-leave', 'peer_id': event['peer_id']})

    async def relay(self, event):
        # Only deliver to the intended target peer.
        if event['target'] != self.peer_id:
            return
        payload = dict(event['payload'])
        payload['from_peer'] = event['from_peer']
        payload['name'] = event.get('name', '')
        await self.send_json(payload)

    async def chat_message(self, event):
        await self.send_json({
            'type': 'chat',
            'name': event['name'],
            'text': event['text'],
            'self': event['sender'] == self.channel_name,
        })
