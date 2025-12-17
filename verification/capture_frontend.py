from playwright.sync_api import sync_playwright
import os

def capture_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the frontend HTML file directly
        frontend_path = os.path.abspath("src/frontend/index.html")
        url = f"file://{frontend_path}"

        page.goto(url)
        # Wait for the simulated fetch to update the dashboard (stats load in useEffect)
        page.wait_for_timeout(2000)

        page.screenshot(path="verification/dashboard_screenshot.png")
        browser.close()

if __name__ == "__main__":
    capture_frontend()
