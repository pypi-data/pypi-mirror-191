IMAGE_CONFIG = {
    'width': 3840,
    'height': 2160,
    # 'width': 1920,
    # 'height': 1080,
    'minimap_width_percent': 0.05,
    # 'seconds_per_screen': 1,
    # 'seconds_per_screen': 2,
    'seconds_per_screen': 6,
    'note_min': 'G2',
    'note_max': 'C5',
    'dpi': 96,
    'scale_root': 'D',
    'scale_name': 'phrygian',
    'single_max_width': 4096,
    'single_max_height': 4096,
}

plan = {
    'note_min': IMAGE_CONFIG['note_min'],
    'note_max': IMAGE_CONFIG['note_max'],
    'min_recors_per_note': 3,
    'max_std_log2': 0.02,
}

# spice_model_path = 'https://tfhub.dev/google/spice/2'
spice_model_path = 'data/spice_model/'

host = 'libmv.tandav.me'
port = 50007
certchain_path = 'data/certs/fullchain.pem'
certkey_path = 'data/certs/privkey.pem'
client_certs_path = 'data/certs/client'
