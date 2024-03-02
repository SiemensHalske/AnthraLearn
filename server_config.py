from app import create_app

app = create_app()

SERVER_CONFIG = {
    'host': "localhost",
    'port': 8080,
    'max_packet_size': 2000,
    'max_connection': 2,
    'name': 'what is my name',
    'debug': True
}
