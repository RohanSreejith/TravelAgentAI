from langchain.tools import Tool
import requests

API_BASE = "https://travelagentbackend.onrender.com/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_input: str) -> str:
    try:
        response = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=15)
        response.raise_for_status()
        packages = response.json()

        if not packages:
            return "❗ No travel packages found."

        formatted = "<h3>🧳 Available Travel Packages</h3>"
        for pkg in packages:
            formatted += (
                "<hr>"
                f"<b>🆔 ID:</b> {pkg['id']}<br>"
                f"<b>🏷️ Title:</b> {pkg['title']}<br>"
                f"<b>📍 Destination:</b> {pkg['destination']}<br>"
                f"<b>📅 Duration:</b> {pkg['duration_days']} days<br>"
                f"<b>💰 Price:</b> ${pkg['price']:,.2f}<br>"
                f"<b>📝 Description:</b> {pkg['description']}<br><br>"
            )
        return formatted

    except requests.exceptions.RequestException as e:
        return (
            f"<b>❌ Error fetching packages:</b> {e}<br>"
            f"<b>Status Code:</b> {getattr(e.response, 'status_code', 'N/A')}<br>"
            f"<b>Details:</b> {getattr(e.response, 'text', '')}"
        )


def _create_package(input_str: str) -> str:
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 5:
            return "❗ Invalid format. Use: title | destination | days | price | description"

        data = {
            "title": parts[0],
            "destination": parts[1],
            "duration_days": int(parts[2]),
            "price": float(parts[3]),
            "description": parts[4],
        }

        response = requests.post(f"{API_BASE}packages/", json=data, auth=AUTH, timeout=10)
        response.raise_for_status()
        created = response.json()

        return (
            f"<b>✅ Package Created Successfully!</b><br><br>"
            f"<b>🆔 ID:</b> {created.get('id')}<br>"
            f"<b>🏷️ Title:</b> {created.get('title')}<br>"
            f"<b>📍 Destination:</b> {created.get('destination')}<br>"
            f"<b>📅 Duration:</b> {created.get('duration_days')} days<br>"
            f"<b>💰 Price:</b> ${created.get('price'):,.2f}<br>"
            f"<b>📝 Description:</b> {created.get('description')}"
        )
    except Exception as e:
        return f"<b>❌ Error creating package:</b> {str(e)}"

get_packages = Tool(
    name="get_packages",
    func=_get_packages,
    description="Fetches all travel packages. Input is ignored."
)

create_package = Tool(
    name="create_package",
    func=_create_package,
    description="Creates a travel package. Input format: 'title | destination | days | price | description'"
)
