#!/usr/bin/env python
"""
Selenium Functional UI Test Suite for https://www.saucedemo.com/

Scenario:
  1. Log in as a standard user.
  2. Add every product on the inventory page to the cart.
  3. Verify the cart badge count matches the number of products added.
  4. Remove every product from the cart.
  5. Verify the cart badge is gone (cart is empty).

Run:
    python3 cart_test_suite.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SITE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"


def log(message):
    print(f"[TEST] {message}")


def login(driver, wait):
    log(f"Navigating to site: {SITE_URL}")
    driver.get(SITE_URL)

    log(f"Logging in as '{USERNAME}'")
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_item")))
    log("Login successful, inventory page loaded")


def add_all_products_to_cart(driver, wait):
    inventory_items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item")
    total_products = len(inventory_items)
    log(f"Found {total_products} products on the inventory page")

    for item in inventory_items:
        item_name = item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
        add_button = item.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart-']")
        add_button.click()
        log(f"Added to cart: {item_name}")

    cart_badge = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".shopping_cart_badge"))
    )
    cart_count = cart_badge.text
    log(f"Cart badge shows: {cart_count} item(s)")

    assert cart_count == str(total_products), (
        f"Expected cart badge to show {total_products}, but got {cart_count}"
    )
    log("PASS: Cart badge count matches number of products added")

    return total_products


def remove_all_products_from_cart(driver, wait):
    inventory_items = driver.find_elements(By.CSS_SELECTOR, ".inventory_item")
    total_to_remove = 0

    for item in inventory_items:
        remove_buttons = item.find_elements(By.CSS_SELECTOR, "button[id^='remove-']")
        if not remove_buttons:
            continue
        item_name = item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
        remove_buttons[0].click()
        log(f"Removed from cart: {item_name}")
        total_to_remove += 1

    log(f"Removed {total_to_remove} product(s) from the cart")

    cart_badges = driver.find_elements(By.CSS_SELECTOR, ".shopping_cart_badge")
    if len(cart_badges) == 0:
        log("PASS: Cart is empty, no badge displayed")
    else:
        log(f"FAIL: Expected no cart badge, but found: {cart_badges[0].text}")
        raise AssertionError("Cart badge still present after removing all items")


def main():
    log("Starting Selenium test suite: add all products to cart, then remove them")
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        login(driver, wait)
        total_products = add_all_products_to_cart(driver, wait)
        remove_all_products_from_cart(driver, wait)
        log(f"TEST SUITE PASSED: successfully added and removed {total_products} products")
    except Exception as e:
        log(f"TEST SUITE FAILED: {e}")
        raise
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()