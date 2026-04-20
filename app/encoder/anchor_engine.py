import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
ASSETS_DIR = os.getenv('ASSETS_DIR', 'app/assets')

logger = logging.getLogger(__name__)

class AnchorEngine:
    def __init__(self):
        self.state_file = os.path.join(ASSETS_DIR, 'anchor_state.json')
        self.anchors = ['male', 'female']
        self.current_index = self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data.get('current_index', 0)
        return 0

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({'current_index': self.current_index}, f)

    def get_next_anchor(self):
        anchor = self.anchors[self.current_index % 2]
        self.current_index += 1
        self.save_state()
        image_path = os.path.join(ASSETS_DIR, 'anchors', f'{anchor}.png')
        voice = f'mr-IN-{anchor}'
        logger.info(f"Selected anchor: {anchor}")
        return {
            "anchor": anchor,
            "image": image_path,
            "voice": voice
        }