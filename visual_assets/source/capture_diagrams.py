import asyncio
from playwright.async_api import async_playwright
import os

async def capture_screenshots():
    # Ensure output directory exists
    output_dir = "visual_assets"
    os.makedirs(output_dir, exist_ok=True)

    # Get absolute path to source directory
    source_dir = os.path.abspath("visual_assets/source")

    files_to_capture = [
        ("architecture.html", "architecture_diagram.png"),
        ("flowchart.html", "flow_chart.png"),
        ("wireframe_dashboard.html", "dashboard_wireframe.png"),
        ("wireframe_conversation.html", "conversation_wireframe.png")
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Set viewport to ensure high resolution capture
        await page.set_viewport_size({"width": 1920, "height": 1080})

        for html_file, png_file in files_to_capture:
            file_path = os.path.join(source_dir, html_file)
            if not os.path.exists(file_path):
                print(f"Skipping {html_file} (not found)")
                continue

            url = f"file://{file_path}"
            print(f"Capturing {html_file}...")

            await page.goto(url)
            # Wait for Mermaid/rendering to finish (generic wait)
            await page.wait_for_timeout(2000)

            # Locate the container to take a cleaner screenshot
            # If container not found, take full page
            try:
                locator = page.locator(".container")
                if await locator.count() > 0:
                    await locator.screenshot(path=os.path.join(output_dir, png_file))
                else:
                     await page.screenshot(path=os.path.join(output_dir, png_file), full_page=True)
            except Exception as e:
                print(f"Error capturing {html_file}: {e}")
                await page.screenshot(path=os.path.join(output_dir, png_file), full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
