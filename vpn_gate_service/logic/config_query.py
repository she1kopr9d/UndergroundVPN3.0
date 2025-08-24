import database.io.server
import database.models
import logic.keygen


def get_template_config(private) -> str:
    data = {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "port": 44344,
                "protocol": "vless",
                "settings": {
                    "clients": [
                        {
                            "id": "cbabcd4b-1585-4f44-9f87-3a2e888c19c8",
                            "flow": "xtls-rprx-vision",
                            "level": 0,
                            "email": "admin_init@xray",
                        },
                    ],
                    "decryption": "none",
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "show": False,
                        "dest": "www.cloudflare.com:443",
                        "xver": 0,
                        "serverNames": ["www.cloudflare.com"],
                        "privateKey": private,
                        "shortIds": ["12345678"],
                    },
                },
            }
        ],
        "outbounds": [
            {"protocol": "freedom"},
            {"protocol": "blackhole", "settings": {}, "tag": "blocked"},
        ],
        "routing": {
            "rules": [
                {
                    "type": "field",
                    "ip": ["geoip:private"],
                    "outboundTag": "blocked",
                }
            ]
        },
    }
    return data


async def create_server_config(
    server: database.models.Server,
) -> tuple:
    public, private = logic.keygen.gen_pair()
    config_data = get_template_config(private)
    server_config = database.io.server.create_server_config(
        server,
        public,
        private,
        config_data,
    )
    return (server_config, public, private)
