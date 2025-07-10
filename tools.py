from langchain.tools import Tool
import requests

API_BASE = "https://travelagentbackend.onrender.com/api/"
AUTH = ("rohansreejith05", "Rohan333$")

def _get_packages(_: str) -> str:
    try:
        res = requests.get(f"{API_BASE}packages/", auth=AUTH, timeout=15)
        res.raise_for_status()
        packages = res.json()

        if not packages:
            return "❗ No travel packages found."

        output = ["### 🧳 Available Travel Packages"]
        for p in packages:
            price = p.get("price") or 0.0
            output.append(
                f"\n---\n"
                f"**🆔 ID:** {p.get('id', 'N/A')}  \n"
                f"**🏷️ Title:** {p.get('title', 'N/A')}  \n"
                f"**📍 Destination:** {p.get('destination', 'N/A')}  \n"
                f"**📅 Duration:** {p.get('duration_days', 'N/A')} days  \n"
                f"**💰 Price:** ${price:,.2f}  \n"
                f"**📝 Description:** {p.get('description', 'N/A')}"
            )
        return "\n".join(output)

    except requests.RequestException as e:
        return (
            f"❌ Error fetching packages: {e}\n"
            f"**Status Code:** {getattr(e.response, 'status_code', 'N/A')}\n"
            f"**Details:** {getattr(e.response, 'text', '')}"
        )

def _create_package(input_str: str) -> str:
    try:
        parts = [p.strip() for p in input_str.split("|")]
        if len(parts) != 5:
            return "❗ Use format: title | destination | days | price | description"

        data = {
            "title": parts[0],
            "destination": parts[1],
            "duration_days": int(parts[2]),
            "price": float(parts[3]),
            "description": parts[4],
        }

        res = requests.post(f"{API_BASE}packages/", json=data, auth=AUTH, timeout=10)
        res.raise_for_status()
        p = res.json()
        price = p.get("price") or 0.0

        return (
            f"✅ **Package Created!**\n\n"
            f"**🆔 ID:** {p.get('id', 'N/A')}  \n"
            f"**🏷️ Title:** {p.get('title', 'N/A')}  \n"
            f"**📍 Destination:** {p.get('destination', 'N/A')}  \n"
            f"**📅 Duration:** {p.get('duration_days', 'N/A')} days  \n"
            f"**💰 Price:** ${price:,.2f}  \n"
            f"**📝 Description:** {p.get('description', 'N/A')}"
        )

    except Exception as e:
        return f"❌ Error creating package: {e}"

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
