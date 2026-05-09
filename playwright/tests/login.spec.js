import { test, expect } from '@playwright/test'


test.describe('Login — negative', () => {

    test('Login with wrong password', async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.fill('#user-name', 'standard_user')
        await page.fill('#password', 'wrongpassxdddd')
        await page.click('[data-test="login-button"]')
        await expect(page.locator('[data-test="error"]')).toBeVisible()
    })

    test('Login with no credentials at all', async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.click('[data-test="login-button"]')
        await expect(page.locator('[data-test="error"]')).toBeVisible()
    })

})

test.describe('Inventory', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.fill('#user-name', 'standard_user')
        await page.fill('#password', 'secret_sauce')
        await page.click('[data-test="login-button"]')
        await expect(page).toHaveURL('https://www.saucedemo.com/inventory.html')
    })

    test('After login products are visible', async ({ page }) => {
        await expect(page.locator('[data-test="inventory-item-sauce-labs-backpack-img"]')).toBeVisible()
    })

    test('Verify product count is correct', async ({ page }) => {
        await expect(page.locator('[data-test="inventory-item"]')).toHaveCount(6)
    })

    test('Verify product name is visible', async ({ page }) => {
        await expect(page.getByText('Sauce Labs Backpack')).toBeVisible()
    })  

    test('Full cart testing', async ({ page }) => {
        await page.click('#add-to-cart-sauce-labs-backpack')
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toBeVisible()
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1')
        await page.click('#add-to-cart-sauce-labs-bike-light')
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toBeVisible()
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('2')
        await page.click('#remove-sauce-labs-backpack')
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toBeVisible()
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1')
        
    })

    test('Full lifecycle on e-commerce website', async ({ page }) => {
        await page.click('#add-to-cart-sauce-labs-backpack')
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toBeVisible()
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1')
        await page.click('[data-test="shopping-cart-link"]')
        await expect(page.locator('[data-test="title"]')).toBeVisible()
        await page.click('[data-test="checkout"]')
        await page.fill('[data-test="firstName"]', 'Patrik')
        await page.fill('[data-test="lastName"]', 'Tichy')
        await page.fill('[data-test="postalCode"]', '04001')
        await page.click('[data-test="continue"]')
        await expect(page.locator('[data-test="total-info-label"]')).toBeVisible()
        await page.click('[data-test="finish"]')
        await expect(page.locator('[data-test="complete-header"]')).toBeVisible()
        await page.click('[data-test="back-to-products"]')
        await expect(page).toHaveURL('https://www.saucedemo.com/inventory.html')
    })

    test('Full lifecycle on e-commerce website with 1 field not filled in the checkout', async ({ page }) => {
        await page.click('#add-to-cart-sauce-labs-backpack')
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toBeVisible()
        await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1')
        await page.click('[data-test="shopping-cart-link"]')
        await expect(page.locator('[data-test="title"]')).toBeVisible()
        await page.click('[data-test="checkout"]')
        await page.fill('[data-test="firstName"]', 'Patrik')
        await page.fill('[data-test="lastName"]', 'Tichy')
        await page.click('[data-test="continue"]')
        await expect(page.locator('[data-test="error-button"]')).toBeVisible()
    })

})
