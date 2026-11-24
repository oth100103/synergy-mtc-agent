"""Context Layer (Ed's context/server.py) als Container auf Coolify starten.

Lauscht auf 0.0.0.0:8006/mcp, damit der Agent ihn im Docker-Netz unter
http://context:8006/mcp erreicht. Der Dienst bekommt keine öffentliche Domain,
deshalb ist der DNS-Rebinding-Schutz für lokale Hosts hier abgeschaltet."""

from mcp.server.transport_security import TransportSecuritySettings

from context.server import build_server

if __name__ == "__main__":
    server = build_server(TransportSecuritySettings(enable_dns_rebinding_protection=False))
    server.settings.host = "0.0.0.0"  # noqa: S104 - nur im internen Docker-Netz
    server.run(transport="streamable-http")
