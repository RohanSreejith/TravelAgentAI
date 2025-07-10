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

        formatted = "### 🧳 Available Travel Packages\n"
        for pkg in packages:
            formatted += (
                f"\n---\n"
                f"**🆔 ID:** {pkg.get('id', 'N/A')}  \n"
                f"**🏷️ Title:** {pkg.get('title', 'N/A')}  \n"
                f"**📍 Destination:** {pkg.get('destination', 'N/A')}  \n"
                f"**📅 Duration:** {pkg.get('duration_days', 'N/A')} days  \n"
                f"**💰 Price:** ${pkg.get('price', 0):,.2f}  \n"
                f"**📝 Description:** {pkg.get('description', 'N/A')}  \n"
            )
        return formatted

    except requests.exceptions.RequestException as e:
        return (
            f"❌ Error fetching packages: {e}\n"
            f"**Status Code:** {getattr(e.response, 'status_code', 'N/A')}\n"
            f"**Details:** {getattr(e.response, 'text', '')}"
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
            f"✅ **Package Created Successfully!**\n\n"
            f"**🆔 ID:** {created.get('id', 'N/A')}  \n"
            f"**🏷️ Title:** {created.get('title', 'N/A')}  \n"
            f"**📍 Destination:** {created.get('destination', 'N/A')}  \n"
            f"**📅 Duration:** {created.get('duration_days', 'N/A')} days  \n"
            f"**💰 Price:** ${created.get('price', 0):,.2f}  \n"
            f"**📝 Description:** {created.get('description', 'N/A')}"
        )
    except Exception as e:
        return f"❌ Error creating package: {str(e)}"

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
