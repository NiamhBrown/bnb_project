from playwright.sync_api import Page, expect, sync_playwright

# Tests for your routes go here

# """
# We can render the index page
# """
# def test_get_index(page, test_web_address):
#     # We load a virtual browser and navigate to the /index page
#     page.goto(f"http://{test_web_address}/index")

#     # We look at the <p> tag
#     p_tag = page.locator("p")

#     # We assert that it has the text "This is the homepage."
#     expect(p_tag).to_have_text("This is the homepage.")

def test_get_login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    # Check if the page contains the expected text
    page.fill("input[name='email']",'test1@gmail.com')
    page.fill("input[name='password']",'password123')
    page.click("text='Login'")
    login_text = page.locator("h1")
    expect(login_text).to_have_text("Hello, test1@gmail.com! You are logged in.")
    
    
def test_sign_out(page, test_web_address):
    test_get_login(page, test_web_address) #Go through login process
    page.click("text='Sign Out'")
    sign_out_text = page.locator("h2")
    expect(sign_out_text).to_have_text("Please log in")
    
def test_for_invalid_password(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    # Check if the page contains the expected text
    page.fill("input[name='email']",'test1@gmail.com')
    page.fill("input[name='password']",'password12')
    page.click("text='Login'")
    invalid_text = page.locator("h1")
    expect(invalid_text).to_have_text("Invalid email or password.")
    
    
def test_for_invalid_email(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    # Check if the page contains the expected text
    page.fill("input[name='email']",'liamadrian@hotmail.com')
    page.fill("input[name='password']",'password123')
    page.click("text='Login'")
    invalid_text = page.locator("h1")
    expect(invalid_text).to_have_text("Invalid email or password.")


def test_for_back_to_login_button_working(page, test_web_address):
    test_for_invalid_password(page, test_web_address)
    page.click("text='Back to login'")
    click_text = page.locator("h2")
    expect(click_text).to_have_text("Please log in")
    expect(click_text).to_have_text("Please log in")
    